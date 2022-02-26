from threading import Thread
from time import time, sleep
import cv2

from app.app import App
from my_enum.game_type_state import GameTypeState
from game.game import Game
from util.pixel import getImgRectangle
import argparse

game = None
def main():
    global game
    parser = argparse.ArgumentParser(description='Run the game.')
    parser.add_argument("-t", "--type", dest="type", help="chose the type of game to start beetwen play record replay",
                        type=str, required=True)
    parser.add_argument("--fps", help="show fps", action='store_true')
    parser.add_argument("--show_region", help="show_region", action='store_true')
    parser.add_argument("--auto_screenshot", help="take screen shot automaticly with param as duration", type=int)
    # parser.add_argument("--AABuff", help="activate autobuff", action='store_true')

    args = parser.parse_args()
    game = Game(args)
    game.start()



    tScreenShot = 0
    game.stopped = False
    configState = False
    while not game.stopped:
        if game.screenShot is not None and not game.freeze:
            game.imSave.update("img", game.screenShot)
            if game.cv2Controller.withRegion:
                if game.cv2Controller.refreshRegion:
                    game.cv2Controller.loadRegions()
                game.cv2Controller.feedRegion(game.imSave.img)

            game.cv2Controller.applyScreenShotToWindow(game.imSave.img, "root")
            if game.imSave.mask_img is not None:
                game.cv2Controller.applyScreenShotToWindow(game.imSave.mask_img, "mask")
            if game.imSave.draw_img is not None:
                game.cv2Controller.applyScreenShotToWindow(game.imSave.draw_img, "draw")

        key = cv2.waitKey(1)
        # quit programm
        if key == ord('p') or game.stopped:  # quit
            game.stop()
            game.stopped = True
        # make a screenshot based of last 2 clicks
        if key == ord("t"):
            if game.imSave.img is not None:
                if len(game.imSave.clickList) >= 2:
                    last2Click = game.imSave.clickList[-2:]
                    tmpCoor = {
                        "x": last2Click[0]['x'],
                        "y": last2Click[0]['y'],
                        "w": abs(last2Click[1]['x'] - last2Click[0]['x']),
                        "h": abs(last2Click[1]['y'] - last2Click[0]['y'])
                    }
                    cv2.imwrite("tmp/cliped/{}_x_{}_y_{}_w_{}_h_{}.png".format(int(time()), tmpCoor['x'], tmpCoor['y'],
                                                                               tmpCoor["w"], tmpCoor['h']),
                                getImgRectangle(game.imSave.img, tmpCoor))

        if key == ord('s'):  # save img
            if game.imSave.img is not None:
                cv2.imwrite("tmp/record/{}.png".format(int(time())), game.imSave.img)
        if key == ord("f"):  # game.freeze
            game.freeze = not game.freeze
        # in replay mode  q d to move left right and z to change directory
        if game.typeState == GameTypeState.REPLAY:
            if key == ord('q'):
                game.RC.prev()
            elif key == ord('d'):
                game.RC.next()
            elif key == ord('z'):
                game.RC.nextDir()

        if game.args.auto_screenshot is not None and game.imSave.img is not None and not game.freeze:
            if tScreenShot == 0 or time() - tScreenShot > game.args.auto_screenshot:
                cv2.imwrite("tmp/auto_screenshot/{}.png".format(int(time())), game.imSave.img)
                tScreenShot = time()


t = Thread(target=main)
t.start()

while game is None:
    print('wait game to load')
    sleep(0.2)
app = App(game)

app.mainloop()


