import json
import os
from time import time
from typing import Tuple

import cv2
import numpy as np

from baseclass.my_dataclass.coor import Coor
from baseclass.my_dataclass.pixel import Pixel
from baseclass.my_dataclass.rectangle import Rectangle
from util.pixel import get_img_rectangle


class ImageSave:
    def __init__(self, game):
        self.game = game
        self.img = None
        self.draw_img = None
        self.mask_img = None
        self.screen_shot = None
        self.processed_img = None
        self.img_to_pick = "img"
        self.click_info = False

        self.click_list = []

    def save_image(self, rectangle, path, name):
        if rectangle is not None:
            if not os.path.exists(path):
                os.makedirs(path)
            if rectangle['region'] != "root":
                img = self.game.regions.applyRegion(rectangle['region'])
            else:
                img = self.game.screen_shot
            img = get_img_rectangle(img, rectangle)
            if img is not None:
                cv2.imwrite(f"{path}/{name}", img)
            return img
        return None

    def update(self, hint, screen_shot):
        setattr(self, hint, screen_shot)

    def reset(self):
        self.click_list = []

    def get_by_hint(self, hint) -> Tuple[Rectangle | Pixel | Coor | None, None | str]:
        region = None
        res = None
        if hint == "pixel" or hint == "mask" or hint == "coor":
            click = self.get_coor()
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
            base_rectangle = self.get_rectangle()
            if base_rectangle is not None:
                region = base_rectangle['region']
                rectangle = Rectangle.from_dict({})
                rectangle.x = base_rectangle['x']
                rectangle.y = base_rectangle['y']
                rectangle.w = base_rectangle['w']
                rectangle.h = base_rectangle['h']
                return rectangle, region

        if hint == 'pixel':
            res = Pixel.from_dict({})

        elif hint == 'rectangle' or hint == 'image':
            res = Rectangle.from_dict({})
        elif hint == 'coor':
            res = Coor.from_dict({})

        return res, region

    def add_click(self, click):
        if len(self.click_list) == 2:
            self.click_list.pop()
        self.click_list.append(click)

    def get_coor(self):
        if len(self.click_list) != 0:
            return self.click_list[0]
        else:
            return None

    def get_mask(self):
        click = self.get_coor()
        res = {}
        if click is not None:
            res['region'] = click['region']
            res['upper'] = {"r": click['color']["r"] + 15, "g": click['color']["g"] + 15, "b": click['color']["b"] + 30}
            res['lower'] = {"r": click['color']["r"] - 15, "g": click['color']["g"] - 15, "b": click['color']["b"] - 30}
            return res
        return None

    def save_rectangle(self):
        rectangle = self.get_rectangle()
        if rectangle is not None:
            if 'region' in rectangle and rectangle['region'] != "root":
                img = self.game.regions.applyRegion(rectangle['region'])
            else:
                img = self.game.screen_shot
            img = get_img_rectangle(img, rectangle)
            print("rectangle: \n", json.dumps(rectangle, indent=4))
            cv2.imwrite("tmp/clipped/{}_region_{}_x_{}_y_{}_w_{}_h_{}.png".format(int(time()), rectangle['region'],
                                                                                  rectangle['x'], rectangle['y'],
                                                                                  rectangle["w"], rectangle['h']), img)

    def get_rectangle(self) -> dict | None:

        if len(self.click_list) == 2:
            res = {
                "x": self.click_list[0]['x'],
                "y": self.click_list[0]['y'],
                "w": abs(self.click_list[1]['x'] - self.click_list[0]['x']),
                "h": abs(self.click_list[1]['y'] - self.click_list[0]['y']),
                "region": self.click_list[0]['region']
            }
            if res['w'] == 0:
                res['w'] = 5
            return res
        else:
            return None

    def save_screen_shot(self):
        if self.game.screen_shot is not None:
            cv2.imwrite(f"tmp/screenshot/{int(time())}.png", self.game.screen_shot)

    def pick_color(self, event, x, y, other, params=None):
        if event == cv2.EVENT_LBUTTONDOWN:
            img_ = getattr(self, self.img_to_pick)
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
                self.add_click(
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
                if self.click_info:
                    print("----\nx: {}\ny: {}\npixel: {}\nlower: {}\nupper: {}".format(x, y,
                                                                                       "[" + ", ".join(
                                                                                           str(v) for v in pixel) + "]",
                                                                                       "[" + ", ".join(
                                                                                           str(v) for v in lower) + "]",
                                                                                       "[" + ", ".join(
                                                                                           str(v) for v in
                                                                                           upper) + "]"))
                self.mask_img = cv2.inRange(img_, lower, upper)
