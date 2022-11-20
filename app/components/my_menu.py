import tkinter
from tkinter import FLAT
from typing import List

from app.components.my_input import MyButton
from baseclass.my_enum.game_state import GameState
from baseclass.my_enum.game_type_state import GameTypeState


class MyMenu:
    elemToConfig = [
        "Window",
        "Regions",
        "Pixels",
        "Match Images",
        "Tcr Scans",
        "Mask Detections",
        "Mouse Actions",
        "Keyboard Actions",
        "Record actions"
    ]
    config_menu: tkinter.Menu = None
    game_states_menu: tkinter.Menu = None
    option_menu: tkinter.Menu = None
    global_states_menu: tkinter.Menu = None
    btn_quit: MyButton = None
    game_states: List[str] = []
    app: 'App' = None

    def __init__(self, app):
        self.menu = tkinter.Menu(app)
        self.app = app
        self.menu.config(bg="green", fg="white", activebackground='red', activeforeground='purple', activeborderwidth=0,
                         font=("Verdana", 12))
        self.game_states = [el for el in dir(GameState) if "__" not in el]
        self.global_states = [el for el in dir(GameTypeState) if "__" not in el]
        self.menu.add_command(label="Home", command=self.app.view.load_home)
        self.add_global_state_menu()
        self.add_game_states_menu()
        self.add_option_menu()
        self.add_config_menu()

        self.menu.add_command(label="Exit", command=self.quit)

    def add_config_menu(self):
        self.config_menu = tkinter.Menu(self.menu, tearoff=0, relief=FLAT, font=("Verdana", 12), activebackground='red')
        for elem in self.elemToConfig:
            self.config_menu.add_command(label=elem, command=lambda el=elem: self.app.controller.load_config(el))
        self.menu.add_cascade(label="Config", menu=self.config_menu)

    def add_option_menu(self):
        self.option_menu = tkinter.Menu(self.menu, tearoff=0, relief=FLAT, font=("Verdana", 12), activebackground='red')
        self.option_menu.add_command(label="Unfreeze" if self.app.game.config.freeze else "Freeze",
                                     command=lambda: self.app.controller.do_action("toggle", "freeze"))
        self.option_menu.add_command(
            label="[*] Auto Screenshot" if self.app.game.config.auto_screenshot else "Auto Screenshot",
            command=lambda: self.app.controller.do_action("toggle", "autoScreenshot"))
        self.option_menu.add_command(label="Hide regions" if self.app.game.config.show_regions else "Show regions",
                                     command=lambda: self.app.controller.do_action("toggle", "showRegions"))
        self.option_menu.add_command(label="Hide Fps" if self.app.game.config.showFps else "Show Fps",
                                     command=lambda: self.app.controller.do_action("toggle", "showFps"))
        self.option_menu.add_command(label="End Recording" if self.app.game.config.recording else "Start Recording",
                                     command=lambda: self.app.controller.do_action("toggle", "recording"))
        self.menu.add_cascade(label="Options", menu=self.option_menu)

    def quit(self, event=None):
        self.app.game.stopped = True
        self.app.destroy()
        self.app.quit()

    def add_global_state_menu(self):
        self.global_states_menu = tkinter.Menu(self.menu, tearoff=0, relief=FLAT, font=("Verdana", 12),
                                               activebackground='red')

        for idx, state in enumerate(self.global_states):
            self.global_states_menu.add_command(
                label="[*] " + state if self.app.game.type_state == GameTypeState[state] else state,
                command=lambda el=state: self.app.controller.do_action("set_global_state", GameTypeState[el]),
                state=tkinter.NORMAL if self.app.game.type_state !=
                                        GameTypeState[state] else tkinter.DISABLED)

        self.menu.add_cascade(label="Global States", menu=self.global_states_menu)

    def add_game_states_menu(self):
        self.game_states_menu = tkinter.Menu(self.menu, tearoff=0, relief=FLAT, font=("Verdana", 12),
                                             activebackground='red')

        for idx, state in enumerate(self.game_states):
            self.game_states_menu.add_command(
                label="[*] " + state if self.app.game.state == GameState[state] else state,
                command=lambda el=state: self.app.controller.do_action("set_game_state", GameState[el]),
                state=tkinter.NORMAL if self.app.game.state != GameState[state] else tkinter.DISABLED)

        self.menu.add_cascade(label="Game States", menu=self.game_states_menu)

    def rebuild_game_state_menu(self):
        for idx, state in enumerate(self.game_states):
            self.game_states_menu.entryconfig(idx, label="[*] " + state if self.app.game.state == GameState[
                state] else state, state=tkinter.NORMAL if self.app.game.state != GameState[
                state] else tkinter.DISABLED)

    def rebuild_option_menu(self):
        self.option_menu.entryconfig(0, label="Unfreeze" if self.app.game.config.freeze else "Freeze")
        self.option_menu.entryconfig(1,
                                     label="[*] Auto Screenshot" if self.app.game.config.auto_screenshot else "Auto Screenshot")
        self.option_menu.entryconfig(2, label="Hide regions" if self.app.game.config.show_regions else "Show regions")
        self.option_menu.entryconfig(3, label="Hide Fps" if self.app.game.config.showFps else "Show Fps")
        self.option_menu.entryconfig(4, label="End Recording" if self.app.game.config.recording else "Start Recording")

    def rebuild_global_state_menu(self):
        for idx, state in enumerate(self.global_states):
            self.global_states_menu.entryconfig(idx, label="[*] " + state if self.app.game.type_state == GameTypeState[
                state] else state, state=tkinter.NORMAL if self.app.game.type_state != GameTypeState[
                state] else tkinter.DISABLED)
