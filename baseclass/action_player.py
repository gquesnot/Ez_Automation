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
                if len(self.parent.mouseToPress) > 0:
                    action = self.parent.mouseToPress.pop(0)
                    print('mouse press:', action)
                    self.parent.game.kc.handleMouseActionRecord(action, release=False)
                    self.parent.mousePressed.append(action)
                if len(self.parent.mouseToRelease) > 0:
                    action = self.parent.mouseToRelease.pop(0)
                    print('mouse release:', action)
                    self.parent.game.kc.handleMouseActionRecord(action, release=True)
            elif self.type == 'keyboard':
                if len(self.parent.keyToPress) > 0:
                    action = self.parent.keyToPress.pop(0)
                    print('key press:', action)
                    self.parent.game.kc.handleKeyboardActionRecord(action, release=False)
                    self.parent.keyPressed.append(action)
                if len(self.parent.keyToRelease) > 0:
                    action = self.parent.keyToRelease.pop(0)
                    print('key release:', action)
                    self.parent.game.kc.handleKeyboardActionRecord(action, release=True)
            sleep(0.01)


class ActionReplay(ActionRecordConfigs, ThreadClass):
    game: 'Game' = None
    mousePressed: list = None
    mouseToPress: list = None
    mouseToRelease: list = None
    keyToPress: list = None
    keyPressed: list = None
    keyToRelease: list = None
    selectedRecord: ActionRecordConfig = None
    clicksCursor: int = 0
    keysCursor: int = 0

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.dict = self.game.config.replayActions.dict
        self.mouseThread = ActionThread(self, type_="mouse")
        self.keyboardThread = ActionThread(self, type_="keyboard")

    def select(self, hint):
        self.selectedRecord = self.get(hint)
        self.clicksCursor = 0
        self.keysCursor = 0
        return self.selectedRecord is not None

    def play(self, hint):
        if self.select(hint):
            self.start()

    def start(self):
        if self.selectedRecord is None:
            return
        self.mousePressed = []
        self.mouseToPress = []
        self.mouseToRelease = []
        self.keyToPress = []
        self.keyPressed = []
        self.keyToRelease = []
        self.clicksCursor = 0
        self.keysCursor = 0
        self.mouseThread.start()
        self.keyboardThread.start()
        super().start()

    def allEmpty(self):
        return len(self.mouseToPress) == 0 and len(self.mouseToRelease) == 0 and len(self.keyToPress) == 0 and len(
            self.keyToRelease) == 0 and len(self.mousePressed) == 0 and len(self.keyPressed) == 0

    def stop(self):
        self.mouseThread.stop()
        self.keyboardThread.stop()
        self.game.kc.clearInput()
        super().stop()

    def run(self):
        t = time()
        lenClicks = len(self.selectedRecord.clicks) - 1
        lenKeys = len(self.selectedRecord.keys) - 1
        maxT = self.selectedRecord.totalDuration()
        while not self.stopped:
            now = time() - t
            if self.allEmpty() and now > maxT + 1:
                self.game.app.view.content.replay(isFirst=False)
                continue

            if self.clicksCursor <= lenClicks:
                click = self.selectedRecord.clicks[self.clicksCursor]
                if click.startAt <= now:
                    self.mouseToPress.append(click)
                    self.clicksCursor += 1

            if self.keysCursor <= lenKeys:
                key = self.selectedRecord.keys[self.keysCursor]
                if key.startAt <= now:
                    self.keyToPress.append(key)
                    self.keysCursor += 1

            for action in self.mousePressed:
                if action.endAt <= now:
                    self.mouseToRelease.append(action)
                    self.mousePressed.remove(action)
            for action in self.keyPressed:
                if action.endAt <= now:
                    self.keyToRelease.append(action)
                    self.keyPressed.remove(action)
            sleep(0.01)
