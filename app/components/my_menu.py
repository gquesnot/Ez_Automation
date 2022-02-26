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
    ]
    configMenu: tkinter.Menu = None
    gameStatesMenu: tkinter.Menu = None
    optionMenu: tkinter.Menu = None
    globalStatesMenu: tkinter.Menu = None
    btnQuit: MyButton = None
    gameStates: List[str] = []
    app: 'App' = None

    def __init__(self, app):
        self.menu = tkinter.Menu(app)
        self.app = app
        self.menu.config(bg="green", fg="white", activebackground='red', activeforeground='purple', activeborderwidth=0,
                         font=("Verdana", 12))
        self.gameStates = [el for el in dir(GameState) if "__" not in el]
        self.globalStates = [el for el in dir(GameTypeState) if "__" not in el]
        self.menu.add_command(label="Home", command=self.app.view.loadHome)
        self.addGlobalStateMenu()
        self.addGameStatesMenu()
        self.addOptionMenu()
        self.addConfigMenu()

        self.menu.add_command(label="Exit", command=self.app.quit)


    def addConfigMenu(self):
        self.configMenu = tkinter.Menu(self.menu, tearoff=0, relief=FLAT, font=("Verdana", 12), activebackground='red')
        for elem in self.elemToConfig:
            self.configMenu.add_command(label=elem, command=lambda el=elem: self.app.controller.loadConfig(el))
        self.menu.add_cascade(label="Config", menu=self.configMenu)

    def addOptionMenu(self):
        self.optionMenu = tkinter.Menu(self.menu, tearoff=0, relief=FLAT, font=("Verdana", 12), activebackground='red')
        self.optionMenu.add_command(label="Unfreeze" if self.app.game.config.freeze else "Freeze",
                                    command=lambda: self.app.controller.doAction("toggle", "freeze"))
        self.optionMenu.add_command(label="Auto Screenshot",
                                    command=lambda: self.app.controller.doAction("toggle", "autoScreenshot"))
        self.optionMenu.add_command(label="Show regions",
                                    command=lambda: self.app.controller.doAction("toggle", "showRegions"))
        self.optionMenu.add_command(label="Show Fps", command=lambda: self.app.controller.doAction("toggle", "showFps"))
        self.menu.add_cascade(label="Options", menu=self.optionMenu)

    def addGlobalStateMenu(self):
        self.globalStatesMenu = tkinter.Menu(self.menu, tearoff=0, relief=FLAT, font=("Verdana", 12), activebackground='red')

        for idx, state in enumerate(self.globalStates):
            self.globalStatesMenu.add_command(label="[*] " + state if self.app.game.typeState == GameTypeState[state] else state,
                                            command=lambda el=state: self.app.controller.doAction("set_global_state", GameTypeState[el]),
                                            state=tkinter.NORMAL if self.app.game.typeState !=
                                                                GameTypeState[state] else tkinter.DISABLED)

        self.menu.add_cascade(label="Global States", menu=self.globalStatesMenu)

    def addGameStatesMenu(self):
        self.gameStatesMenu = tkinter.Menu(self.menu, tearoff=0, relief=FLAT, font=("Verdana", 12), activebackground='red')

        for idx, state in enumerate(self.gameStates):
            print(idx, state)
            self.gameStatesMenu.add_command(label="[*] " + state if self.app.game.state == GameState[state] else state,
                                            command=lambda el = state: self.app.controller.doAction("set_game_state", GameState[el]),
                                            state=tkinter.NORMAL if self.app.game.state != GameState[state] else tkinter.DISABLED)

        self.menu.add_cascade(label="Game States", menu=self.gameStatesMenu)


    def rebuildGameStateMenu(self):
        for idx, state in enumerate(self.gameStates):
            self.gameStatesMenu.entryconfig(idx, label="[*] " + state if self.app.game.state == GameState[
                state] else state, state=tkinter.NORMAL if self.app.game.state != GameState[
                state] else tkinter.DISABLED)

    def rebuildOptionMenu(self):
        self.optionMenu.entryconfig(0, label="Unfreeze" if self.app.game.config.freeze else "Freeze")
        self.optionMenu.entryconfig(1,
                                    label="[*] Auto Screenshot" if self.app.game.config.autoScreenshot else "Auto Screenshot")
        self.optionMenu.entryconfig(2, label="Hide regions" if self.app.game.config.showRegions else "Show regions")


    def rebuildGlobalStateMenu(self):
        for idx , state in enumerate(self.globalStates):
            self.globalStatesMenu.entryconfig(idx, label="[*] " + state if self.app.game.typeState == GameTypeState[
                state] else state, state=tkinter.NORMAL if self.app.game.typeState != GameTypeState[
                state] else tkinter.DISABLED)


