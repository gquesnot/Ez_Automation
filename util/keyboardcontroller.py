from time import sleep

import pyautogui
from pynput.keyboard import Listener
from pynput.keyboard import Key, Controller
from util.threadclass import ThreadClass
from pynput.mouse import Button, Controller as MC


# The event listener will be running in this block


class KeyboardController(ThreadClass):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.mouseRatio = 0.3
        self.pressed = set()
        self.keyboard = Controller()
        self.mouse = MC()

    def press(self, combo=[]):
        for c in self.pressed:
            self.keyboard.release(c)
        for c in combo:
            self.keyboard.press(c)
        self.pressed.add(set(combo))

    def handleMouseAction(self, mouseAction):
        if mouseAction['region'] != "root":
            coor = self.game.regions.getCoorByRegion(mouseAction['region'], (mouseAction['x'], mouseAction['y']))
        else:
            coor = (mouseAction['x'], mouseAction['y'])
        self.mouseMove(coor)
        self.click(mouseAction['delay'])
        sleep(mouseAction['sleepAfter'])

    def handleKeyAction(self, keyAction):
        self.basePress(keyAction['key'], keyAction['duration'])
        sleep(keyAction['sleepAfter'])


    def moveClick(self, coor,delay=.5, byScreen=True, timeBeetwen=.25):
        self.mouseMove(coor, byScreen)
        sleep(timeBeetwen)
        self.click(delay)

    def click(self,delay=.5):
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
