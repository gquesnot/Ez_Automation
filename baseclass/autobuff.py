from time import time, sleep

from util.json_function import applyJsonConfig
from util.keyboardcontroller import KeyboardController
from util.threadclass import ThreadClass


class AutoBuff(ThreadClass):
    keys = {}

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.kc = KeyboardController()
        applyJsonConfig(self, "autobuff")
        self.prio1 = {}
        self.prio2 = {}
        for k, v in self.keys.items():
            if v['priority'] == 1:
                self.prio1[k] = v
            else:
                self.prio2[k] = v

    def hasActionToDo(self, prio=1):
        t = time()
        res = 0
        tmpDic = self.prio1 if prio == 1 else self.prio2
        for k, v in tmpDic.items():
            if (v['lastSeen'] == 0 or t - v['lastSeen'] >= v['duration']) and v['active']:
                res += 1
        return res

    def clickPrio(self, prio):
        t = time()
        tmpDic = self.prio1 if prio == 1 else self.prio2
        for k, v in tmpDic.items():
            if self.hasActionToDo(prio=1) > 0 and prio != 1:
                return
            if (v['lastSeen'] == 0 or t - v['lastSeen'] >= v['duration']) and v['active']:
                self.kc.basePress(k)
                print(f"pressed {k} after {round(t - v['lastSeen'], 2)}")
                v['lastSeen'] = t
                sleep(v['sleep'])

    def run(self):
        while not self.stopped:
            if self.hasActionToDo(prio=1) > 0:
                self.clickPrio(prio=1)
            if self.hasActionToDo(prio=2) > 0:
                self.clickPrio(prio=2)
            sleep(0.01)
