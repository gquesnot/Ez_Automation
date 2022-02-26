import copy
from time import sleep, time

import cv2
from pynput.mouse import Button

from baseclass.imagesave import ImageSave
from baseclass.regions import Regions
from baseclass.replayClass import Replay
from controllers.MenuController import MenuController
from controllers.configcontroller import ConfigController
from controllers.datapickercontroller import DataPickerController
from my_enum.game_state import GameState
from my_enum.game_type_state import GameTypeState
from my_enum.location_state import LocationState
from util.json_function import applyJsonConfig, getJson
from util.keyboardcontroller import KeyboardController
from util.tcr import Tcr
from util.threadclass import ThreadClass
from util.timer import Timer
from window.cv2windowcontroller import Cv2WindowController
from window.windowcapture import WindowCapture


class Game(ThreadClass):
    name = ""
    state = GameState.WAITING
    location = LocationState.START
    screenShot = None
    firstState = True
    freeze = False
    config : ConfigController=None



    def __init__(self, args):
        super().__init__()
        self.args = args
        if self.args.type == "record":
            self.typeState = GameTypeState.RECORD
        elif self.args.type == "replay":
            self.typeState = GameTypeState.REPLAY
        elif self.args.type == "play":
            self.typeState = GameTypeState.PLAY
        self.state = GameState.WAITING
        self.config = ConfigController(self)
        self.name = self.config.window.name
        if not self.isReplay():
            self.wc = WindowCapture(self, imgGrab=True)
            # self.ac = ActionController(self)
        else:
            self.timer = Timer()
            self.RC = Replay()
        self.regions = Regions(self)
        self.imSave = ImageSave(self)
        # self.vision = Vision(hsv=True)

        if not self.isPlaying():
            self.cv2Controller = Cv2WindowController(self, withRegion=self.args.show_region)
            # self.vision.init_control_gui()
        self.tcr = Tcr(self)
        self.dpc = DataPickerController(self)
        # self.trackerController = TrackerController(self)
        self.kc = KeyboardController(self)


        self.startClass()


    def initWaitingTime(self, duration=3):
        i = 3
        while i > 0:
            print(f"action in {i}s")
            sleep(1)
            i -= 1



    def doClick(self, hint, activate=False, isTest=False):
        self.initWaitingTime(duration=3)
        if hint in self.config.mouseActions:
            if activate:
                self.wc.activate()
                self.kc.moveClick(self.wc.getCenter(), delay=.1, timeBeetwen=.1 )

            self.kc.handleMouseAction(self.config.mouseActions.get(hint))

    def doKey(self, hint, activate = False, isTest=False):
        self.initWaitingTime(duration=3)
        if hint in self.config.keyboardActions:
            if activate:
                self.wc.activate()
                self.kc.moveClick(self.wc.getCenter(), delay=.1, timeBeetwen=.1 )
            self.kc.handleMouseAction(self.config.keyboardActions.get(hint))


    def toggleFreeze(self, double=False):
        self.freeze = not self.freeze
        if double:
            sleep(0.1)
            self.freeze = not self.freeze
        print(self.freeze)

    def startClass(self):
        pass


    # def createImage(self, comboHint):
    #     if self.screenShot is not None:
    #         return self.dpc.createImage(self.screenShot, comboHint)
    #     return None

    def stop(self):
        super().stop()
        cv2.destroyAllWindows()


        #self.dpc.stopAll()

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

    def run(self):
        while not self.stopped:

            if not self.freeze:
                if not self.isReplay():
                    self.screenShot = self.wc.getScreenshot()
                else:
                    self.screenShot = self.RC.getScreenshot()
            if self.screenShot is not None:
                #self.checkConfigState()
                if self.state == GameState.PLAYING:
                    print('scan wave: ', self.dpc.checkTcrScan('wave'))
                    print('check pixel evt1On: ', self.dpc.checkPixel("evt1On"))
                    print('check image evt1: ', self.dpc.checkImageMatch('evt1'))
                    print('check mask greenBar: ', self.dpc.checkMaskDetection('greenBar'))
                    print('do action closeUp')
                    self.doClick('closeUpgrade')
                    self.doKey('up')
            sleep(0.01)
