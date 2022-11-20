import copy
from time import time, sleep

import cv2
import numpy as np

from baseclass.my_dataclass.mask_detection_config import MaskDetectionConfig
from util.rectangle import RectangleCoor
from util.threadclass import ThreadClass


class HsvFilter:
    pass


class DataPicker(ThreadClass, MaskDetectionConfig):
    lower_mask = None
    upper_mask = None
    conditions = None

    draw_offset = 2

    vision_filter = None
    results = {"countours": [], "coors": []}
    config: MaskDetectionConfig = None
    game: 'Game' = None

    def __init__(self, game, config):
        super().__init__()
        self.game = game
        self.config = config
        self.config.apply(self)
        print("create new", config)
        # if self.visionFilter is not None:
        #     self.hsv_filter = HsvFilter(*self.visionFilter)

        self.lower_mask = np.array(self.config.lower.as_list(), np.uint8)
        self.upper_mask = np.array(self.upper.as_list(), np.uint8)
        self.kernel = np.ones((self.kernel_size, self.kernel_size), "uint8")
        self.draw_size = 5

    def get_coors(self):
        return self.results['coors']

    def get_contours(self):
        return self.results['contours']

    # def checkCondition(self, tmpRectangle, condition):
    #     result = True
    #     if condition[1] == ">":
    #         if not getattr(tmpRectangle, condition[0]) > condition[2]:
    #             result = False
    #     elif condition[1] == ">=":
    #         if not getattr(tmpRectangle, condition[0]) >= condition[2]:
    #             result = False
    #     elif condition[1] == "<":
    #         if not getattr(tmpRectangle, condition[0]) < condition[2]:
    #             result = False
    #     elif condition[1] == "<=":
    #         if not getattr(tmpRectangle, condition[0]) <= condition[2]:
    #             result = False
    #     elif condition[1] == "in":
    #         if not (condition[2][0] <= getattr(tmpRectangle, condition[0]) <= condition[2][1]):
    #             result = False
    #     elif condition[1] == "out":
    #         if condition[2][0] <= getattr(tmpRectangle, condition[0]) <= condition[2][1]:
    #             result = False
    #     else:
    #         if not getattr(tmpRectangle, condition[0]) == condition[2]:
    #             result = False
    #     return result

    # def applyConditions(self, tmpRectangle, conditions):
    #     result = True
    #     for condition in conditions:
    #         if type(condition[0]) is list:
    #             if condition[1] == "or":
    #                 if not self.checkCondition(tmpRectangle, condition[0]) and not self.checkCondition(tmpRectangle, condition[2]):
    #                     result = False
    #             else:
    #                 if not self.checkCondition(tmpRectangle, condition[0]) or not self.checkCondition(tmpRectangle, condition[2]):
    #                     result = False
    #         else:
    #             if not self.checkCondition(tmpRectangle, condition):
    #                 result = False
    #
    #     return result

    def draw_screen_shot(self, screen_shot):
        if len(self.results['coors']) > 0:
            for coor in self.results['coors']:
                cv2.rectangle(screen_shot, (coor.x - self.draw_offset, coor.y - self.draw_offset),
                              (coor.x + coor.w + self.draw_offset, coor.y + coor.h + self.draw_offset),
                              self.draw_color.as_list(), self.draw_size)
                # if hasattr(self, "line"):
                #    center = centerCoor(coor)
                #    cv2.line(screen_shot, (self.line['x'], self.line['y']), (coor.centerX, coor.centerY), (0, 255, 0), 8)
        return screen_shot

    def scan_datas(self, screenshot=None, get="results"):

        if screenshot is None:
            if self.game.screen_shot is not None:
                screenshot = copy.deepcopy(self.game.screen_shot)
            else:
                return

        if screenshot is not None:
            if self.region is not None and self.region != "root":
                screenshot = self.game.regions.apply_region(self.region, screenshot=screenshot)
            # if self.visionFilter is not None:
            #     screenshot = self.game.vision.apply_hsv_filter(screenshot, self.hsv_filter)
            mask = cv2.inRange(screenshot, self.lower_mask, self.upper_mask)
            cv2.imwrite("tmp/test/{}.png".format(self.name), mask)
            # cv2.imwrite("tmp/test/{}.png".format(self.name), mask)

            # mask = cv2.dilate(mask, self.kernel)

            dont_know_why_its_exist = cv2.bitwise_and(screenshot, screenshot, mask=mask)

            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            self.results = {"contours": [], "coors": []}
            nb = 0
            for pic, contour in enumerate(contours):

                area = cv2.contourArea(contour)
                if self.max_found is not None:
                    if nb >= self.max_found:
                        break
                    if area > self.min_area:
                        x, y, w, h = cv2.boundingRect(contour)
                        tmp_rectangle = RectangleCoor(x=x, y=y, w=w, h=h)
                        # if self.region is not None:
                        #     regionCoor = self.game.regions.getRegion(self.region)
                        #     tmpRectangle.x += regionCoor.rectangle.x
                        #     tmpRectangle.y += regionCoor.rectangle.y
                        #     tmpRectangle.update()
                        # if self.applyConditions(tmpRectangle, self.conditions):
                        self.results['coors'].append(tmp_rectangle)
                        self.results['contours'].append(contour)

                        nb += 1

        if get == "screenshot":
            return self.draw_screen_shot(screenshot)
        elif get == "results":
            return self.results

    def run(self):
        self.loop_time = time()
        while not self.stopped:
            self.scan_datas()

            sleep(0.01)
