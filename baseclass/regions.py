import cv2

from util.pixel import getImgRectangle


class Regions:

    def __init__(self, game):
        self.game = game

    def getRegion(self, hint):
        if hint in self.all():
            return self.game.config.regions.get(hint)
        return None

    def all(self):
        return self.game.config.regions.dict

    def getCoorByRegion(self, hint):
        region = self.getRegion(hint)
        if region is not None:
            return region.rectangle
        return None

    def applyRegion(self, hint, screenshot=None, withRatio=False):
        if screenshot is None:
            screenshot = self.game.screenShot
        region = self.getRegion(hint)
        if region is not None:
            screenshot = getImgRectangle(screenshot, region.rectangle)
            if withRatio != 1:
                screenshot = cv2.resize(screenshot, (
                    int(region.rectangle.w * region.ratio), int(region.rectangle.h * region.ratio)))
        return screenshot
