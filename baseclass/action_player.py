from time import time, sleep

from baseclass.my_dataclass.action_record_config import ActionRecordConfigs, ActionRecordConfig
from util.threadclass import ThreadClass


class ActionThread(ThreadClass):
    parent: 'ActionReplay' = None

    def __init__(self, parent, type_):
        super().__init__()
        self.parent = parent
        self.type = type_

    def run(self):
        while not self.stopped:
            if self.type == 'mouse':
                if len(self.parent.mouse_to_press) > 0:
                    action = self.parent.mouse_to_press.pop(0)
                    print('mouse press:', action)
                    self.parent.game.kc.handle_mouse_action_record(action, release=False)
                    self.parent.mouse_pressed.append(action)
                if len(self.parent.mouse_to_release) > 0:
                    action = self.parent.mouse_to_release.pop(0)
                    print('mouse release:', action)
                    self.parent.game.kc.handle_mouse_action_record(action, release=True)
            elif self.type == 'keyboard':
                if len(self.parent.key_to_press) > 0:
                    action = self.parent.key_to_press.pop(0)
                    print('key press:', action)
                    self.parent.game.kc.handle_keyboard_action_record(action, release=False)
                    self.parent.key_pressed.append(action)
                if len(self.parent.key_to_release) > 0:
                    action = self.parent.key_to_release.pop(0)
                    print('key release:', action)
                    self.parent.game.kc.handle_keyboard_action_record(action, release=True)
            sleep(0.01)


class ActionReplay(ActionRecordConfigs, ThreadClass):
    game: 'Game' = None
    mouse_pressed: list = None
    mouse_to_press: list = None
    mouse_to_release: list = None
    key_to_press: list = None
    key_pressed: list = None
    key_to_release: list = None
    selected_record: ActionRecordConfig = None
    clicks_cursor: int = 0
    keys_cursor: int = 0

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.dict = self.game.config.replay_actions.dict
        self.mouse_thread = ActionThread(self, type_="mouse")
        self.keyboard_thread = ActionThread(self, type_="keyboard")

    def select(self, hint):
        self.selected_record = self.get(hint)
        self.clicks_cursor = 0
        self.keys_cursor = 0
        return self.selected_record is not None

    def play(self, hint):
        if self.select(hint):
            self.start()

    def start(self):
        if self.selected_record is None:
            return
        self.mouse_pressed = []
        self.mouse_to_press = []
        self.mouse_to_release = []
        self.key_to_press = []
        self.key_pressed = []
        self.key_to_release = []
        self.clicks_cursor = 0
        self.keys_cursor = 0
        self.mouse_thread.start()
        self.keyboard_thread.start()
        super().start()

    def all_empty(self):
        return len(self.mouse_to_press) == 0 and len(self.mouse_to_release) == 0 and len(
            self.key_to_press) == 0 and len(
            self.key_to_release) == 0 and len(self.mouse_pressed) == 0 and len(self.key_pressed) == 0

    def stop(self):
        self.mouse_thread.stop()
        self.keyboard_thread.stop()
        self.game.kc.clear_input()
        super().stop()

    def run(self):
        t = time()
        len_clicks = len(self.selected_record.clicks) - 1
        len_keys = len(self.selected_record.keys) - 1
        max_t = self.selected_record.total_duration()
        while not self.stopped:
            now = time() - t
            if self.all_empty() and now > max_t + 1:
                self.game.app.view.content.replay(is_first=False)
                continue

            if self.clicks_cursor <= len_clicks:
                click = self.selected_record.clicks[self.clicks_cursor]
                if click.start_at <= now:
                    self.mouse_to_press.append(click)
                    self.clicks_cursor += 1

            if self.keys_cursor <= len_keys:
                key = self.selected_record.keys[self.keys_cursor]
                if key.start_at <= now:
                    self.key_to_press.append(key)
                    self.keys_cursor += 1

            for action in self.mouse_pressed:
                if action.endAt <= now:
                    self.mouse_to_release.append(action)
                    self.mouse_pressed.remove(action)
            for action in self.key_pressed:
                if action.endAt <= now:
                    self.key_to_release.append(action)
                    self.key_pressed.remove(action)
            sleep(0.01)
