import cv2

from util.pixel import get_img_rectangle


class Regions:

    def __init__(self, game):
        self.game = game

    def get_region(self, hint):
        if hint in self.all():
            return self.game.config.regions.get(hint)
        return None

    def all(self):
        return self.game.config.regions.dict

    def get_coor_by_region(self, hint):
        region = self.get_region(hint)
        if region is not None:
            return region.rectangle
        return None

    def apply_region(self, hint, screenshot=None, with_ratio=False):
        if screenshot is None:
            screenshot = self.game.screen_shot
        region = self.get_region(hint)
        if region is not None and region.rectangle.x != 0 and region.rectangle.y != 0:
            screenshot = get_img_rectangle(screenshot, region.rectangle)
            if with_ratio != 1:
                screenshot = cv2.resize(screenshot, (
                    int(region.rectangle.w * region.ratio), int(region.rectangle.h * region.ratio)))
            return screenshot
        return screenshot
