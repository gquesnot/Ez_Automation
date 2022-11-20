from dataclasses import fields
from time import sleep
from typing import Union

from baseclass.my_dataclass.action_config import KeyboardActionConfigs, MouseActionConfigs
from baseclass.my_dataclass.action_record_config import ActionRecordConfigs
from baseclass.my_dataclass.image_match_config import ImageMatchConfigs
from baseclass.my_dataclass.mask_detection_config import MaskDetectionConfigs
from baseclass.my_dataclass.pixel_config import PixelConfigs
from baseclass.my_dataclass.region_config import RegionConfigs
from baseclass.my_dataclass.tcr_scan_config import TcrScanConfigs
from baseclass.my_dataclass.window_config import WindowConfig
from util.json_function import get_json, to_json


class ConfigController:
    clicks = []

    game = None
    window: WindowConfig = None
    regions: RegionConfigs = None
    match_images: ImageMatchConfigs = None
    pixels: PixelConfigs = None
    tcr_scans: TcrScanConfigs = None
    mask_detections: MaskDetectionConfigs = None
    mouse_actions: MouseActionConfigs = None
    keyboard_actions: KeyboardActionConfigs = None
    replay_actions: ActionRecordConfigs = None
    freeze: bool = False
    auto_screenshot: bool = False
    show_regions: bool = False
    auto_screenshot_interval: int = 3
    show_fps: bool = False
    recording: bool = False

    maskTest: Union[str, None] = None

    def __init__(self, game):
        self.window = WindowConfig.from_dict(get_json("window"), )
        self.regions = RegionConfigs.from_dict(get_json("regions"))
        self.match_images = ImageMatchConfigs.from_dict(get_json("match_images"))
        self.pixels = PixelConfigs.from_dict(get_json("pixels"))
        self.tcr_scans = TcrScanConfigs.from_dict(get_json("tcr_scans"))
        self.mask_detections = MaskDetectionConfigs.from_dict(get_json("mask_detections"))
        self.mouse_actions = MouseActionConfigs.from_dict(get_json("mouse_actions"))
        self.keyboard_actions = KeyboardActionConfigs.from_dict(get_json("keyboard_actions"))
        self.replay_actions = ActionRecordConfigs.from_dict(get_json("replay_actions"))
        print(self.replay_actions)
        self.game = game

    def apply(self, obj, hint: str, with_out_dict: bool = False):
        my_dc = getattr(self, hint)

        for field in fields(my_dc):
            if with_out_dict:
                value = getattr(my_dc.dict, field.name)
            else:
                value = getattr(my_dc, field.name)
            setattr(obj, field.name, value)

    def toggle_recording(self):
        if self.recording is False:
            self.game.action_listener.start()
        else:
            self.game.action_listener.stop()
        # print('pass start recording', self.game.action_listener.actions)
        for k in self.game.action_listener.actions:
            print(k)
        self.recording = not self.recording

    def set(self, model, obj, save=False, load=False):
        my_dc = getattr(self, model)
        for field in fields(my_dc):
            setattr(my_dc, field.name, getattr(obj, field.name))
        if load:
            self.load(model)
        if save:
            return self.save(model)
        return my_dc

    def toggle(self, key, double=False):
        if key == "recording" and self.recording is False:
            self.game.action_listener.start()
        elif key == "recording" and self.recording is True:
            self.game.action_listener.stop()
        setattr(self, key, not getattr(self, key))

        if double:
            sleep(0.1)
            setattr(self, key, not getattr(self, key))

    def set_key(self, model, key, value, save=False, load=False):
        my_dc = getattr(self, model)
        setattr(my_dc, key, value)
        if load:
            self.load(model)
        if save:
            return self.save(model)
        return my_dc

    def save_only(self, model, reload=False):
        my_dc = getattr(self, model)
        if reload:
            self.load(model)
        to_json(model, my_dc.to_dict())
        return my_dc

    def save(self, model):
        my_dc = getattr(self, model)
        to_json(model, my_dc.to_dict(), "json_data/")
        return my_dc

    def load(self, model):

        if model == "window":
            self.game.wc.load_config()
        elif model == "regions":
            # self.game.regions = getattr(self, model)
            self.game.cv2_controller.refresh_region = True
        elif model == "match_images":
            self.game.dpc.load_match_images()
        elif model == "pixels":
            self.game.dpc.load_pixels()
        elif model == "tcr_scans":
            self.game.dpc.load_tcr_scans()
        elif model == "mask_detections":
            self.game.dpc.load_mask_detections()
