from typing import Dict

from baseclass.datapicker import DataPicker
from baseclass.datascanner import DataScanner
from baseclass.matchimages import MatchImages
from baseclass.my_dataclass.pixel_config import PixelConfig
from baseclass.my_enum.condition_type import ConditionType
from util.pixel import compare_pixel


class DataPickerController:
    pick_dict: Dict[str, DataPicker] = {}
    scan_dict: Dict[str, DataScanner] = {}
    pixel_dict: Dict[str, PixelConfig] = {}
    imgs_scan_dict: Dict[str, MatchImages] = {}

    game = None

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_mask_detections()
        self.load_tcr_scans()
        self.load_match_images()
        self.load_pixels()

    def load_mask_detections(self):
        self.pick_dict = {}
        for mask_name, mask_detections in self.game.config.mask_detections.dict.items():
            dp = DataPicker(self.game, mask_detections)
            self.pick_dict[mask_name] = dp

    def load_pixels(self):

        self.pixel_dict = self.game.config.pixels.dict

    def load_tcr_scans(self):
        self.scan_dict = {}
        for screen_info_name, screen_info in self.game.config.tcr_scans.dict.items():
            ds = DataScanner(self.game, screen_info)
            self.scan_dict[screen_info_name] = ds

    def load_match_images(self):
        self.imgs_scan_dict = {}
        for match_images_name, match_images_info in self.game.config.match_images.dict.items():
            mi = MatchImages(self.game, match_images_info)
            self.imgs_scan_dict[match_images_name] = mi

    def check_pixel(self, hint):
        if self.game.screen_shot is not None:
            screen_shot = self.game.screen_shot
            if hint in self.pixel_dict:

                match = False
                for pixel in self.pixel_dict[hint].pixels:
                    new_screenshot = screen_shot
                    if pixel.region != "root":
                        new_screenshot = self.game.regions.applyRegion(pixel.region, screen_shot)
                    if compare_pixel(new_screenshot, pixel):
                        match = True
                        if self.pixel_dict[hint].type == ConditionType.OR:
                            return True

                    elif self.pixel_dict[hint].type == ConditionType.AND:
                        return False
                return match
        return False

    def check_tcr_scan(self, hint):
        if hint in self.scan_dict:
            return self.scan_dict[hint].scan_datas()
        return None

    def check_mask_detection(self, hint, get="results"):
        if hint in self.pick_dict:
            return self.pick_dict[hint].scan_datas(get=get)
        return None

    def check_config_has_mask_test(self):
        if self.game.config.maskTest is not None:
            if self.game.config.maskTest in self.pick_dict:
                drawed_sc = self.check_mask_detection(self.game.config.maskTest, get="screenshot")
                self.game.im_save.update("draw_img", drawed_sc)

    def check_image_match(self, hint):
        if hint in self.imgs_scan_dict:
            return self.imgs_scan_dict[hint].scan_datas()
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
    #             coors = v.get_coors()
    #             if len(coors) > 0:
    #                 drawScreenShot = v.drawScreenShot(newImg)
    #     return newImg
