import os
import cv2


class Replay:
    i = 0
    di = 0
    h = 0
    w = 0
    directoryList = ["tmp/record/"] #['tmp/cliped/',
    currentDir = []

    def __init__(self):
        self.directory = self.directoryList[self.di]
        self.fileNames = os.listdir(self.directory)

    def prev(self):
        self.i -= 1
        if self.i < 0:
            self.i = len(self.fileNames) - 1
        return self.getScreenshot()

    def saveCoor(self, screenShot):
        self.h, self.w, channels = screenShot.shape

    def next(self):
        self.i += 1
        if self.i >= len(self.fileNames):
            self.i = 0
        return self.getScreenshot()

    def nextDir(self):
        self.di += 1
        if self.di >= len(self.directoryList):
            self.di = 0
        self.directory = self.directoryList[self.di]
        self.fileNames = os.listdir(self.directory)

    def getScreenshot(self):
        screenShot = cv2.imread(self.directory + self.fileNames[self.i])
        self.saveCoor(screenShot)
        return screenShot
