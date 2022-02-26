import tkinter
from tkinter import ttk, W
from tkinter.scrolledtext import ScrolledText
from typing import Union

from PIL import Image, ImageTk


class MyTextArea:
    wText: ScrolledText = None

    def __init__(self, parent, row=0, col=0):
        self.parent = parent
        self.row = row
        self.col = col

        self.wText = ScrolledText(self.parent, width=40, height=10)
        self.wText.grid(row=self.row, column=self.col, columnspan=4)
        self.set('')

    def set(self, value):
        self.wText.delete(1.0, "end-1c")
        self.wText.insert(1.0, value)

    def get(self):
        return self.wText.get(1.0, "end-1c")


class MySimpleInput:
    wValue: tkinter.StringVar = None
    wLabel: ttk.Label = None
    parent = None
    type = None

    def __init__(self, parent, row=0, col=0, colspan=1):
        self.parent = parent
        self.row = row
        self.col = col
        self.wValue = tkinter.StringVar()
        self.wValue.set("")
        self.wLabel = ttk.Label(self.parent, textvariable=self.wValue, anchor="w", width=10)
        self.wLabel.grid(column=self.col, row=self.row, columnspan=colspan, padx=10, pady=10, sticky=W)

    def set(self, value):
        self.wValue.set(value)


class MyInput:
    label: str = ''
    path: Union[str, None] = None
    wValue: tkinter.StringVar = None
    wEntry: ttk.Entry = None
    wLabel: ttk.Label = None
    parent = None
    type = None

    def __init__(self, parent, label, value, row=0, col=0, path=None):
        self.parent = parent
        self.label = label
        self.row = row
        self.col = col
        self.path = path
        self.type = type(value)
        self.wLabel = ttk.Label(self.parent, text=label, anchor="w", width=len(label) + 3)
        self.wLabel.grid(column=self.col, row=self.row, padx=10, pady=10, sticky=W)
        self.wValue = tkinter.StringVar()
        self.wValue.set(value)
        self.wEntry = ttk.Entry(self.parent, textvariable=self.wValue, width=20)
        self.wEntry.grid(column=self.col + 1, row=self.row, padx=10, pady=10, sticky=W)

    def get(self):
        if self.canSave():
            return self.type(self.wValue.get())

    def updatePath(self, path):
        self.path = path

    def set(self, value):
        self.wValue.set(value)

    def canSave(self):
        return self.path is not None


class MyImg:
    img: Image = None
    imgTk: ImageTk = None
    root: tkinter.Label = None
    path: str = ""

    def __init__(self, parent, imgPath: str, row=0, col=0, path=""):
        self.parent = parent
        self.path = path
        self.root = tkinter.Label(self.parent)
        self.root.grid(row=row, column=col)
        if imgPath != "":

            self.img = Image.open(imgPath)
            self.img.thumbnail((30, 30), Image.ANTIALIAS)

            self.imgTk = ImageTk.PhotoImage(self.img)
            self.root.config(image=self.imgTk)

    def update(self, imgPath):
        if imgPath != "":
            self.img = Image.open(imgPath)
            self.img.thumbnail((75, 75), Image.ANTIALIAS)
            self.imgTk = ImageTk.PhotoImage(self.img)
            self.root.config(image=self.imgTk)
        else:
            self.root.config(image='')

    def resize(self, width, height):
        self.img = self.img.resize((width, height), Image.ANTIALIAS)
        self.imgTk = ImageTk.PhotoImage(self.img)
        self.root.config(image=self.imgTk)


class MyButton(ttk.Button):
    wValue: tkinter.StringVar = None

    def __init__(self, parent, text='', command=None, width=15, col=0, row=0, colspan=1, padX=0,
                 padY=0):
        self.wValue = tkinter.StringVar()
        self.wValue.set(text)
        super().__init__(parent, command=command, textvariable=self.wValue, width=width)
        self.grid(column=col, row=row, columnspan=colspan, padx=padX, pady=padY)

    def set(self, value):
        self.wValue.set(value)

    def get(self):
        return self.wValue.get()
