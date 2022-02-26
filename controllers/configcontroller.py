import os
from dataclasses import fields
from time import sleep

import cv2

from app.my_dataclasses import WindowConfig, RegionConfigs, ImageMatchConfigs, PixelConfigs, TcrScanConfigs, \
    MaskDetectionConfigs, MouseActionConfigs, KeyboardActionConfigs
from util.InputHandler import getMenus, getMenusElements, updateValueOfKey, askQuestion
from util.json_function import getJson, toJson
from util.pixel import getImgRectangle


class ConfigController():
    clicks = []

    game = None
    window: WindowConfig = None
    regions: RegionConfigs = None
    matchImages: ImageMatchConfigs = None
    pixels: PixelConfigs = None
    tcrScans: TcrScanConfigs = None
    maskDetections: MaskDetectionConfigs = None
    mouseActions: MouseActionConfigs = None
    keyboardActions: KeyboardActionConfigs = None

    def __init__(self, game):
        self.window = WindowConfig.from_dict(getJson("window"), )
        self.regions = RegionConfigs.from_dict(getJson("regions"))
        self.matchImages = ImageMatchConfigs.from_dict(getJson("matchImages"))
        self.pixels = PixelConfigs.from_dict(getJson("pixels"))
        self.tcrScans = TcrScanConfigs.from_dict(getJson("tcrScans"))
        self.maskDetections = MaskDetectionConfigs.from_dict(getJson("maskDetections"))
        self.mouseActions = MouseActionConfigs.from_dict(getJson("mouseActions"))
        self.keyboardActions = KeyboardActionConfigs.from_dict(getJson("keyboardActions"))
        self.game = game

    def apply(self, obj, hint: str, withOutDict: bool = False):
        myDc = getattr(self, hint)

        for field in fields(myDc):
            if withOutDict:
                value = getattr(myDc.dict, field.name)
            else:
                value = getattr(myDc, field.name)
            setattr(obj, field.name, value)

    def set(self, model, obj, save=False, load=False):
        myDc = getattr(self, model)
        for field in fields(myDc):
            setattr(myDc, field.name, getattr(obj, field.name))
        if load:
            self.load(model)
        if save:
            return self.save(model)
        return myDc

    def setKey(self, model, key, value, save=False, load=False):
        myDc = getattr(self, model)
        setattr(myDc, key, value)
        if load:
            self.load(model)
        if save:
            return self.save(model)
        return myDc

    def saveOnly(self, model, reload=False):
        myDc = getattr(self, model)
        if reload:
            self.load(model)
        print(myDc)
        print(myDc.to_dict())
        toJson(model, myDc.to_dict())
        return myDc

    def save(self, model):
        myDc = getattr(self, model)
        toJson(model, myDc.to_dict(), "json_data/")
        return myDc

    def load(self, model):

        if model == "window":
            self.game.wc.loadConfig()
        elif model == "regions":
            #self.game.regions = getattr(self, model)
            self.game.cv2Controller.refreshRegion = True
        elif model == "matchImages":
            self.game.dpc.loadMatchImages()
        elif model == "pixels":
            self.game.dpc.loadPixels()
        elif model == "tcrScans":
            self.game.dpc.loadTcrScans()
        elif model == "maskDetections":
            self.game.dpc.loadMaskDetections()
