import os

import cv2


class Replay:
    i = 0
    di = 0
    h = 0
    w = 0
    directory_list = ["tmp/auto_screenshot/", "tmp/clipped/", "tmp/screenshot/"]  # ['tmp/cliped/',
    current_dir = []

    def __init__(self):
        self.directory = self.directory_list[self.di]
        self.file_names = [dir_ for dir_ in os.listdir(self.directory) if dir_[0] != '.']

    def get_directory_as_str(self):
        return self.directory_list[self.di].split('/')[-2]

    def prev(self):
        self.i -= 1
        if self.i < 0:
            self.i = len(self.file_names) - 1
        return self.get_screenshot()

    def save_coor(self, screen_shot):
        self.h, self.w, channels = screen_shot.shape

    def next(self):
        self.i += 1
        if self.i >= len(self.file_names):
            self.i = 0
        return self.get_screenshot()

    def next_dir(self):
        self.di += 1
        if self.di >= len(self.directory_list):
            self.di = 0
        self.i = 0
        self.directory = self.directory_list[self.di]
        self.file_names = [dir_ for dir_ in os.listdir(self.directory) if dir_[0] != '.']

    def get_screenshot(self):
        if len(self.file_names) > 0:
            screen_shot = cv2.imread(self.directory + self.file_names[self.i])
            self.save_coor(screen_shot)
            return screen_shot
        return None
