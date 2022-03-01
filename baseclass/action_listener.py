from time import time
from typing import Union

from pynput import mouse, keyboard
from pynput.keyboard import Key, KeyCode

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
        self.selected.actions.sort(key=lambda x: x.startAt)

    def on_click(self, x, y, button, pressed):
        if self.game.wc.x <= x <= self.game.wc.x + self.game.wc.w and self.game.wc.y <= y <= self.game.wc.y + self.game.wc.h:
            if pressed:
                self.mouseAction = ActionMouseClickRecord(coorStart=self.game.wc.windowCoor(Coor(x, y)),
                                                          startAt=time() - self.t)
            else:
                if self.mouseAction is not None:

                    coorEnd = self.game.wc.windowCoor(Coor(x, y))
                    self.mouseAction.endAt = time() - self.t
                    if abs(coorEnd.x - self.mouseAction.coorStart.x) >= 5 and abs(
                            coorEnd.y - self.mouseAction.coorStart.y) >= 5:
                        self.selected.actions.append(
                            ActionMouseDragRecord(coorStart=self.mouseAction.coorStart, coorEnd=coorEnd,
                                                  startAt=self.mouseAction.startAt,
                                                  endAt=self.mouseAction.endAt))
                    else:
                        self.selected.actions.append(self.mouseAction)
                    self.mouseAction = None

    def on_scroll(self, x, y, dx, dy):
        print("pass scroll", x, y, dx, dy)

    def on_keyboard_release(self, key):
        if key in self.incompleteKeyActions:
            self.incompleteKeyActions[key].endAt = time() - self.t
            self.selected.actions.append(self.incompleteKeyActions[key])
            del self.incompleteKeyActions[key]

    def on_press(self, key):
        if key == Key.esc:
            self.stop()
            return False
        print(key,str(key), type(key))        
        self.incompleteKeyActions[key] = ActionKeyBoardRecord(key=key, startAt=time() - self.t)
