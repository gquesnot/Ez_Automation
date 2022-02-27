from threading import Thread
from time import time, sleep
from typing import Union

import cv2

from app.app import App
from baseclass.my_enum.game_type_state import GameTypeState
from game.game import Game
from util.pixel import getImgRectangle

game: Union[Game, None] = None


def main():
    global game
    game = Game()
    game.start()

    tScreenShot = 0
    game.stopped = False
    while not game.stopped:
        if game.screenShot is not None and not game.config.freeze:
            game.imSave.update("img", game.screenShot)
            if game.config.showRegions:
                if game.cv2Controller.refreshRegion:
                    game.cv2Controller.loadRegions()
                game.cv2Controller.feedRegion(game.imSave.img)
            else:
                game.cv2Controller.clearRegions()

            game.cv2Controller.applyScreenShotToWindow(game.imSave.img, "root")
            if game.imSave.mask_img is not None:

                game.cv2Controller.applyScreenShotToWindow(game.imSave.mask_img, "mask")
            if game.imSave.draw_img is not None:
                game.cv2Controller.applyScreenShotToWindow(game.imSave.draw_img, "draw")
            if game.config.autoScreenshot:
                if tScreenShot == 0 or time() - tScreenShot > game.config.autoScreenshotInterval:
                    print("screenshot")
                    cv2.imwrite("tmp/auto_screenshot/{}.png".format(int(time())), game.screenShot)
                    tScreenShot = time()
        sleep(0.01)
        cv2.waitKey(1)
        if game.stopped:
            game.stop()
            return

t = Thread(target=main)
t.start()

while game is None:
    print('waiting game to load')
    sleep(0.2)
app = App(game)
game.addApp(app)

app.mainloop()
