from time import time

import cv2
import numpy as np

import skimage.color
import skimage.segmentation
import skimage.filters
import skimage.morphology
import skimage.util
import skimage.transform
import skimage.measure
import skimage.io

from baseclass.my_dataclass.pixel import Pixel
from baseclass.my_dataclass.rectangle import Rectangle


def centerCoor(data, diff=None):
    if diff is None:
        diff = {"x": 0, "y": 0}
    x, y, w, h = (v for v in data.values())

    x = int(x + w / 2) + diff["x"]
    y = int(y + h / 2) + diff["y"]
    return {"x": x if x > 0 else 0, "y": y if y > 0 else 0}


def applyRegion(img, region):
    return perform_ocr(getImgRectangle(img, region)) if region is not None else img


def applySave(img, save):
    if save is not None:
        tmp = save.split("_")[0]
        print("testimg\\{0}\\{1}_{2}.jpg".format(tmp, save, str(time())))
        cv2.imwrite("testimg\\{0}\\{1}_{2}.jpg".format(tmp, save, str(time())), img)


def comparePixel(screenShot, pixel: Pixel):
    if screenShot is not None:
        myPixel = screenShot[pixel.coor.y, pixel.coor.x]
        # get screensize of screenshot
        # print("{} vs {} on {}".format(pixel.coor, pixel.color.asList(), screenSize))
        if abs(myPixel[0] - pixel.color.r) <= pixel.tolerance:
            if abs(myPixel[1] - pixel.color.g) <= pixel.tolerance:
                if abs(myPixel[2] - pixel.color.b) <= pixel.tolerance:
                    return True
    return False


def perform_ocr(image, scale=10, order=5, horizontal_closing=10, vertical_closing=5):
    image = skimage.color.rgb2gray(image)
    image = skimage.transform.resize(
        image,
        (image.shape[0] * scale, image.shape[1] * scale),
        mode="edge",
        order=order
    )

    image = image > skimage.filters.threshold_otsu(image)

    black_pixel_count = image[image == 0].size
    white_pixel_count = image[image == 1].size

    if black_pixel_count > white_pixel_count:
        image = skimage.util.invert(image)

    image = skimage.morphology.closing(image, skimage.morphology.rectangle(1, horizontal_closing))
    image = skimage.morphology.closing(image, skimage.morphology.rectangle(vertical_closing, 1))

    image = skimage.util.img_as_ubyte(image)

    return image  # Image.fromarray(image)


def applyThresh(srcImg):
    img = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (0, 0), fx=2, fy=2)
    kernel = np.ones((2, 2), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    (thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    return img


def getImgRectangle(img, rectangle):
    if type(rectangle) is Rectangle:
        cropped = img[rectangle.y:rectangle.y + rectangle.h, rectangle.x:rectangle.x + rectangle.w]
    else:
        cropped = img[rectangle['y']: rectangle['y'] + rectangle['h'], rectangle['x']: rectangle['x'] + rectangle['w']]
    return cropped
