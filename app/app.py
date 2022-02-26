import tkinter
from tkinter import W
from tkinter import ttk

from app.components.my_menu import MyMenu
from app.view.actions_view import MouseActionsView, KeyboardActionsView
from app.view.mask_detections_view import MaskDetectionsView
from app.view.match_images_view import MatchImagesView
from app.view.pixels_view import PixelsView
from app.view.regions_view import RegionsView
from app.view.tcr_scans_view import TcrScansView
from app.view.window_view import WindowView
from my_enum.game_state import GameState


class MainFrame(tkinter.Frame):
    game = None
    parent: tkinter.Tk = None
    menu: MyMenu = None
    app: 'App' = None
    content = None

    def __init__(self, app: 'App'):
        super().__init__(app)
        self.app = app
        print('init view')

    def clear(self):
        for widget in self.winfo_children():
            if type(widget) != tkinter.Menu:
                widget.destroy()

    def addView(self, view):
        self.content = view
        # self.content.load()


class Controller():
    app: 'App' = None

    def __init__(self, app: 'App'):
        self.app = app
        print('init controller')

    def loadConfig(self, config):
        print('loadConfig', config)
        self.app.view.clear()
        if config == "Window":
            self.app.view.addView(WindowView(self.app))
        elif config == "Regions":
            self.app.view.addView(RegionsView(self.app))
        elif config == "Pixels":
            self.app.view.addView(PixelsView(self.app))
        elif config == "Match Images":
            self.app.view.addView(MatchImagesView(self.app))
        elif config == "Tcr Scans":
            self.app.view.addView(TcrScansView(self.app))
        elif config == "Mask Detections":
            self.app.view.addView(MaskDetectionsView(self.app))
        elif config == "Mouse Actions":
            self.app.view.addView(MouseActionsView(self.app))
        elif config == "Keyboard Actions":
            self.app.view.addView(KeyboardActionsView(self.app))

    def doAction(self, toDo, state):
        print('doAction', toDo, state)
        if state == "freeze":
            self.app.game.toggleFreeze()
        else:
            self.app.game.setState(GameState[state])
        self.app.menu.rebuildStateMenu()

    def test(self, config, hint):
        if config == "pixels":
            return self.app.game.dpc.checkPixel(hint)
        elif config == "matchImages":
            return self.app.game.dpc.checkImageMatch(hint)
        elif config == "tcrScans":
            return self.app.game.dpc.checkTcrScan(hint)
        elif config == "maskDetections":
            return self.app.game.dpc.checkMaskDetection(hint)
        elif config == "mouseActions":
            self.app.game.doClick(hint, activate=True, isTest=True)
        elif config == "keyboardActions":
            self.app.game.doKey(hint, activate=True, isTest=True)
        return None


class App(tkinter.Tk):
    view: MainFrame = None
    game = None
    controller: Controller = None

    def __init__(self, game):
        print('init app')
        super().__init__()
        self.game = game
        self.menu = MyMenu(self)

        self.config(menu=self.menu.menu)
        self.title("Bot Control")
        self.geometry("700x650")
        self.resizable(width=False, height=False)
        self.style = ttk.Style(self)
        self.style.theme_use("vista")
        self.controller = Controller(self)
        self.view = MainFrame(self)
        self.view.grid(sticky=W)
