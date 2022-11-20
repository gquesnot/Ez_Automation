from time import sleep
from typing import Union

import pyautogui
from pynput.keyboard import Controller, KeyCode
from pynput.keyboard import Listener
from pynput.mouse import Button, Controller as MC

from baseclass.my_dataclass.action_record import ActionMouseClickRecord, ActionMouseDragRecord, ActionKeyBoardRecord
from util.threadclass import ThreadClass


class KeyboardController(ThreadClass):
    mouse: MC = None
    keybord: Controller = None

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.mouse_ratio = 0.3
        self.pressed = set()
        self.keyboard = Controller()
        self.mouse = MC()

    def press(self, combo=None):
        if combo is None:
            combo = []
        for c in self.pressed:
            self.keyboard.release(c)
        for c in combo:
            self.keyboard.press(c)
        self.pressed.add(set(combo))

    def handle_mouse_action_record(self, action: Union[ActionMouseClickRecord, ActionMouseDragRecord], release=False):
        if release:
            if type(action) == ActionMouseDragRecord:
                self.mouse.move(*self.game.wc.to_window(action.coor_end, *self.mouse.position))
            self.mouse.release(Button.left)
        else:
            self.mouse.move(*self.game.wc.to_window(action.coor_start, *self.mouse.position))

            self.mouse.press(Button.left)

    def clear_input(self):
        for c in self.pressed:
            self.keyboard.release(c)

    def handle_keyboard_action_record(self, action: ActionKeyBoardRecord, release=False):
        if release:
            self.keyboard.press(KeyCode.from_vk(action.key))
            self.pressed.remove(action.key)
        else:
            self.keyboard.release(KeyCode.from_vk(action.key))
            self.pressed.add(action.key)

    def handle_mouse_action(self, mouse_action):
        if mouse_action.region != "root":
            coor = self.game.regions.get_coorByRegion(mouse_action.region)
            coor = (mouse_action.coor.x + coor.x, mouse_action.coor.y + coor.y)
        else:
            coor = (mouse_action.coor.x, mouse_action.coor.y)
        self.mouse_move(coor)
        self.click(mouse_action.delay)
        sleep(mouse_action.sleep_after)

    def handle_key_action(self, keyAction):
        self.base_press(keyAction.key, keyAction.delay)
        sleep(keyAction.sleep_after)

    def move_click(self, coor, delay=.5, by_screen=True, time_beetwen=.25):
        self.mouse_move(coor, by_screen)
        sleep(time_beetwen)
        self.click(delay)

    def click(self, delay=.5):
        self.mouse.press(Button.left)
        sleep(delay)
        self.mouse.release(Button.left)

    def mouse_move(self, coor, by_screen=True):
        if by_screen:
            self.mouse.position = (coor[0] + self.game.wc.offset_x, coor[1] + self.game.wc.offset_y)
        else:
            self.mouse.position = coor

    def focus(self, coor):
        self.mouse_move(coor)
        sleep(0.1)
        self.mouse.press(Button.right)
        x, y = coor
        center_x, center_y = self.game.wc.get_center()
        diff_x = -int((x - center_x) * self.mouse_ratio)
        diff_y = -int((y - center_y) * self.mouse_ratio)
        print("diff", x, y, center_x, center_y, diff_x, diff_y)
        sleep(0.1)
        self.mouse.move(diff_x, diff_y)
        sleep(0.1)
        self.mouse.release(Button.right)

    def press_key(self, c):
        if c not in self.pressed:
            self.keyboard.press(c)

    def release_key(self, c):
        if c in self.pressed:
            self.keyboard.release(c)

    def reset_movement(self):
        for c in self.pressed:
            if c in ("z", "s", "q", "d"):
                self.keyboard.release(c)

    def base_press(self, key, duration=.01):
        self.keyboard.press(key)
        sleep(duration)
        self.keyboard.release(key)

    def base_press2(self, key, duration=.01):
        pyautogui.keyDown(key)
        sleep(duration)
        pyautogui.keyUp(key)

    def on_press(self, key):

        self.pressed.add(key)

    def on_release(self, key):
        self.pressed.remove(key)

    def run(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
