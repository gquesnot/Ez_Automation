from time import time, sleep

from baseclass.my_dataclass.action_record import ActionMouseClickRecord, ActionMouseDragRecord, ActionKeyBoardRecord
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
                    self.parent.game.kc.handlemouseActionRecord(action, release=False)
                    self.parent.mousePressed.append(action)
                if len(self.parent.mouseToRelease) > 0:
                    print('mouse release:', self.parent.mouseToRelease[0])
                    action = self.parent.mousePressed.pop(0)
                    self.parent.game.kc.handlemouseActionRecord(action, release=True)
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
    cursor: int = 0


    def __init__(self, game):
        super().__init__()
        self.game = game
        self.dict = self.game.config.replayActions
        self.mouseThread = ActionThread(self, type_="mouse")
        self.keyboardThread = ActionThread(self, type_="keyboard")

    def select(self, hint):
        self.selectedRecord = self.get(hint)
        self.cursor = 0

    def start(self):
        if self.selectedRecord is None:
            return
        self.mousePressed = []
        self.mouseToPress = []
        self.mouseToRelease = []
        self.keyToPress = []
        self.keyPressed = []
        self.keyToRelease = []
        self.cursor = 0
        self.mouseThread.start()
        self.keyboardThread.start()
        super().start()

    def stop(self):
        self.mouseThread.stop()
        self.keyboardThread.stop()
        super().stop()

    def run(self):
        t = time()
        while not self.stopped and self.cursor < len(self.selectedRecord.actions):
            now = time() - t
            action = self.selectedRecord.actions[self.cursor]
            if action.startAt <= now:
                if type(action) in (ActionMouseClickRecord, ActionMouseDragRecord):
                    self.mouseToPress.append(action)
                elif type(action) == ActionKeyBoardRecord:
                    self.keyToPress.append(action)
                self.cursor += 1
            for action in self.mousePressed:
                if action.endAt <= now:
                    self.mouseToRelease.append(action)
                    self.mousePressed.remove(action)
            for action in self.keyPressed:
                if action.endAt <= now:
                    self.keyToRelease.append(action)
                    self.keyPressed.remove(action)
            sleep(0.01)
