from time import time

import cv2
import pytesseract

from util.pixel import getImgRectangle, applyThresh, applyRegion, applySave, perform_ocr

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


class Tcr:
    def __init__(self, game):
        self.game = game
        self.textConfig = r'-l eng --tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --oem 3 --psm 8'
        self.numberConfig = r'--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 6 outputbase digits'

    def initScan(self, region, save):
        img = self.game.screenShot
        img = applyRegion(img, region)
        applySave(img, save)
        return img

    def scanText(self, region=None, save=None, img=None):
        if img is None:
            img = self.initScan(region, save)
        else:
            img = perform_ocr(img)
        text = pytesseract.image_to_string(img, config=self.textConfig).replace("\n", "").replace("\x0c", "")
        return img, text

    def scanNumber(self, region=None, save=None, img=None, maxDigit=None):
        if img is None:
            img = self.initScan(region, save)
        else:
            img = perform_ocr(img)
        text = pytesseract.image_to_string(img, config=self.numberConfig) \
            .replace("\n", "") \
            .replace("\x0c", "") \
            .replace(" ", "")
        if maxDigit is not None:
            if len(text) > maxDigit:
                text = text[:2]

        if text == "":
            return None, None
        return img, int(text)
