from typing import Dict

from baseclass.my_dataclass.pixel_config import PixelConfig
from baseclass.my_enum.condition_type import ConditionType
from baseclass.datapicker import DataPicker
from baseclass.datascanner import DataScanner
from baseclass.matchimages import MatchImages

from util.pixel import comparePixel


class DataPickerController:
    pickDict: Dict[str, DataPicker] = {}
    scanDict: Dict[str, DataScanner] = {}
    pixelDict: Dict[str, PixelConfig] = {}
    imgsScanDict: Dict[str, MatchImages] = {}

    game = None

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.loadMaskDetections()
        self.loadTcrScans()
        self.loadMatchImages()
        self.loadPixels()

    def loadMaskDetections(self):
        self.pickDict = {}
        for maskName, maskDetection in self.game.config.maskDetections.dict.items():
            dp = DataPicker(self.game, maskDetection)
            self.pickDict[maskName] = dp

    def loadPixels(self):

        self.pixelDict = self.game.config.pixels.dict

    def loadTcrScans(self):
        self.scanDict = {}
        for screenInfoName, screenInfo in self.game.config.tcrScans.dict.items():
            ds = DataScanner(self.game, screenInfo)
            self.scanDict[screenInfoName] = ds

    def loadMatchImages(self):
        self.imgsScanDict = {}
        for matchImagesName, matchImagesInfo in self.game.config.matchImages.dict.items():
            mi = MatchImages(self.game, matchImagesInfo)
            self.imgsScanDict[matchImagesName] = mi

    def checkPixel(self, hint):
        if self.game.screenShot is not None:
            screenShot = self.game.screenShot
            if hint in self.pixelDict:

                match = False
                for pixel in self.pixelDict[hint].pixels:
                    newScreenshot = screenShot
                    if pixel.region != "root":
                        newScreenshot = self.game.regions.applyRegion(pixel.region, screenShot)
                    if comparePixel(newScreenshot, pixel):
                        match = True
                        if self.pixelDict[hint].type == ConditionType.OR:
                            return True

                    elif self.pixelDict[hint].type == ConditionType.AND:
                        return False
                return match
        return False

    def checkTcrScan(self, hint):
        if hint in self.scanDict:
            return self.scanDict[hint].scanDatas()
        return None

    def checkMaskDetection(self, hint):
        if hint in self.pixelDict:
            return self.pickDict[hint].scanDatas()
        return None

    def checkImageMatch(self, hint):
        if hint in self.imgsScanDict:
            return self.imgsScanDict[hint].scanDatas()
        return None

    # def createImage(self, screenshot, comboHint):
    #     height, width = screenshot.shape[:2]
    #     newImg = np.zeros((height, width, 3), np.uint8)
    #     hasRegions = "+" in comboHint
    #     if hasRegions:
    #         regionElem = comboHint.split('+')
    #         allHint = regionElem.pop(0)
    #         tmpRegionList = regionElem[0].split(' ')
    #     else:
    #         allHint = comboHint
    #         regionElem = []
    #         tmpRegionList = []
    #     hintList = allHint.split(' ')
    #
    #     if len(tmpRegionList) > 0 and not self.game.isReplay():
    #         for region in tmpRegionList:
    #             tmpRegion = self.game.regions.getRegion(region)
    #             rR = (tmpRegion['ratio'] - 1) / 2
    #
    #             rY = int(tmpRegion['y'] - tmpRegion['h'] * rR)
    #
    #             rX = int(tmpRegion['x'] - tmpRegion['w'] * rR)
    #
    #             rH = int(tmpRegion['h'] * tmpRegion['ratio'])
    #             rW = int(tmpRegion['w'] * tmpRegion['ratio'])
    #
    #             if rY + rH > height:
    #                 rY -= int(tmpRegion['h'] * rR)
    #             elif rY < 0:
    #                 rY += int(tmpRegion['h'] * rR)
    #             if rX + rW > width:
    #                 rX -= int(tmpRegion['w'] * rR)
    #             elif rX < 0:
    #                 rX += int(tmpRegion['w'] * rR)
    #
    #             newImg[rY:rY + rH, rX:rX + rW] = cv2.resize(self.game.regions.applyRegion(region, screenshot=screenshot),
    #                                                         (rW, rH))
    #     for k, v in self.dataPickList.items():
    #         if v.name in hintList:
    #             coors = v.getCoors()
    #             if len(coors) > 0:
    #                 drawScreenShot = v.drawScreenShot(newImg)
    #     return newImg
