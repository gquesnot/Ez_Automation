from threading import Thread
from time import time, sleep
from typing import Union

import cv2

from app.app import App
from game.game import Game

game: Union[Game, None] = None


def main():
    global game
    game = Game()
    game.start()

    t_screen_shot = 0
    game.stopped = False
    while not game.stopped:
        if game.screen_shot is not None and not game.config.freeze:
            game.im_save.update("img", game.screen_shot)
            if game.config.show_regions:
                if game.cv2_controller.refresh_region:
                    game.cv2_controller.load_regions()
                game.cv2_controller.feed_region(game.im_save.img)
            else:
                game.cv2_controller.clear_regions()

            game.cv2_controller.apply_screen_shot_to_window(game.im_save.img, "root")
            if game.im_save.mask_img is not None:
                game.cv2_controller.apply_screen_shot_to_window(game.im_save.mask_img, "mask")
            if game.im_save.draw_img is not None:
                game.cv2_controller.apply_screen_shot_to_window(game.im_save.draw_img, "draw")
            if game.config.auto_screenshot:
                if t_screen_shot == 0 or time() - t_screen_shot > game.config.auto_screenshot_interval:
                    print("screenshot")
                    cv2.imwrite("tmp/auto_screenshot/{}.png".format(int(time())), game.screen_shot)
                    t_screen_shot = time()
        sleep(0.01)
        cv2.waitKey(1)
        if game.stopped:
            game.stop()
            return


if __name__ == '__main__':

    t = Thread(target=main)
    t.start()

    while game is None:
        print('waiting game to load')
        sleep(0.2)
    app = App(game)
    game.add_app(app)

    app.mainloop()
