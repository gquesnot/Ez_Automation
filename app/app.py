import tkinter
from tkinter import W
from tkinter import ttk

from app.components.my_menu import MyMenu
from app.view.actions_view import MouseActionsView, KeyboardActionsView, RecordPlayActionView
from app.view.mask_detections_view import MaskDetectionsView
from app.view.match_images_view import MatchImagesView
from app.view.pixels_view import PixelsView
from app.view.regions_view import RegionsView
from app.view.tcr_scans_view import TcrScansView
from app.view.window_view import WindowView
from baseclass.my_enum.game_type_state import GameTypeState


class MainFrame(tkinter.Frame):
    game = None
    parent: tkinter.Tk = None
    menu: MyMenu = None
    app: 'App' = None
    content = None
    fps_counter: tkinter.StringVar = None
    base_row = 0
    home: bool = True
    dir_var: tkinter.StringVar = None

    def __init__(self, app: 'App'):
        super().__init__(app)
        self.app = app
        self.fps_counter = tkinter.StringVar()
        self.fps_counter.set('FPS: 0')
        self.dir_var = tkinter.StringVar()
        self.dir_var.set('DIR: ' + str(self.app.game.RC.get_directory_as_str()))

        print('init view')

    def load_home(self):
        self.clear()
        self.base_row = 0
        self.home = True
        if self.app.game.config.showFps:
            tkinter.Label(self, textvariable=self.fps_counter, font=('Helvetica', '10')).grid(row=self.base_row,
                                                                                              column=1, sticky=W)
            self.base_row += 1
        if self.app.game.type_state == GameTypeState.REPLAY:

            tkinter.Label(self, textvariable=self.dir_var, font=('Helvetica', '10')).grid(row=self.base_row, column=1,
                                                                                          sticky=W)

            ttk.Button(self, command=lambda: self.app.game.RC.prev(), text='Previous Frame').grid(row=self.base_row + 1,
                                                                                                  column=1, sticky=W)
            ttk.Button(self, command=lambda: self.app.game.RC.next(), text='Next Frame').grid(row=self.base_row + 1,
                                                                                              column=0, sticky=W)
            ttk.Button(self, command=lambda: self.next_dir(), text='Next Dir').grid(row=self.base_row + 1, column=2,
                                                                                    sticky=W)
            self.base_row += 2
        else:
            ttk.Button(self, command=self.app.game.im_save.save_screen_shot, text='Take Screenshot').grid(
                row=self.base_row, column=0, sticky=W)
            self.base_row += 1
        ttk.Button(self, command=self.app.game.im_save.save_rectangle, text='Show Rectangle\nfrom 2 last click').grid(
            row=self.base_row, column=0, sticky=W)
        ttk.Button(self, command=lambda: self.app.game.config.load('window'), text='Fix Window').grid(
            row=self.base_row + 1, column=0, sticky=W)
        self.base_row += 2

    def next_dir(self, event=None):
        self.app.game.RC.nextDir()
        self.dir_var.set('DIR: ' + str(self.app.game.RC.getDirectoryAsStr()))

    def clear(self):
        for widget in self.winfo_children():
            if type(widget) != tkinter.Menu:
                widget.destroy()

    def add_view(self, view):
        self.home = False
        self.content = view

        # self.content.load()


class Controller:
    app: 'App' = None

    def __init__(self, app: 'App'):
        self.app = app
        print('init controller')

    def load_config(self, config):
        print('loadConfig', config)
        self.app.view.clear()
        if config == "Window":
            self.app.view.add_view(WindowView(self.app))
        elif config == "Regions":
            self.app.view.add_view(RegionsView(self.app))
        elif config == "Pixels":
            self.app.view.add_view(PixelsView(self.app))
        elif config == "Match Images":
            self.app.view.add_view(MatchImagesView(self.app))
        elif config == "Tcr Scans":
            self.app.view.add_view(TcrScansView(self.app))
        elif config == "Mask Detections":
            self.app.view.add_view(MaskDetectionsView(self.app))
        elif config == "Mouse Actions":
            self.app.view.add_view(MouseActionsView(self.app))
        elif config == "Keyboard Actions":
            self.app.view.add_view(KeyboardActionsView(self.app))
        elif config == "Record actions":
            self.app.view.add_view(RecordPlayActionView(self.app))

    def do_action(self, to_do, state):
        print('do action', to_do, state)
        if to_do == 'toggle':
            self.app.game.config.toggle(state)
            self.app.menu.rebuild_option_menu()
        if "state" in to_do:
            if 'global' in to_do:
                self.app.game.setGlobalState(state)
                self.app.menu.rebuild_global_state_menu()
            elif 'game' in to_do:
                self.app.game.setState(state)
                self.app.menu.rebuild_game_state_menu()

        if self.app.view.home:
            self.app.view.load_home()

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
        self.geometry("800x650")
        self.resizable(width=False, height=False)
        self.style = ttk.Style(self)
        self.style.theme_use("vista")

        self.view.grid(sticky=W)
        self.view.load_home()
