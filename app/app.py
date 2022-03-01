import tkinter
from tkinter import W
from tkinter import ttk

from app.components.my_input import MyButton
from app.components.my_menu import MyMenu
from app.view.actions_view import MouseActionsView, KeyboardActionsView, RecordPlayActionView
from app.view.mask_detections_view import MaskDetectionsView
from app.view.match_images_view import MatchImagesView
from app.view.pixels_view import PixelsView
from app.view.regions_view import RegionsView
from app.view.tcr_scans_view import TcrScansView
from app.view.window_view import WindowView
from baseclass.my_enum.game_state import GameState
from baseclass.my_enum.game_type_state import GameTypeState


class MainFrame(tkinter.Frame):
    game = None
    parent: tkinter.Tk = None
    menu: MyMenu = None
    app: 'App' = None
    content = None
    fpsCounter : tkinter.StringVar = None
    baseRow = 0
    home : bool = True
    dirVar: tkinter.StringVar = None

    def __init__(self, app: 'App'):
        super().__init__(app)
        self.app = app
        self.fpsCounter = tkinter.StringVar()
        self.fpsCounter.set('FPS: 0')
        self.dirVar = tkinter.StringVar()
        self.dirVar.set('DIR: ' + str(self.app.game.RC.getDirectoryAsStr()))


        print('init view')




    def loadHome(self):
        self.clear()
        self.baseRow = 0
        self.home = True
        if self.app.game.config.showFps :

            tkinter.Label(self, textvariable=self.fpsCounter, font=('Helvetica', '10')).grid(row=self.baseRow, column=1, sticky=W)
            self.baseRow += 1
        if self.app.game.typeState == GameTypeState.REPLAY:

            tkinter.Label(self, textvariable=self.dirVar, font=('Helvetica', '10')).grid(row=self.baseRow, column=1, sticky=W)

            ttk.Button(self, command=lambda:self.app.game.RC.prev(), text='Previous Frame').grid(row=self.baseRow + 1, column= 1, sticky=W)
            ttk.Button(self, command=lambda:self.app.game.RC.next(), text='Next Frame').grid(row=self.baseRow + 1, column=0, sticky=W)
            ttk.Button(self, command=lambda:self.nextDir(), text='Next Dir').grid(row=self.baseRow + 1, column= 2, sticky=W)
            self.baseRow += 2
        else:
            ttk.Button(self, command=self.app.game.imSave.saveScreenShot, text='Take Screenshot').grid(row=self.baseRow, column=0, sticky=W)
            self.baseRow += 1
        ttk.Button(self, command=self.app.game.imSave.saveRectangle, text='Show Rectangle\nfrom 2 last click').grid(row=self.baseRow, column=0, sticky=W)
        ttk.Button(self, command=lambda :self.app.game.config.load('window'), text='Fix Window').grid(row=self.baseRow +1, column=0, sticky=W)
        self.baseRow +=2

    def nextDir(self, event = None):
        self.app.game.RC.nextDir()
        self.dirVar.set('DIR: ' + str(self.app.game.RC.getDirectoryAsStr()))


    def clear(self):
        for widget in self.winfo_children():
            if type(widget) != tkinter.Menu:
                widget.destroy()

    def addView(self, view):
        self.home = False
        self.content = view

        # self.content.load()


class Controller:
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
        elif config == "Record actions":
            self.app.view.addView(RecordPlayActionView(self.app))

    def doAction(self, toDo, state):
        print('do action', toDo, state)
        if toDo == 'toggle':
            self.app.game.config.toggle(state)
            self.app.menu.rebuildOptionMenu()
        if "state" in  toDo:
            if 'global' in toDo:
                self.app.game.setGlobalState(state)
                self.app.menu.rebuildGlobalStateMenu()
            elif 'game' in toDo:
                self.app.game.setState(state)
                self.app.menu.rebuildGameStateMenu()

        if self.app.view.home:
            self.app.view.loadHome()


    def test(self, config, hint):
        print('test', config, hint)
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
    controller: Controller = None
    game = None

    def __init__(self, game):
        print('init app')
        super().__init__()
        self.game = game
        self.controller = Controller(self)
        self.view = MainFrame(self)
        self.menu = MyMenu(self)

        self.config(menu=self.menu.menu)
        self.title("Bot Control")
        self.geometry("700x650")
        self.resizable(width=False, height=False)
        self.style = ttk.Style(self)
        self.style.theme_use("vista")

        self.view.grid(sticky=W)
        self.view.loadHome()
