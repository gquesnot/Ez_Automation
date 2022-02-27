from dataclasses import fields
from time import sleep
from typing import Union

from baseclass.my_dataclass.mask_detection_config import MaskDetectionConfigs
from baseclass.my_dataclass.action_config import KeyboardActionConfigs, MouseActionConfigs
from baseclass.my_dataclass.window_config import WindowConfig
from baseclass.my_dataclass.tcr_scan_config import TcrScanConfigs
from baseclass.my_dataclass.pixel_config import PixelConfigs
from baseclass.my_dataclass.image_match_config import ImageMatchConfigs
from baseclass.my_dataclass.region_config import RegionConfigs
from util.json_function import getJson, toJson


class ConfigController:
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

    freeze: bool = False
    autoScreenshot: bool = False
    showRegions: bool = False
    autoScreenshotInterval: int = 3
    showFps: bool = False

    maskTest: Union[str, None] = None

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

    def toggle(self, key, double=False):
        setattr(self, key, not getattr(self, key))
        if double:
            sleep(0.1)
            setattr(self, key, not getattr(self, key))

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
            # self.game.regions = getattr(self, model)
            self.game.cv2Controller.refreshRegion = True
        elif model == "matchImages":
            self.game.dpc.loadMatchImages()
        elif model == "pixels":
            self.game.dpc.loadPixels()
        elif model == "tcrScans":
            self.game.dpc.loadTcrScans()
        elif model == "maskDetections":
            self.game.dpc.loadMaskDetections()
