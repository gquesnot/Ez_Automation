import tkinter
from tkinter import FLAT
from typing import List


from app.components.my_input import MyButton
from my_enum.game_state import GameState


class MyMenu():
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
    statesMenu: tkinter.Menu = None
    btnQuit: MyButton = None
    states: List[str] = []
    app: 'App' = None

    def __init__(self, app):
        self.menu = tkinter.Menu(app)
        self.app = app
        self.menu.config(bg="green", fg="white", activebackground='red', activeforeground='purple', activeborderwidth=0,
                         font=("Verdana", 12))
        self.states = [el for el in dir(GameState) if "__" not in el]
        self.addStatesMenu()
        self.addConfigMenu()

        self.menu.add_command(label="Exit", command=self.app.quit)

    def addConfigMenu(self):
        self.configMenu = tkinter.Menu(self.menu, tearoff=0, relief=FLAT, font=("Verdana", 12), activebackground='red')
        for elem in self.elemToConfig:
            self.configMenu.add_command(label=elem, command=lambda elem=elem: self.app.controller.loadConfig(elem))
        self.menu.add_cascade(label="Config", menu=self.configMenu)

    def addStatesMenu(self):
        self.statesMenu = tkinter.Menu(self.menu, tearoff=0, relief=FLAT, font=("Verdana", 12), activebackground='red')

        self.statesMenu.add_command(label="Unfreeze" if self.app.game.freeze else "Freeze",
                                    command=lambda: self.app.controller.doAction("set", "freeze"))
        for idx, state in enumerate(self.states):
            self.statesMenu.add_command(label="*" + state if self.app.game.state == GameState[state] else state,
                                        command=lambda: self.app.controller.doAction("set", state),
                                        state=tkinter.NORMAL if self.app.game.state !=
                                                                GameState[
                                                                    state] else tkinter.DISABLED)

        self.menu.add_cascade(label="States", menu=self.statesMenu)

    def rebuildStateMenu(self):
        self.statesMenu.entryconfig(0, label="Unfreeze" if self.app.game.freeze else "Freeze")
        for i in range(1, len(self.states) - 1):
            self.statesMenu.entryconfig(i, label="[*] " + self.states[i] if self.app.game.state == GameState[
                self.states[i]] else self.states[i], state=tkinter.NORMAL if self.app.game.state != GameState[
                self.states[i]] else tkinter.DISABLED)