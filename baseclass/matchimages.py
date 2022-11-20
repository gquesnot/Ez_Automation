import time
from time import sleep

import cv2

from baseclass.my_dataclass.image_match_config import ImageMatchConfig
from util.threadclass import ThreadClass


class MatchImages(ThreadClass, ImageMatchConfig):
    tolerance: float = .1

    config: ImageMatchConfig = None

    def __init__(self, game, config):
        super().__init__()
        self.game = game
        self.config = config
        self.config.apply(self)
        self.load_images()

    def load_images(self):
        for img in self.images:
            img.image = cv2.imread(img.path)

    def run(self):
        while not self.stopped:
            t = time.time()
            self.scan_datas()

            sleep(0.01)

    def image_match_screen_shot(self, img, screenshot=None):
        result = cv2.matchTemplate(img, screenshot, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if min_val < self.tolerance:
            return min_loc
        return False

    def scan_datas(self, screenshot=None):
        if screenshot is None:
            if self.game.screen_shot is not None:
                screenshot = self.game.screen_shot

        if screenshot is not None:
            for img in self.images:
                if img.region not in ("", "root"):
                    tmp_image = self.game.regions.applyRegion(img.region, screenshot)
                else:
                    tmp_image = screenshot
                result = self.image_match_screen_shot(img.image, tmp_image)
                if result is not False:
                    return result

        return False
