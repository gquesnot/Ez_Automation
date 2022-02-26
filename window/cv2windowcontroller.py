import cv2

from util.json_function import applyJsonConfig


class Cv2WindowController:
    windowList = {}
    gameName = ""
    cv2RegionList = {}
    refreshRegion: bool = False

    def __init__(self, game):

        self.game = game
        self.regions = self.game.regions
        applyJsonConfig(self, "cv2")
        self.list = [k for k, v in self.windowList.items()]
        for k, v in self.windowList.items():
            v['name'] = k + " " + self.gameName
        self.createWindows(self.windowList)
        self.setMouseCallBack("root", self.game.imSave.pick_color)

    def clearRegions(self):
        if len(self.cv2RegionList) != 0:
            for k, v in self.cv2RegionList.items():
                cv2.destroyWindow(v['name'])
        self.cv2RegionList = {}

    def loadRegions(self):
        self.clearRegions()

        for regionName, region in self.regions.all().items():
            self.cv2RegionList[regionName] = {
                "name": "Regions " + regionName,
                "coor": [-1080, 400],
                "resize": (int(region.rectangle.w * region.ratio), int(region.rectangle.h * region.ratio)),
            }
        if self.game.config.showRegions:
            self.createWindows(self.cv2RegionList, regions=True)
        self.refreshRegion = False

    def getWindowByHint(self, hint):
        if hint in self.list:
            return self.windowList[hint]
        elif hint in self.cv2RegionList:
            return self.cv2RegionList[hint]
        else:
            return False

    def applyScreenShotToWindow(self, screenShot, hint):
        if self.game.wc.isLoaded:
            window = self.getWindowByHint(hint)
            if window and screenShot is not None and self.game.wc.w != 0:
                try:
                    x, y, z = screenShot.shape
                except:
                    try:
                        x, y = screenShot.shape
                        z = 3
                    except:
                        return
                if not x or not y:
                    return
                if "resize" not in window:
                    if not self.game.isReplay():
                        window['resize'] = (
                            int(self.game.wc.w * window['ratio']), int(self.game.wc.h * window['ratio']))
                    else:
                        window['resize'] = (
                            int(self.game.RC.w * window['ratio']), int(self.game.RC.h * window['ratio']))
                cv2.imshow(window['name'], cv2.resize(screenShot, window['resize']))

    def createWindows(self, windowDic, regions=False):
        for k, v in windowDic.items():
            cv2.namedWindow(v['name'])
            if regions:
                self.setMouseCallBack(k, self.game.imSave.pick_color)
            # cv2.moveWindow(v['name'], *v['coor'])

    def setMouseCallBack(self, hint, fn):
        window = self.getWindowByHint(hint)
        if window:
            cv2.setMouseCallback(window['name'], fn, param={"window": hint})

    def feedRegion(self, processed_image):
        if self.game.config.showRegions:
            if len(self.cv2RegionList) == 0:
                self.loadRegions()
            for regionName, cv2Region in self.cv2RegionList.items():
                if self.refreshRegion:
                    self.loadRegions()

                newImg = self.regions.applyRegion(regionName, screenshot=processed_image)
                if newImg is not None:
                    cv2.imshow(cv2Region['name'], cv2.resize(newImg, cv2Region["resize"]))
