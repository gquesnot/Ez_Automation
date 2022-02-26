import copy
import ctypes
from threading import Lock

import numpy as np
import win32con
import win32gui
import win32ui
from mss import mss

from baseclass.my_dataclass.window_config import WindowConfig

user32 = ctypes.WinDLL('user32', use_last_error=True)

gameName = ""


def find_window(hwnd, strings):
    global gameName
    window_title = win32gui.GetWindowText(hwnd)
    # print(window_title)
    if gameName in window_title:
        strings.append({"hwnd": hwnd, "name": window_title})


class WindowCapture:
    w = 0
    h = 0
    hwnd = None
    isLoaded : bool = False
    offset_x = 0
    offset_y = 0
    x = 0
    y = 0
    x1 = 0
    y1 = 0
    center = 0
    halfSize = 0
    stopped = True
    lock = None
    screenshot = None
    modifiedScreenshot = None

    firstTime = True
    config: WindowConfig = None

    def __init__(self, game, fps=False, imgGrab=False):

        self.game = game
        self.imgGrab = imgGrab
        if self.imgGrab:
            self.sct = mss()
        self.fps = fps
        self.lock = Lock()
        self.config = self.game.config.window
        if self.config.name != "":
            self.loadConfig()
        self.firstTime = False

    def updateWindowInfo(self):
        global gameName
        winList = []
        win32gui.EnumWindows(find_window, winList)
        if len(winList) > 0:
            self.hwnd = winList[0]["hwnd"]
            self.config.name = winList[0]["name"]

        else:
            self.hwnd = win32gui.FindWindow(None, gameName)
            print("test get name other", win32gui.GetWindowText(self.hwnd))

    def loadConfig(self):

        global gameName
        gameName = self.config.name
        self.updateWindowInfo()
        isLoaded= self.activate()
        if not isLoaded: return
        self.x, self.y, self.x1, self.y1 = win32gui.GetWindowRect(self.hwnd)

        self.h = self.y1 - self.y + self.config.h_diff
        self.w = self.x1 - self.x + self.config.w_diff
        self.offset_x = self.x + self.config.cropped_x
        self.offset_y = self.y + self.config.cropped_y
        self.center = {"x": int(self.w / 2), "y": int(self.h / 2)}
        self.halfSize = (int(self.w / 2), int(self.h / 2))
        self.isLoaded = isLoaded

    def getCenter(self):
        return self.center['x'], self.center['y']

    def copy(self):
        return copy.deepcopy(self.screenshot)

    def activate(self):
        try:
            win32gui.SetForegroundWindow(self.hwnd)
            return True
        except:
            try:
                win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
                win32gui.SetForegroundWindow(self.hwnd)
                return True
            except:
                print("no window found")

        return False

    def coorAsList(self):
        return {"top": self.offset_y, "left": self.offset_x, "width": self.w, "height": self.h}

    def stop(self):
        self.stopped = True

    def getScreenshot(self):
        try:

            if not self.imgGrab:
                return self.getBaseScreenShot()
            else:
                return self.getImgGrab()
        except:
            return None

    def get_screen_position(self, pos):
        return pos[0] + self.offset_x, pos[1] + self.offset_y

    def getImgGrab(self):
        return np.array(self.sct.grab(self.coorAsList()))[..., :3]

    def getBaseScreenShot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDc = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDc.SelectObject(dataBitMap)
        cDc.BitBlt((0, 0), (self.w, self.h), dcObj, (self.config.cropped_x, self.config.cropped_y), win32con.SRCCOPY)
        signedIntArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        dcObj.DeleteDC()
        cDc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = np.ascontiguousarray(img)

        return img
