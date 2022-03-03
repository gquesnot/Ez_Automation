from time import time
from typing import Union
import binascii
from pynput import mouse, keyboard
from pynput.keyboard import Key

from baseclass.my_dataclass.action_record import ActionKeyBoardRecord, ActionMouseClickRecord, ActionMouseDragRecord
from baseclass.my_dataclass.action_record_config import ActionRecordConfig
from baseclass.my_dataclass.coor import Coor


class ActionListener:
    t: float = 0
    incompleteKeyActions = {}
    incompleteMouseActions = {}
    game: 'Game' = None
    actions: list = []
    mouseAction: Union[ActionMouseClickRecord, None] = None
    mouse_listener: mouse.Listener = None
    keyboard_listener: keyboard.Listener = None
    selected: ActionRecordConfig = None
    stopped = False

    def __init__(self, game):
        self.game = game

    def start(self):
        self.selected = ActionRecordConfig()
        self.mouseAction = None
        self.incompleteKeyActions = {}
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll
                                             )
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_keyboard_release)
        self.t = time()
        self.stopped = False
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop(self):
        self.stopped = True
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.selected.keys.sort(key=lambda x: x.startAt)
        self.selected.clicks.sort(key=lambda x: x.startAt)

        for el in self.selected.all():
            print(el)

    def on_click(self, x, y, button, pressed):
        if pressed and not (self.game.wc.x <= x <= self.game.wc.x + self.game.wc.w and self.game.wc.y <= y <= self.game.wc.y + self.game.wc.h):
            return

        if pressed:
            self.mouseAction = ActionMouseClickRecord(coorStart=self.game.wc.fromWindow(Coor(x, y)),
                                                      startAt=time() - self.t)
        else:
            if self.mouseAction is not None:

                coorEnd = self.game.wc.fromWindow(Coor(x, y))
                self.mouseAction.endAt = time() - self.t
                if abs(coorEnd.x - self.mouseAction.coorStart.x) >= 5 and abs(
                        coorEnd.y - self.mouseAction.coorStart.y) >= 5:
                    self.selected.clicks.append(
                        ActionMouseDragRecord(coorStart=self.mouseAction.coorStart, coorEnd=coorEnd,
                                              startAt=self.mouseAction.startAt,
                                              endAt=self.mouseAction.endAt))
                else:
                    self.selected.clicks.append(self.mouseAction)
                self.mouseAction = None

    def on_scroll(self, x, y, dx, dy):
        print("pass scroll", x, y, dx, dy)

    def on_keyboard_release(self, key):
        try:
            char = key.vk
        except:
            char = key.value.vk
        if char is not None and char in self.incompleteKeyActions:
            self.incompleteKeyActions[char].endAt = time() - self.t
            self.selected.keys.append(self.incompleteKeyActions[char])
            del self.incompleteKeyActions[char]




    def on_press(self, key):
        if key == Key.esc:
            self.game.app.view.content.record(isFirst=False)
            return False
        try:
            char = key.vk
        except:
            char = key.value.vk
        if char is not None and char > 7:
            self.incompleteKeyActions[char] = ActionKeyBoardRecord(key=char, startAt=time() - self.t)
        else:
            print("keyboard error", key, char)



