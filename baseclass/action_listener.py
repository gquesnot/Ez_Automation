from time import time
from typing import Union

from pynput import mouse, keyboard
from pynput.keyboard import Key

from baseclass.my_dataclass.action_record import ActionKeyBoardRecord, ActionMouseClickRecord, ActionMouseDragRecord
from baseclass.my_dataclass.action_record_config import ActionRecordConfig
from baseclass.my_dataclass.coor import Coor


class ActionListener:
    t: float = 0
    incomplete_key_actions = {}
    incomplete_mouse_actions = {}
    game: 'Game' = None
    actions: list = []
    mouse_action: Union[ActionMouseClickRecord, None] = None
    mouse_listener: mouse.Listener = None
    keyboard_listener: keyboard.Listener = None
    selected: ActionRecordConfig = None
    stopped = False

    def __init__(self, game):
        self.game = game

    def start(self):
        self.selected = ActionRecordConfig()
        self.mouse_action = None
        self.incomplete_key_actions = {}
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
        self.selected.keys.sort(key=lambda x: x.start_at)
        self.selected.clicks.sort(key=lambda x: x.start_at)

        for el in self.selected.all():
            print(el)

    def on_click(self, x, y, button, pressed):
        if pressed and not (
                self.game.wc.x <= x <= self.game.wc.x + self.game.wc.w and self.game.wc.y <= y <= self.game.wc.y + self.game.wc.h):
            return

        if pressed:
            self.mouse_action = ActionMouseClickRecord(coor_start=self.game.wc.from_window(Coor(x, y)),
                                                       start_at=time() - self.t)
        else:
            if self.mouse_action is not None:

                coor_end = self.game.wc.from_window(Coor(x, y))
                self.mouse_action.end_at = time() - self.t
                if abs(coor_end.x - self.mouse_action.coor_start.x) >= 5 and abs(
                        coor_end.y - self.mouse_action.coor_start.y) >= 5:
                    self.selected.clicks.append(
                        ActionMouseDragRecord(coor_start=self.mouse_action.coor_start, coor_end=coor_end,
                                              start_at=self.mouse_action.start_at,
                                              endAt=self.mouse_action.end_at))
                else:
                    self.selected.clicks.append(self.mouse_action)
                self.mouse_action = None

    def on_scroll(self, x, y, dx, dy):
        print("pass scroll", x, y, dx, dy)

    def on_keyboard_release(self, key):
        try:
            char = key.vk
        except:
            char = key.value.vk
        if char is not None and char in self.incomplete_key_actions:
            self.incomplete_key_actions[char].endAt = time() - self.t
            self.selected.keys.append(self.incomplete_key_actions[char])
            del self.incomplete_key_actions[char]

    def on_press(self, key):
        if key == Key.esc:
            self.game.app.view.content.record(is_first=False)
            return False
        try:
            char = key.vk
        except:
            char = key.value.vk
        if char is not None and char > 7:
            self.incomplete_key_actions[char] = ActionKeyBoardRecord(key=char, start_at=time() - self.t)
        else:
            print("keyboard error", key, char)
