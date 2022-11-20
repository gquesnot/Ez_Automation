import copy
from time import sleep, time
from typing import Any

import cv2

from baseclass.action_listener import ActionListener
from baseclass.action_player import ActionReplay
from baseclass.imagesave import ImageSave
from baseclass.my_enum.game_state import GameState
from baseclass.my_enum.game_type_state import GameTypeState
from baseclass.my_enum.location_state import LocationState
from baseclass.regions import Regions
from baseclass.replayClass import Replay
from controllers.configcontroller import ConfigController
from controllers.datapickercontroller import DataPickerController
from ia.ia import IA
from util.keyboardcontroller import KeyboardController
from util.tcr import Tcr
from util.threadclass import ThreadClass
from util.timer import Timer
from window.cv2windowcontroller import Cv2WindowController
from window.windowcapture import WindowCapture


class Game(ThreadClass):
    name: str = ""
    state: GameState = GameState.WAITING
    location: LocationState = LocationState.START
    screen_shot: Any = None
    first_state: bool = True
    config: ConfigController = None
    type_state: GameTypeState = GameTypeState.RECORD
    app: 'App' = None
    wc: WindowCapture = None
    replay: Replay = None
    im_save: ImageSave = None
    tcr: Tcr = None
    kc: KeyboardController = None
    dpc: DataPickerController = None
    cv2_controller: Cv2WindowController = None
    timer: Timer = None
    regions: Regions = None
    action_listener: ActionListener = None
    action_replay: ActionReplay = None
    ia: IA = None

    def __init__(self):
        super().__init__()

        self.config = ConfigController(self)
        self.name = self.config.window.name

        self.wc = WindowCapture(self, img_grab=True)
        # self.ac = ActionController(self)

        self.timer = Timer()
        self.RC = Replay()
        self.regions = Regions(self)
        self.im_save = ImageSave(self)
        self.action_listener = ActionListener(self)
        self.action_replay = ActionReplay(self)
        # self.vision = Vision(hsv=True)

        if not self.is_playing():
            self.cv2_controller = Cv2WindowController(self)
            # self.vision.init_control_gui()
        self.tcr = Tcr(self)
        self.dpc = DataPickerController(self)
        # self.trackerController = TrackerController(self)
        self.kc = KeyboardController(self)
        self.ia = IA(self)

        self.start_class()

    def init_waiting_time(self):
        i = 3
        while i > 0:
            print(f"action in {i}s")
            sleep(1)
            i -= 1

    def do_click(self, hint, activate=False, is_test=False):
        if is_test:
            self.init_waiting_time()
        if hint in self.config.mouse_actions.dict:
            if activate:
                self.wc.activate()
                self.kc.move_click(self.wc.get_center(), delay=.1, time_beetwen=.1)

            self.kc.handle_mouse_action(self.config.mouse_actions.get(hint))

    def do_key(self, hint, activate=False, is_test=False):
        if is_test:
            self.init_waiting_time()
        if hint in self.config.keyboard_actions.dict:
            if activate:
                self.wc.activate()
                self.kc.move_click(self.wc.get_center(), delay=.1, time_beetwen=.1)
            self.kc.handle_mouse_action(self.config.keyboard_actions.get(hint))

    def get_screenshot_copy(self):
        if self.screen_shot is not None:
            return copy.deepcopy(self.screen_shot)
        else:
            return None

    def start_class(self):
        self.ia.start()

    # def createImage(self, comboHint):
    #     if self.screenShot is not None:
    #         return self.dpc.createImage(self.screenShot, comboHint)
    #     return None

    def stop(self):
        super().stop()
        cv2.destroyAllWindows()

        # self.dpc.stopAll()

    def set_global_state(self, state):
        self.lock.acquire()
        self.type_state = state
        self.lock.release()

    def set_name(self, name):
        self.name = name

    def set_state(self, state, first_state=False):
        print("NEW GAME STATE: " + state.name)
        if self.first_state or first_state:
            print("FIRST STATE SLEEPING 2s")
            # self.kc.moveClick(self.wc.getCenter())
            sleep(2)
            self.first_state = False
        self.lock.acquire()
        self.state = state
        self.lock.release()

    def is_replay(self):
        return self.type_state == GameTypeState.REPLAY

    def is_record(self):
        return self.type_state == GameTypeState.RECORD

    def is_playing(self):
        return self.type_state == GameTypeState.PLAY

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

    def add_app(self, app):
        self.app = app

    def run(self):
        time_after = None
        time_before = None
        while not self.stopped:
            if self.config.showFps:
                time_before = time()
            if not self.config.freeze:
                if not self.is_replay():
                    self.screen_shot = self.wc.get_screenshot()
                else:
                    self.screen_shot = self.RC.get_screenshot()
                self.dpc.check_config_has_mask_test()
            if self.screen_shot is not None:
                # code Here
                if self.state == GameState.PLAYING:
                    print('scan wave: ', self.dpc.check_tcr_scan('wave'))
                    print('check pixel evt1On: ', self.dpc.check_pixel("evt1On"))
                    print('check image evt1: ', self.dpc.check_image_match('evt1'))
                    print('check mask greenBar: ', self.dpc.check_mask_detection('greenBar'))
                    print('do action closeUp')
                    self.do_click('closeUpgrade')
                    self.do_key('up')
                    self.action_replay.play('upgradeAll')
            if self.config.showFps:
                if self.screen_shot is not None:
                    if time_after is not None and time_before is not None and abs(
                            time_before - time_after) > 1 and time_after != time_before:
                        time_after = time()

                        self.app.view.fpsCounter.set("FPS: {:.2f}".format(1 / (time_after - time_before)))
                    elif time_after is None:
                        time_after = time()

            sleep(0.01)
