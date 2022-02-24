import json

import cv2

from app.my_dataclasses import RegionConfigs
from util.json_function import applyJsonConfig, getJson
from util.pixel import getImgRectangle


class Regions(RegionConfigs):

    def __init__(self, game):
        self.game = game
        self.game.config.apply(self, 'regions')

    def getRegion(self, hint):
        if hint in self.dict:
            return self.dict[hint]
        return None


    def getCoorByRegion(self, hint, coor):
        region = self.get(hint)
        if region is not None:
            return region.rectangle
        return None

    def applyRegion(self, hint, screenshot=None, withRatio=False):
        if screenshot is None:
            screenshot = self.game.screenShot
        region = self.get(hint)
        if region is not None:
            screenshot = getImgRectangle(screenshot, region.rectangle)
            if withRatio != 1:
                screenshot = cv2.resize(screenshot, (int(region.rectangle.w * region.ratio), int(region.rectangle.h * region.ratio)))
        return screenshot
