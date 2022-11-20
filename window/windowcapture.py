import copy
import ctypes
from threading import Lock

import numpy as np
import win32con
import win32gui
import win32ui
from mss import mss

from baseclass.my_dataclass.coor import Coor
from baseclass.my_dataclass.window_config import WindowConfig

user32 = ctypes.WinDLL('user32', use_last_error=True)

game_name = ""


def find_window(hwnd, strings):
    global game_name
    window_title = win32gui.GetWindowText(hwnd)
    # print(window_title)
    if game_name in window_title:
        strings.append({"hwnd": hwnd, "name": window_title})


class WindowCapture:
    w = 0
    h = 0
    hwnd = None
    is_loaded: bool = False
    offset_x = 0
    offset_y = 0
    x = 0
    y = 0
    x1 = 0
    y1 = 0
    center = 0
    half_size = 0
    stopped = True
    lock = None
    screenshot = None
    modified_screenshot = None

    first_time = True
    config: WindowConfig = None

    def __init__(self, game, fps=False, img_grab=False):

        self.game = game
        self.img_grab = img_grab
        if self.img_grab:
            self.sct = mss()
        self.fps = fps
        self.lock = Lock()
        self.config = self.game.config.window
        if self.config.name != "":
            self.load_config()
        self.first_time = False

    def update_window_info(self):
        global game_name
        win_list = []
        win32gui.EnumWindows(find_window, win_list)
        if len(win_list) > 0:
            self.hwnd = win_list[0]["hwnd"]
            self.config.name = win_list[0]["name"]

        else:
            self.hwnd = win32gui.FindWindow(None, game_name)
            print("test get name other", win32gui.GetWindowText(self.hwnd))

    def load_config(self):

        global game_name
        game_name = self.config.name
        self.update_window_info()
        is_loaded = self.activate()
        if not is_loaded: return
        self.x, self.y, self.x1, self.y1 = win32gui.GetWindowRect(self.hwnd)

        self.h = self.y1 - self.y + self.config.h_diff
        self.w = self.x1 - self.x + self.config.w_diff
        self.offset_x = self.x + self.config.cropped_x
        self.offset_y = self.y + self.config.cropped_y
        self.center = {"x": int(self.w / 2), "y": int(self.h / 2)}
        self.half_size = (int(self.w / 2), int(self.h / 2))
        self.is_loaded = is_loaded
        print("window loaded", self.offset_x, self.offset_y, self.w, self.h, self.center)

    def get_center(self):
        return self.center['x'], self.center['y']

    def copy(self):
        return copy.deepcopy(self.screenshot)

    def activate(self):
        try:
            print('activate window')
            win32gui.ShowWindow(self.hwnd, 5)
            win32gui.SetForegroundWindow(self.hwnd)
            return True
        except:
            try:
                print('try hard to activate window')
                win32gui.ShowWindow(self.hwnd, 5)
                win32gui.SetForegroundWindow(self.hwnd)
                return True
            except:
                print("no window found")

        return False

    def coor_as_list(self):
        return {"top": self.offset_y, "left": self.offset_x, "width": self.w, "height": self.h}

    def stop(self):
        self.stopped = True

    def to_window(self, coor: Coor, position_x, position_y):
        print("toWindow", coor.x + self.offset_x, coor.y + self.offset_y, position_x, position_y)
        return coor.x + self.offset_x - position_x, coor.y + self.offset_y - position_y

    def from_window(self, coor: Coor) -> Coor:
        coor.x -= self.offset_x
        coor.y -= self.offset_y
        return coor

    def get_screenshot(self):
        try:

            if not self.img_grab:
                return self.get_base_screen_shot()
            else:
                return self.get_img_grab()
        except:
            return None

    def get_screen_position(self, pos):
        return pos[0] + self.offset_x, pos[1] + self.offset_y

    def get_img_grab(self):
        return np.array(self.sct.grab(self.coor_as_list()))[..., :3]

    def get_base_screen_shot(self):
        w_dc = win32gui.GetWindowDC(self.hwnd)
        dc_obj = win32ui.CreateDCFromHandle(w_dc)
        c_dc = dc_obj.CreateCompatibleDC()
        data_bit_map = win32ui.CreateBitmap()
        data_bit_map.CreateCompatibleBitmap(dc_obj, self.w, self.h)
        c_dc.SelectObject(data_bit_map)
        c_dc.BitBlt((0, 0), (self.w, self.h), dc_obj, (self.config.cropped_x, self.config.cropped_y), win32con.SRCCOPY)
        signed_int_array = data_bit_map.GetBitmapBits(True)
        img = np.fromstring(signed_int_array, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        dc_obj.DeleteDC()
        c_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, w_dc)
        win32gui.DeleteObject(data_bit_map.GetHandle())

        img = img[..., :3]
        img = np.ascontiguousarray(img)

        return img
