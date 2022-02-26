import time
from time import sleep
from typing import Union

import cv2

from baseclass.my_dataclass.tcr_scan_config import TcrScanConfig
from baseclass.my_enum.var_type import VarType
from util.pixel import getImgRectangle
from util.threadclass import ThreadClass


class DataScanner(ThreadClass, TcrScanConfig):
    digits: Union[int, None] = None
    conditions = []
    result: Union[str, int, None] = None
    config: TcrScanConfig = None

    def __init__(self, game, config):
        super().__init__()
        self.config = config
        self.config.apply(self)
        self.game = game

    def run(self):
        while not self.stopped:
            t = time.time()
            self.scanDatas()
            # if self.result not in ("", 0):
            #     print(self.name, self.result)
            # if time.time() - t > 0:
            #     print("fps: {}".format(time.time() - t))
            sleep(0.01)

    def conditionMeet(self):
        for condition in self.conditions:
            if condition[1] == "=":

                if len(self.game.dpc.getPickCoors(condition[0])) != condition[2]:
                    return False

        return True

    def scanDatas(self, screenshot=None):
        if screenshot is None:
            if self.game.screenShot is not None:
                screenshot = self.game.screenShot

        if self.region != "" and screenshot is not None:
            screenshot = self.game.regions.applyRegion(self.region, screenshot)

        if screenshot is not None:
            screenshot = getImgRectangle(screenshot, self.rectangle)
            cv2.imwrite("tmp/scans/{}.png".format(self.name), screenshot)
            if self.type == VarType.STRING:
                img, self.result = self.game.tcr.scanText(img=screenshot)
            elif self.type == VarType.INT:
                if self.digits is not None:
                    img, self.result = self.game.tcr.scanNumber(img=screenshot)
                else:
                    img, self.result = self.game.tcr.scanNumber(img=screenshot)

        return self.result
