import os
import time
from time import sleep
from typing import Union, List

import cv2

from app.my_dataclasses import ImageMatchConfig, ImageMatchItemConfig
from util.threadclass import ThreadClass


class MatchImages(ThreadClass, ImageMatchConfig):
    tolerance: float = .1

    config: ImageMatchConfig = None

    def __init__(self, game, config):
        super().__init__()
        self.game = game
        self.config = config
        self.config.apply(self)
        self.loadImages()

    def loadImages(self):
        for img in self.images:
            img.image = cv2.imread(img.path)

    def run(self):
        while not self.stopped:
            t = time.time()
            self.scanDatas()
            # if self.result not in ("", 0):
            #     print(self.name, self.result)
            # if time.time() - t > 0:
            #     print("fps: {}".format(time.time() - t))
            sleep(0.01)

    def imageMatchScreenShot(self, img, screenshot=None, ):
        result = cv2.matchTemplate(img, screenshot, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if min_val < self.tolerance:
            return min_loc
        return False

    def scanDatas(self, screenshot=None):
        if screenshot is None:
            if self.game.screenShot is not None:
                screenshot = self.game.screenShot

        if screenshot is not None:
            for img in self.images:
                if img.region not in ("", "root"):
                    tmpImage = self.game.regions.applyRegion(img.region, screenshot)
                else:
                    tmpImage = screenshot
                result = self.imageMatchScreenShot(img.image, tmpImage)
                if result is not False:
                    return result

        return False
