import copy
from time import time, sleep

import cv2
import numpy as np

from app.my_dataclasses import MaskDetectionConfig
from util.pixel import centerCoor
from util.rectangle import RectangleCoor
from util.threadclass import ThreadClass


class HsvFilter:
    pass


class DataPicker(ThreadClass, MaskDetectionConfig):
    lowerMask = None
    upperMask = None
    conditions = None

    drawOffset = 0

    visionFilter = None
    results = {"countours": [], "coors": []}
    config: MaskDetectionConfig = None
    game: 'Game' = None

    def __init__(self, game, config):
        super().__init__()
        self.game = game
        self.config = config
        self.config.apply(self)
        # if self.visionFilter is not None:
        #     self.hsv_filter = HsvFilter(*self.visionFilter)

        self.lowerMask = np.array(self.config.lower.asList(), np.uint8)
        self.upperMask = np.array(self.upper.asList(), np.uint8)
        self.kernel = np.ones((self.kernelSize, self.kernelSize), "uint8")

    def getCoors(self):
        return self.results['coors']

    def getContours(self):
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

    # def drawScreenShot(self, screenShot):
    #     if len(self.results['coors']) > 0:
    #         for coor in self.results['coors']:
    #             cv2.rectangle(screenShot, (coor.x - self.drawOffset, coor.y - self.drawOffset),
    #                           (coor.x + coor.w + self.drawOffset, coor.y + coor.h + self.drawOffset),
    #                           self.drawColor, self.drawSize)
    #             if hasattr(self, "line"):
    #                 center = centerCoor(coor)
    #                 cv2.line(screenShot, (self.line['x'], self.line['y']), (coor.centerX, coor.centerY), (0, 255, 0), 8)
    #     return screenShot

    def scanDatas(self, screenshot=None):
        if screenshot is None:
            if self.game.screenShot is not None:
                screenshot = copy.deepcopy(self.game.screenShot)
            else:
                return

        if screenshot is not None:
            if self.region is not None and self.region != "root":
                screenshot = self.game.regions.applyRegion(self.region, screenshot=screenshot)
            # if self.visionFilter is not None:
            #     screenshot = self.game.vision.apply_hsv_filter(screenshot, self.hsv_filter)

            mask = cv2.inRange(screenshot, self.lowerMask, self.upperMask)
            cv2.imwrite("tmp/test/{}.png".format(self.name), mask)
            # cv2.imwrite("tmp/test/{}.png".format(self.name), mask)

            # mask = cv2.dilate(mask, self.kernel)

            dontKnowWhyItsExist = cv2.bitwise_and(screenshot, screenshot, mask=mask)

            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            result = {"contours": [], "coors": []}
            nb = 0
            for pic, contour in enumerate(contours):

                area = cv2.contourArea(contour)
                if self.maxFound is not None:
                    if nb >= self.maxFound:
                        break
                    if area > self.minArea:
                        x, y, w, h = cv2.boundingRect(contour)
                        tmpRectangle = RectangleCoor(x=x, y=y, w=w, h=h)
                        # if self.region is not None:
                        #     regionCoor = self.game.regions.getRegion(self.region)
                        #     tmpRectangle.x += regionCoor['x']
                        #     tmpRectangle.y += regionCoor['y']
                        #     tmpRectangle.update()
                        #if self.applyConditions(tmpRectangle, self.conditions):
                        result['coors'].append(tmpRectangle)
                        result['contours'].append(contour)
                        nb += 1
            self.results = result
        return self.results

    def run(self):
        self.loop_time = time()
        while not self.stopped:
            self.scanDatas()

            sleep(0.01)
