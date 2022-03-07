import copy
from time import sleep, time
from typing import Any
import cv2
from baseclass.action_listener import ActionListener
from baseclass.action_player import ActionReplay
from baseclass.imagesave import ImageSave
from baseclass.regions import Regions
from baseclass.replayClass import Replay
from controllers.configcontroller import ConfigController
from controllers.datapickercontroller import DataPickerController
from baseclass.my_enum.game_state import GameState
from baseclass.my_enum.game_type_state import GameTypeState
from baseclass.my_enum.location_state import LocationState
from ia.ia import IA
from util.keyboardcontroller import KeyboardController
from util.tcr import Tcr
from util.threadclass import ThreadClass
from util.timer import Timer
from window.cv2windowcontroller import Cv2WindowController
from window.windowcapture import WindowCapture


class Game(ThreadClass):
    name:str = ""
    state: GameState = GameState.WAITING
    location : LocationState= LocationState.START
    screenShot:Any = None
    firstState: bool = True
    config: ConfigController = None
    typeState: GameTypeState = GameTypeState.RECORD
    app: 'App' = None
    wc: WindowCapture = None
    replay: Replay = None
    imSave: ImageSave = None
    tcr: Tcr = None
    kc: KeyboardController = None
    dpc: DataPickerController = None
    cv2Controller: Cv2WindowController = None
    timer: Timer = None
    regions: Regions = None
    actionListener: ActionListener= None
    actionReplay: ActionReplay = None
    ia : IA = None




    def __init__(self):
        super().__init__()

        self.config = ConfigController(self)
        self.name = self.config.window.name

        self.wc = WindowCapture(self, imgGrab=True)
            # self.ac = ActionController(self)

        self.timer = Timer()
        self.RC = Replay()
        self.regions = Regions(self)
        self.imSave = ImageSave(self)
        self.actionListener = ActionListener(self)
        self.actionReplay = ActionReplay(self)
        # self.vision = Vision(hsv=True)

        if not self.isPlaying():
            self.cv2Controller = Cv2WindowController(self)
            # self.vision.init_control_gui()
        self.tcr = Tcr(self)
        self.dpc = DataPickerController(self)
        # self.trackerController = TrackerController(self)
        self.kc = KeyboardController(self)
        self.ia = IA(self)

        self.startClass()

    def initWaitingTime(self):
        i = 3
        while i > 0:
            print(f"action in {i}s")
            sleep(1)
            i -= 1

    def doClick(self, hint, activate=False, isTest=False):
        if isTest:
            self.initWaitingTime()
        if hint in self.config.mouseActions.dict:
            if activate:
                self.wc.activate()
                self.kc.moveClick(self.wc.getCenter(), delay=.1, timeBeetwen=.1)

            self.kc.handleMouseAction(self.config.mouseActions.get(hint))

    def doKey(self, hint, activate=False, isTest=False):
        if isTest:
            self.initWaitingTime()
        if hint in self.config.keyboardActions.dict:
            if activate:
                self.wc.activate()
                self.kc.moveClick(self.wc.getCenter(), delay=.1, timeBeetwen=.1)
            self.kc.handleMouseAction(self.config.keyboardActions.get(hint))


    def getScreenshotCopy(self):
        if self.screenShot is not None:
            return copy.deepcopy(self.screenShot)
        else:
            return None
    def startClass(self):
        self.ia.start()

    # def createImage(self, comboHint):
    #     if self.screenShot is not None:
    #         return self.dpc.createImage(self.screenShot, comboHint)
    #     return None

    def stop(self):
        super().stop()
        cv2.destroyAllWindows()

        # self.dpc.stopAll()

    def setGlobalState(self, state):
        self.lock.acquire()
        self.typeState = state
        self.lock.release()

    def setName(self, name):
        self.name = name

    def setState(self, state, firstState=False):
        print("NEW GAME STATE: " + state.name)
        if self.firstState or firstState:
            print("FIRST STATE SLEEPING 2s")
            # self.kc.moveClick(self.wc.getCenter())
            sleep(2)
            self.firstState = False
        self.lock.acquire()
        self.state = state
        self.lock.release()

    def isReplay(self):
        return self.typeState == GameTypeState.REPLAY

    def isRecord(self):
        return self.typeState == GameTypeState.RECORD

    def isPlaying(self):
        return self.typeState == GameTypeState.PLAY

    # def findBouchon(self):
    #     smallImg1 = cv2.imread("img/bouchon.png")
    #     smallImg2 = cv2.imread("img/bouchon2.png")
    #     result = cv2.matchTemplate(smallImg1, self.screenShot, cv2.TM_SQDIFF_NORMED)
    #
    #     # We want the minimum squared difference
    #     mn, _, mnLoc, _ = cv2.minMaxLoc(result)
    #     if mn < .1:
    #         return mnLoc
    #     else:
    #         result2 = cv2.matchTemplate(smallImg2, self.screenShot, cv2.TM_SQDIFF_NORMED)
    #         mn1, _, mnLoc2, _ = cv2.minMaxLoc(result2)
    #         if mn1 < .1:
    #             return mnLoc2
    #     print("mn", mn, mn1)
    #     return False

    def addApp(self, app):
        self.app = app

    def run(self):
        timeAfter = None
        timeBefore = None
        while not self.stopped:
            if self.config.showFps:
                timeBefore= time()
            if not self.config.freeze:
                if not self.isReplay():
                    self.screenShot = self.wc.getScreenshot()
                else:
                    self.screenShot = self.RC.getScreenshot()
                self.dpc.checkConfigHasMaskTest()
            if self.screenShot is not None:
                # code Here
                if self.state == GameState.PLAYING:
                    print('scan wave: ', self.dpc.checkTcrScan('wave'))
                    print('check pixel evt1On: ', self.dpc.checkPixel("evt1On"))
                    print('check image evt1: ', self.dpc.checkImageMatch('evt1'))
                    print('check mask greenBar: ', self.dpc.checkMaskDetection('greenBar'))
                    print('do action closeUp')
                    self.doClick('closeUpgrade')
                    self.doKey('up')
                    self.actionReplay.play('upgradeAll')
            if self.config.showFps:
                if self.screenShot is not None:
                    if timeAfter is not None and timeBefore is not None and abs(timeBefore- timeAfter) > 1 and timeAfter != timeBefore:
                        timeAfter = time()

                        self.app.view.fpsCounter.set("FPS: {:.2f}".format(1 / (timeAfter - timeBefore)))
                    elif timeAfter is None:
                        timeAfter = time()

            sleep(0.01)
