import cv2

from util.json_function import apply_json_config


class Cv2WindowController:
    window_list = {}
    game_name = ""
    cv2_region_list = {}
    refresh_region: bool = False

    def __init__(self, game):

        self.game = game
        self.regions = self.game.regions
        apply_json_config(self, "cv2")
        self.list = [k for k, v in self.window_list.items()]
        for k, v in self.window_list.items():
            v['name'] = k + " " + self.game_name
        self.create_windows(self.window_list)
        self.set_mouse_call_back("root", self.game.im_save.pick_color)

    def clear_regions(self):
        if len(self.cv2_region_list) != 0:
            for k, v in self.cv2_region_list.items():
                cv2.destroyWindow(v['name'])
        self.cv2_region_list = {}

    def load_regions(self):
        self.clear_regions()

        for region_name, region in self.regions.all().items():
            self.cv2_region_list[region_name] = {
                "name": "Regions " + region_name,
                "coor": [-1080, 400],
                "resize": (int(region.rectangle.w * region.ratio), int(region.rectangle.h * region.ratio)),
            }
        if self.game.config.show_regions:
            self.create_windows(self.cv2_region_list, regions=True)
        self.refresh_region = False

    def get_window_by_hint(self, hint):
        if hint in self.list:
            return self.window_list[hint]
        elif hint in self.cv2_region_list:
            return self.cv2_region_list[hint]
        else:
            return False

    def apply_screen_shot_to_window(self, screen_shot, hint):
        if self.game.wc.is_loaded:
            window = self.get_window_by_hint(hint)
            if window and screen_shot is not None and self.game.wc.w != 0:

                if "resize" not in window or window['ratio'] != 1:
                    try:
                        h, w, z = screen_shot.shape
                    except:
                        try:
                            h, w = screen_shot.shape
                            z = 3
                        except:
                            return
                    if not w or not h:
                        return
                    if not self.game.is_replay():
                        window['resize'] = (
                            int(w * window['ratio']), int(h * window['ratio']))
                    else:

                        window['resize'] = (
                            int(w * window['ratio']), int(h * window['ratio']))
                    cv2.imshow(window['name'], cv2.resize(screen_shot, window['resize']))
                else:
                    cv2.imshow(window['name'], screen_shot)

    def create_windows(self, window_dic, regions=False):
        for k, v in window_dic.items():
            cv2.namedWindow(v['name'])
            if regions:
                self.set_mouse_call_back(k, self.game.im_save.pick_color)
            # cv2.moveWindow(v['name'], *v['coor'])

    def set_mouse_call_back(self, hint, fn):
        window = self.get_window_by_hint(hint)
        if window:
            cv2.setMouseCallback(window['name'], fn, param={"window": hint})

    def feed_region(self, processed_image):
        if self.game.config.show_regions:
            if len(self.cv2_region_list) == 0:
                self.load_regions()
            for region_name, cv2Region in self.cv2_region_list.items():
                if self.refresh_region:
                    self.load_regions()

                new_img = self.regions.applyRegion(region_name, screenshot=processed_image)
                if new_img is not None:
                    cv2.imshow(cv2Region['name'], cv2.resize(new_img, cv2Region["resize"]))
