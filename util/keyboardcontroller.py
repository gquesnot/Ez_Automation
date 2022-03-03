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
        self.mouseRatio = 0.3
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

    def handleMouseActionRecord(self, action: Union[ActionMouseClickRecord,ActionMouseDragRecord] , release=False):
        if release:
            if type(action) == ActionMouseDragRecord:

                self.mouse.move(*self.game.wc.toWindow(action.coorEnd, *self.mouse.position))
            self.mouse.release(Button.left)
        else:
            self.mouse.move(*self.game.wc.toWindow(action.coorStart, *self.mouse.position))

            self.mouse.press(Button.left)

    def clearInput(self):
        for c in self.pressed:
            self.keyboard.release(c)

    def handleKeyboardActionRecord(self, action: ActionKeyBoardRecord, release=False):
        if release:
            self.keyboard.press(KeyCode.from_vk(action.key))
            self.pressed.remove(action.key)
        else:
            self.keyboard.release(KeyCode.from_vk(action.key))
            self.pressed.add(action.key)


    def handleMouseAction(self, mouseAction):
        if mouseAction.region != "root":
            coor = self.game.regions.getCoorByRegion(mouseAction.region)
            coor = (mouseAction.coor.x + coor.x, mouseAction.coor.y + coor.y)
        else:
            coor = (mouseAction.coor.x, mouseAction.coor.y)
        self.mouseMove(coor)
        self.click(mouseAction.delay)
        sleep(mouseAction.sleepAfter)

    def handleKeyAction(self, keyAction):
        self.basePress(keyAction.key, keyAction.delay)
        sleep(keyAction.sleepAfter)

    def moveClick(self, coor, delay=.5, byScreen=True, timeBeetwen=.25):
        self.mouseMove(coor, byScreen)
        sleep(timeBeetwen)
        self.click(delay)

    def click(self, delay=.5):
        self.mouse.press(Button.left)
        sleep(delay)
        self.mouse.release(Button.left)

    def mouseMove(self, coor, byScreen=True):
        if byScreen:
            self.mouse.position = (coor[0] + self.game.wc.offset_x, coor[1] + self.game.wc.offset_y)
        else:
            self.mouse.position = coor

    def focus(self, coor):
        self.mouseMove(coor)
        sleep(0.1)
        self.mouse.press(Button.right)
        x, y = coor
        centerX, centerY = self.game.wc.getCenter()
        diffX = -int((x - centerX) * self.mouseRatio)
        diffY = -int((y - centerY) * self.mouseRatio)
        print("diff", x, y, centerX, centerY, diffX, diffY)
        sleep(0.1)
        self.mouse.move(diffX, diffY)
        sleep(0.1)
        self.mouse.release(Button.right)

    def pressKey(self, c):
        if c not in self.pressed:
            self.keyboard.press(c)

    def releaseKey(self, c):
        if c in self.pressed:
            self.keyboard.release(c)

    def resetMovement(self):
        for c in self.pressed:
            if c in ("z", "s", "q", "d"):
                self.keyboard.release(c)

    def basePress(self, key, duration=.01):
        self.keyboard.press(key)
        sleep(duration)
        self.keyboard.release(key)

    def basePress2(self, key, duration=.01):
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
