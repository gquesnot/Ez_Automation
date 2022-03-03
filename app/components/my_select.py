import tkinter
from time import time
from tkinter import ttk, W
from typing import Union, Any

from app.components.my_input import MyButton
from baseclass.my_dataclass.base_dataclass import GetSetDict


class MyStringEnumSelect:
    label: str = ''
    path: Union[str, None] = None
    wValue: tkinter.StringVar = None
    wSelect: ttk.Combobox = None
    wLabel: ttk.Label = None
    enum: Any = None
    parent = None
    datas = []

    def __init__(self, parent, label, enum: Any, value: Any = None, row=0, col=0, path=None):
        self.parent = parent
        self.label = label
        self.row = row
        self.col = col
        self.path = path
        self.enum = enum
        self.datas = [el for el in dir(self.enum) if "__" not in el]
        self.wLabel = ttk.Label(self.parent, text=label, anchor="w", width=len(label) + 3)
        self.wLabel.grid(column=self.col, row=self.row, padx=10, pady=10, sticky=W)
        self.wValue = tkinter.StringVar()
        self.wValue.set(enum[value])
        self.wEntry = ttk.Combobox(self.parent, values=self.datas, textvariable=self.wValue, width=20, state="readonly")
        self.wEntry.grid(column=self.col + 1, row=self.row, padx=10, pady=10, sticky=W)

    def get(self):
        if self.canSave():
            return self.enum[self.wValue.get()]

    def updatePath(self, path):
        self.path = path

    def set(self, value):
        self.wValue.set(self.enum[value])

    def canSave(self):
        return self.path is not None


class MyChildSelect:
    datas: list = []
    wSelect: ttk.Combobox = None
    wValue: tkinter.StringVar = None
    btnNew: MyButton = None
    btnDel: MyButton = None
    prevValue: int = False

    def __init__(self, parent, datas, row=0):
        self.row = row
        self.parent = parent
        self.datas = datas
        self.wValue = tkinter.StringVar()
        if len(self.datas) > 0:
            self.set(0)
        self.wSelect = ttk.Combobox(self.parent, values=[str(i) for i in range(len(self.datas))],
                                    textvariable=self.wValue, state='readonly')
        self.wSelect.grid(column=0, row=row, padx=10, pady=10, sticky=W)
        self.wSelect.bind("<<ComboboxSelected>>", lambda event: self.doSelect())
        MyButton(self.parent, text="New", command=lambda: self.doNew(withViewUpdate=True), width=10, col=1,
                 row=row)
        MyButton(self.parent, text="Delete", command=self.remove, width=10, col=2, row=row)
        if len(self.datas) == 0:
            self.doNew(withViewUpdate=False)

    def set(self, value):
        oldValue = self.get()
        if oldValue is not None:
            self.prevValue = self.get()
        self.updateAllPath(new=value, old=oldValue)
        self.wValue.set(str(value))
        self.prevValue = value

    def doSelect(self):
        self.updateAllPath(new=self.get(), old=self.prevValue)

        self.prevValue = self.get()
        self.parent.updateView()
        self.update()

    def get(self):
        tmp = self.wValue.get()

        if tmp == '':
            return None
        return int(tmp)

    def remove(self):
        self.datas.pop(self.get())
        self.update()
        if len(self.datas) == 0:
            self.doNew(withViewUpdate=True)
        else:
            self.set(0)
        self.parent.save(saveOnly=True)

    def updateAllPath(self, new, old=None):

        if new is not None:
            for input_ in self.parent.inputs:
                if input_.canSave():
                    if f"[{old}]" in input_.path:
                        if old is not None:
                            input_.path = input_.path.replace(f"[{old}]", f"[{new}]")

    def update(self):
        self.wSelect.configure(values=[str(i) for i in range(len(self.datas))])

        if self.parent.img is not None:
            self.parent.img.update(self.datas[self.get()].path)

    def doNew(self, withViewUpdate=True):
        if self.prevValue is not None:
            self.updateAllPath(new=0, old=self.prevValue)
        newData = self.parent.childClass.from_dict({})

        self.datas.append(newData)
        self.update()
        self.set(len(self.datas) - 1)
        if withViewUpdate:
            self.parent.updateView()


class ParentSelect:
    wSelect: ttk.Combobox = None
    wValue: tkinter.StringVar = None
    wBtnNew: ttk.Button = None
    datas: GetSetDict = None
    parent: Any = None

    def isEmpty(self):
        if self.datas is not None:
            return self.datas.isEmpty()

    def __init__(self, parent, datas, row=0, colspan=1, col=0):
        self.parent = parent
        self.datas = datas
        self.row = row
        self.col = col
        self.wValue = tkinter.StringVar()
        if not self.datas.isEmpty():
            self.wValue.set(self.datas.fromIdx(0).name)

        self.wSelect = ttk.Combobox(self.parent, values=self.datas.keyAsList(), state='readonly',
                                    textvariable=self.wValue, width=15)
        self.wSelect.grid(column=0, row=row, columnspan=colspan, padx=10, pady=10, sticky=W)
        self.wSelect.bind("<<ComboboxSelected>>", self.parent.updateView)
        self.wBtnNew = MyButton(self.parent, text="New", command=self.doNew, width=10, col=1, row=row)
        if self.datas.isEmpty():
            self.doNew(withViewUpdate=False)

    def remove(self):
        self.datas.remove(self.get())
        if self.datas.isEmpty():
            self.doNew(withViewUpdate=True)
        else:
            self.set(self.datas.fromIdx(0).name)
        self.parent.save(saveOnly=True)

    def get(self):
        return self.wValue.get()

    def getObj(self):
        return self.datas.get(self.get())

    def set(self, value):
        self.wValue.set(value)

    def update(self):
        self.wSelect.configure(values=self.datas.keyAsList())

    def doNew(self, withViewUpdate=True):
        newName = str(int(time()))
        newData = self.parent.baseClass.from_dict({"name": newName})
        self.datas.set(newData)
        self.wSelect.config(values=self.datas.keyAsList())
        self.set(newName)


        if withViewUpdate:
            self.parent.updateView()


