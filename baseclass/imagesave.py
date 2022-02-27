import json
import os
from time import time

import cv2
import numpy as np

from baseclass.my_dataclass.coor import Coor
from baseclass.my_dataclass.pixel import Pixel
from baseclass.my_dataclass.rectangle import Rectangle
from util.pixel import getImgRectangle


class ImageSave:
    def __init__(self, game):
        self.game = game
        self.img = None
        self.draw_img = None
        self.mask_img = None
        self.screenShot = None
        self.processed_img = None
        self.imgToPick = "img"
        self.clickInfo = False

        self.clickList = []

    def saveImage(self, rectangle, path, name):
        if rectangle is not None:
            if not os.path.exists(path):
                os.makedirs(path)
            if rectangle['region'] != "root":
                img = self.game.regions.applyRegion(rectangle['region'])
            else:
                img = self.game.screenShot
            img = getImgRectangle(img, rectangle)
            if img is not None:
                cv2.imwrite(f"{path}/{name}", img)
            return img
        return None

    def update(self, hint, screenShot):
        setattr(self, hint, screenShot)

    def reset(self):
        self.clickList = []

    def getByHint(self, hint):
        region = None
        if hint == "pixel" or hint == "mask" or hint == "coor":
            click = self.getCoor()
            if click is not None:
                region = click['region']
                if hint == "pixel":
                    pixel = Pixel.from_dict({})
                    pixel.coor.x = click['x']
                    pixel.coor.y = click['y']
                    pixel.region = click['region']
                    pixel.color.r = click['color'][0]
                    pixel.color.g = click['color'][1]
                    pixel.color.b = click['color'][2]
                    return pixel, region
                elif hint == 'mask':
                    pass
                elif hint == 'coor':
                    coor = Coor.from_dict({})
                    coor.x = click['x']
                    coor.y = click['y']
                    return coor, region
        else:
            rectangle = self.getRectangle()
            if rectangle is not None:
                region = rectangle['region']
                rectangle = Rectangle.from_dict({})
                rectangle.x = rectangle['x']
                rectangle.y = rectangle['y']
                rectangle.w = rectangle['w']
                rectangle.h = rectangle['h']
                return rectangle, region

        if hint == 'pixel':
            res = Pixel.from_dict({})

        elif hint == 'rectangle' or hint == 'image':
            res = Rectangle.from_dict({})
        elif hint == 'coor':
            res = Coor.from_dict({})

        return res, region

    def addClick(self, click):
        if len(self.clickList) == 2:
            self.clickList.pop()
        self.clickList.append(click)

    def getCoor(self):
        if len(self.clickList) != 0:
            return self.clickList[0]
        else:
            return None

    def getMask(self):
        click = self.getCoor()
        res= {}
        if click is not None:
            res['region'] = click['region']
            res['upper'] = {"r":click['color']["r"]+15, "g":click['color']["g"]+15, "b":click['color']["b"]+30}
            res['lower'] = {"r":click['color']["r"]-15, "g":click['color']["g"]-15, "b":click['color']["b"]-30}
            return res
        return None


    def saveRectangle(self):
        rectangle = self.getRectangle()
        if rectangle is not None:
            if 'region' in rectangle and rectangle['region'] != "root":
                img = self.game.regions.applyRegion(rectangle['region'])
            else:
                img = self.game.screenShot
            img = getImgRectangle(img, rectangle)
            print("rectangle: \n", json.dumps(rectangle, indent=4))
            cv2.imwrite("tmp/clipped/{}_region_{}_x_{}_y_{}_w_{}_h_{}.png".format(int(time()), rectangle['region'],rectangle['x'], rectangle['y'],
                                                                       rectangle["w"], rectangle['h']), img)

    def getRectangle(self):

        if len(self.clickList) == 2:
            res = {
                "x": self.clickList[0]['x'],
                "y": self.clickList[0]['y'],
                "w": abs(self.clickList[1]['x'] - self.clickList[0]['x']),
                "h": abs(self.clickList[1]['y'] - self.clickList[0]['y']),
                "region": self.clickList[0]['region']
            }
            if res['w'] == 0:
                res['w'] = 5
            return res
        else:
            return None

    def saveScreenShot(self):
        if self.game.screenShot is not None:
            cv2.imwrite(f"tmp/screenshot/{int(time())}.png", self.game.screenShot)

    def pick_color(self, event, x, y, other, params=None):
        if event == cv2.EVENT_LBUTTONDOWN:
            img_ = getattr(self, self.imgToPick)
            if type(params) is dict:
                if params['window'] != "root":
                    img_ = self.game.regions.applyRegion(params['window'])
            img_ = img_[..., :3]

            r = 15
            g = 15
            b = 30

            if img_ is not None:
                if y > img_.shape[0]:
                    y = img_.shape[0] - 1
                elif y < 0:
                    y = 0
                if x > img_.shape[1]:
                    x = img_.shape[1] - 1
                elif x < 0:
                    x = 0

                pixel = img_[y, x]
                self.addClick(
                    {
                        "x": x,
                        "y": y,
                        'region': "root" if params['window'] == 'main' else params['window'],
                        'color': {"r": int(pixel[0]), "g": int(pixel[1]), "b": int(pixel[2])}
                    }
                )
                # you might want to adjust the ranges(+-10, etc):
                upper = np.array([pixel[0] + r, pixel[1] + g, pixel[2] + b])
                lower = np.array([pixel[0] - r, pixel[1] - g, pixel[2] - b])
                if self.clickInfo:
                    print("----\nx: {}\ny: {}\npixel: {}\nlower: {}\nupper: {}".format(x, y,
                                                                                       "[" + ", ".join(
                                                                                           str(v) for v in pixel) + "]",
                                                                                       "[" + ", ".join(
                                                                                           str(v) for v in lower) + "]",
                                                                                       "[" + ", ".join(
                                                                                           str(v) for v in
                                                                                           upper) + "]"))
                self.mask_img = cv2.inRange(img_, lower, upper)
