import tkinter
from tkinter import ttk, W
from tkinter.scrolledtext import ScrolledText
from typing import Union

from PIL import Image, ImageTk


class MyTextArea:
    w_text: ScrolledText = None

    def __init__(self, parent, row=0, col=0):
        self.parent = parent
        self.row = row
        self.col = col

        self.w_text = ScrolledText(self.parent, width=50, height=25)
        self.w_text.grid(row=self.row, column=self.col, columnspan=6)
        self.set('')

    def set(self, value):
        self.w_text.delete(1.0, "end-1c")
        self.w_text.insert(1.0, value)

    def get(self):
        return self.w_text.get(1.0, "end-1c")


class MySimpleInput:
    w_value: tkinter.StringVar = None
    w_label: ttk.Label = None
    parent = None
    type = None

    def __init__(self, parent, row=0, col=0, colspan=1):
        self.parent = parent
        self.row = row
        self.col = col
        self.w_value = tkinter.StringVar()
        self.w_value.set("")
        self.w_label = ttk.Label(self.parent, textvariable=self.w_value, anchor="w", width=40)
        self.w_label.grid(column=self.col, row=self.row, columnspan=colspan, padx=0, pady=10, sticky=W)

    def set(self, value):
        self.w_value.set(value)


class MyInput:
    label: str = ''
    path: Union[str, None] = None
    w_value: tkinter.StringVar = None
    w_entry: ttk.Entry = None
    w_label: ttk.Label = None
    parent = None
    type = None

    def __init__(self, parent, label, value, row=0, col=0, path=None):
        self.parent = parent
        self.label = label
        self.row = row
        self.col = col
        self.path = path
        self.type = type(value)
        self.w_label = ttk.Label(self.parent, text=label, anchor="w", width=len(label) + 3)
        self.w_label.grid(column=self.col, row=self.row, padx=10, pady=3, sticky=W)
        self.w_value = tkinter.StringVar()
        self.w_value.set(value)
        self.w_entry = ttk.Entry(self.parent, textvariable=self.w_value, width=20)
        self.w_entry.grid(column=self.col + 1, row=self.row, padx=10, pady=3, sticky=W)

    def get(self):
        if self.canSave():
            return self.type(self.w_value.get())

    def updatePath(self, path):
        self.path = path

    def set(self, value):
        self.w_value.set(value)

    def canSave(self):
        return self.path is not None


class MyImg:
    img: Image = None
    img_tk: ImageTk = None
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

            self.img_tk = ImageTk.PhotoImage(self.img)
            self.root.config(image=self.img_tk)

    def update(self, imgPath):
        if imgPath != "":
            self.img = Image.open(imgPath)
            self.img.thumbnail((75, 75), Image.ANTIALIAS)
            self.img_tk = ImageTk.PhotoImage(self.img)
            self.root.config(image=self.img_tk)
        else:
            self.root.config(image='')

    def resize(self, width, height):
        self.img = self.img.resize((width, height), Image.ANTIALIAS)
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.root.config(image=self.img_tk)


class MyButton(ttk.Button):
    w_value: tkinter.StringVar = None

    def __init__(self, parent, text='', command=None, width=15, col=0, row=0, colspan=1, padX=0,
                 padY=0):
        self.w_value = tkinter.StringVar()
        self.w_value.set(text)
        super().__init__(parent, command=command, textvariable=self.w_value, width=width)
        self.grid(column=col, row=row, columnspan=colspan, padx=padX, pady=padY)

    def set(self, value):
        self.w_value.set(value)

    def get(self):
        return self.w_value.get()
