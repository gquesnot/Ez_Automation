import tkinter
from abc import ABC, abstractmethod
from tkinter import FLAT, W
from tkinter import ttk
from typing import Any, List, Union

from app.my_dataclasses import WindowConfig, RegionConfigs, RegionConfig, TcrScanConfigs, TcrScanConfig, VarType, \
    ActionConfigs, ActionConfig, MaskDetectionConfig, MaskDetectionConfigs, ImageMatchConfig, ImageMatchConfigs, \
    PixelConfig, PixelConfigs, ImageMatchItemConfig, GetSetDict, Pixel, PixelConfigType
from my_enum.game_state import GameState
from util.json_function import getJson, toJson


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


class MyBasicSelect:
    label: str = ''
    path: Union[str, None] = None
    wValue: tkinter.StringVar = None
    wSelect: ttk.Combobox = None
    wLabel: ttk.Label = None
    parent = None
    datas: GetSetDict = None

    def __init__(self, parent, label, datas: Any = None, value: Any = None, row=0, col=0, path=None):
        self.parent = parent
        self.label = label
        self.row = row
        self.col = col
        self.path = path

        self.datas = datas
        self.wLabel = ttk.Label(self.parent, text=label, anchor="w", width=len(label) + 3)
        self.wLabel.grid(column=self.col, row=self.row, padx=10, pady=10, sticky=W)
        self.wValue = tkinter.StringVar()
        if not self.datas.isEmpty():
            self.set(value)
        self.wEntry = ttk.Combobox(self.parent, values=self.datas.keyAsList(), textvariable=self.wValue, width=20,
                                   state="readonly")
        self.wEntry.grid(column=self.col + 1, row=self.row, padx=10, pady=10, sticky=W)

    def get(self):
        if self.canSave():
            return self.wValue.get()

    def getObj(self):
        return self.datas.get(self.get())

    def updatePath(self, path):
        self.path = path

    def set(self, value):
        self.wValue.set(value)

    def canSave(self):
        return self.path is not None


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


class MyListSelect:
    datas: list = []
    wSelect: ttk.Combobox = None
    wValue: tkinter.StringVar = None
    btnNew: MyButton = None
    btnDel: MyButton = None

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
        self.wSelect.bind("<<ComboboxSelected>>", self.doSelect)
        btnNew = MyButton(self.parent, text="New", command=lambda: self.doNew(withViewUpdate=True), width=10, col=1,
                          row=row)
        btnNew = MyButton(self.parent, text="Delete", command=self.remove, width=10, col=2, row=row)
        if len(self.datas) == 0:
            self.doNew(withViewUpdate=False)

    def set(self, value):

        self.updateAllPath(self.get(), value)
        self.wValue.set(str(value))
        print(self.get(), value)
        print('pass')

    def get(self):
        tmp = self.wValue.get()

        if tmp == '':
            return None
        return int(tmp)

    def doSelect(self, event):
        pass

    def remove(self, event=None):
        self.datas.pop(self.get())
        if len(self.datas) == 0:
            self.doNew(withViewUpdate=True)
        else:
            self.set(0)
        self.parent.save(saveOnly=True)

    def updateAllPath(self, old, new):
        if old is not None and new is not None:
            for input_ in self.parent.inputs:
                if input_.canSave():
                    if f"[{old}]" in input_.path:
                        input_.path = input_.path.replace(f"[{old}]", f"[{new}]")

    def update(self):
        self.wSelect.configure(values=[str(i) for i in range(len(self.datas))])

    def doNew(self, withViewUpdate=True):
        print(self.parent)
        newData = self.parent.childClass.from_dict({})
        self.datas.append(newData)
        self.update()
        self.set(len(self.datas) - 1)
        if withViewUpdate:
            self.parent.updateView()


class MySelect():
    selected = None

    def __init__(self, parent, label, values, selected, row=0, colspan=1, col=0, isOther=False, parentClass=None):
        self.isOther = isOther
        self.parentClass = parentClass
        self.parent = parent
        self.label = ttk.Label(self.parent, text=label, anchor="w", width=len(label) + 3)
        self.label.grid(column=col, row=row, columnspan=colspan, padx=10, pady=10, sticky=W)
        self.selected = selected
        if self.isOther:
            self.select = ttk.Combobox(self.parent, values=[f"{idx}" for idx, val in enumerate(values)],
                                       state="readonly")
        else:
            self.select = ttk.Combobox(self.parent, values=values, state='readonly')
        if selected is not None:
            if self.isOther:
                self.select.current(int(selected))
            else:
                self.select.current(values.index(selected))
        if self.isOther:
            self.select.bind("<<ComboboxSelected>>", lambda: self.doSelect)
        self.select.grid(column=col + 1, row=row, columnspan=colspan, padx=10, pady=10, sticky=W)
        self.datas = values

        # if self.isOther and self.selected is not None:
        #    self.doSelect()

    def getSelected(self):
        return self.datas[int(self.selected)]

    def doSelect(self, event=None):
        self.selected = self.select.get()
        if self.isOther:
            self.parentClass.selectOther(self.select.get())


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
        self.wSelect.grid(column=col, row=row, columnspan=colspan, padx=10, pady=10, sticky=W)
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
        newData = self.parent.baseClass.from_dict({})
        self.datas.set(newData)
        self.wSelect.config(values=self.datas.keyAsList())
        self.set("")
        if withViewUpdate:
            self.parent.updateView()


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


class Select():
    selected: Union[Any, None] = None
    select: ttk.Combobox = None
    parent: 'BaseViewWithSelect' = None

    def __init__(self, parent, values, selected, row=0):
        self.frame = ttk.Frame(parent)
        self.frame.grid(column=0, row=row, sticky=W, columnspan=2)
        self.selected = selected
        self.parent = parent
        self.values = values
        self.select = ttk.Combobox(self.frame, values=[""] + values.keyAsList(), state='readonly')
        if self.selected is not None:
            self.select.current(values.getIdx(self.selected.name) + 1)
        self.select.grid(column=0, row=0, padx=10, pady=10, sticky=W)
        self.select.bind("<<ComboboxSelected>>", self.doSelect)

        btnNew = MyButton(self.frame, text="New", command=self.doNew, width=10, col=1, row=0)

    def updatesValues(self, values, selected):
        self.values = values
        self.selected = selected
        self.select.configure(values=[""] + values.keyAsList())
        if self.selected is not None:
            self.select.current(values.getIdx(self.selected.name) + 1)
        else:
            self.select.current(0)

    def doNew(self):
        self.select.current(0)
        self.doSelect()

    def doSelect(self, event=None):
        current = self.select.get()
        if current == "":
            self.selected = None
        else:
            self.selected = self.values.get(current)
        self.parent.doSelect(self.selected)


# class Select():
#     inputs = {}
#     btnSelect = None
#     stopped = False
#     select: ttk.Combobox = None
#     lastRow = 0
#     regions = {}
#     frame = None
#     otherFrame = None
#     otherInputs = {}
#     otherRow = 0
#
#     def __init__(self, parent, datas, action, row=0):
#
#         self.action = action
#         self.datas = datas
#         self.row = row
#         self.selected = list(datas.keys())[0] if len(datas) > 0 else None
#         self.parent = parent
#         self.getRegions()
#         self.loadSelect()
#
#     def loadSelect(self):
#         self.parent.clear()
#         self.select = ttk.Combobox(self.parent, values=list(self.datas.keys()), state='readonly')
#         self.select.grid(row=self.row, column=0)
#         btnNew = MyButton(self.parent, text="New",
#                           command=lambda: getattr(self, f"load{self.action.replace(' ', '').capitalize()}")(isNew=True),
#                           col=1, row=self.row)
#         if self.selected is None:
#             self.selected = list(self.datas.keys())[0] if len(self.datas) > 0 else None
#         if self.selected is not None:
#             self.select.current(list(self.datas.keys()).index(self.selected))
#
#         self.select.bind("<<ComboboxSelected>>", self.selectValue)
#         self.frame = ttk.Frame(self.parent)
#         self.frame.grid(column=0, row=self.row + 1, sticky=W)
#         if self.selected is not None:
#             self.selectValue()
#
#     def selectValue(self, event=None):
#         self.clear()
#         self.selected = self.select.get()
#         getattr(self, f"load{self.action.replace(' ', '').capitalize()}")()
#
#     def beforeLoad(self, isNew):
#         if isNew:
#             self.selected = None
#
#     def selectOther(self, idx):
#         self.clearOther()
#         self.otherFrame = ttk.Frame(self.parent)
#         self.otherFrame.grid(column=0, row=self.lastRow + 1, sticky=W)
#
#         if self.otherFrame is not None:
#             selected = self.inputs['otherFrame'].getSelected()
#             self.otherInputs['x'] = MyInput(self.otherFrame, "X", value=selected['x'] if idx is not None else 0,
#                                             row=self.otherRow)
#             self.otherInputs['y'] = MyInput(self.otherFrame, "Y", value=selected['y'] if idx is not None else 0,
#                                             row=self.otherRow + 1)
#             self.otherRow += 2
#             if self.action in "matchImages":
#                 self.otherInputs['w'] = MyInput(self.otherFrame, "Width", value=selected['w'] if idx is not None else 0,
#                                                 row=self.otherRow)
#                 self.otherInputs['h'] = MyInput(self.otherFrame, "Height",
#                                                 value=selected['h'] if idx is not None else 0, row=self.otherRow + 1)
#                 self.otherRow += 2
#
#     def afterLoad(self, isNew):
#         hasOther = self.otherRow != 0
#         MyButton(self.frame if not hasOther else self.otherFrame, "Save", lambda: self.saveObj(True), width=10, col=0,
#                  row=self.lastRow if not hasOther else self.otherRow)
#         if not isNew:
#             MyButton(self.frame if not hasOther else self.otherFrame, "Delete", lambda: self.deleteObj(), width=10,
#                      col=1, row=self.lastRow if not hasOther else self.otherRow)
#         self.replaceBtnSelect(init=True, hasOther=hasOther)
#         MyButton(self.frame if not hasOther else self.otherFrame, "Test", lambda: self.doTest, width=10, col=3,
#                  row=self.lastRow if not hasOther else self.otherRow)
#
#     def loadAction(self, isNew=False):
#         self.beforeLoad(isNew)
#
#         self.inputs["name"] = MyInput(self.frame, "Name", self.selected if not isNew else "", row=0)
#         self.inputs['type'] = MySelect(self.frame, "Type", ["Mouse", "Keyboard"],
#                                        selected=self.datas[self.selected]['type'] if not isNew else "Mouse", row=1)
#         self.inputs['x'] = MyInput(self.frame, "X", self.datas[self.selected]['x'] if not isNew else 0, row=2)
#         self.inputs['y'] = MyInput(self.frame, "Y", self.datas[self.selected]['y'] if not isNew else 0, row=3)
#         self.inputs['key'] = MyInput(self.frame, "Key", self.datas[self.selected]['key'] if not isNew else "", row=4)
#         self.inputs['region'] = MySelect(self.frame, "Regions", self.regions,
#                                          selected=self.datas[self.selected]['region'] if not isNew else self.regions[0],
#                                          row=5)
#         self.inputs['delay'] = MyInput(self.frame, "Delay", self.datas[self.selected]['delay'] if not isNew else 0.1,
#                                        row=6)
#         self.inputs['sleepAfter'] = MyInput(self.frame, "Sleep After",
#                                             self.datas[self.selected]['sleepAfter'] if not isNew else 0.1, row=7)
#         self.lastRow = 8
#         self.afterLoad(isNew)
#
#     def doTest(self):
#         pass
#
#     def newPixel(self):
#         pass
#
#     def loadOtherFrame(self):
#         pass
#
#     def loadPixel(self, isNew=False):
#         self.beforeLoad(isNew)
#         self.inputs["name"] = MyInput(self.frame, "name", self.selected if not isNew else "", row=0)
#         self.inputs['match_type'] = MySelect(self.frame, 'Match Type', values=["OR", "AND"],
#                                              selected=self.datas[self.selected]['match_type'] if not isNew else "OR",
#                                              row=1)
#         self.inputs['otherFrame'] = MySelect(self.frame, 'Pixels',
#                                              self.datas[self.selected]['pixels'] if not isNew else [],
#                                              selected="0" if not isNew else None
#                                              , row=2, col=0, isOther=True, parentClass=self)
#         btn = MyButton(self.frame, "Add", lambda: self.selectOther(None), width=10, col=2, row=2)
#
#         self.lastRow = 3
#         self.selectOther(0)
#         self.afterLoad(isNew)
#
#     def loadMaskDetection(self, isNew=False):
#         self.beforeLoad(isNew)
#
#         self.afterLoad(isNew)
#
#     def getRegions(self):
#         self.regions = ["root"] + list(getJson("region").keys())
#
#     def loadTcrscan(self, isNew=False):
#         self.beforeLoad(isNew)
#         self.inputs['name'] = MyInput(self.frame, 'name', self.selected if not isNew else "", row=0)
#         self.inputs['type'] = MySelect(self.frame, label='type', values=['string', 'int'],
#                                        selected=self.datas[self.selected]['type'] if not isNew else "string", row=1)
#         self.inputs['x'] = MyInput(self.frame, 'x', self.datas[self.selected]['x'] if not isNew else 0, row=2)
#         self.inputs['y'] = MyInput(self.frame, 'y', self.datas[self.selected]['y'] if not isNew else 0, row=3)
#         self.inputs['w'] = MyInput(self.frame, 'w', self.datas[self.selected]['w'] if not isNew else 0, row=4)
#         self.inputs['h'] = MyInput(self.frame, 'h', self.datas[self.selected]['h'] if not isNew else 0, row=5)
#         self.inputs['region'] = MySelect(self.frame, 'region', values=self.regions,
#                                          selected=self.datas[self.selected]['region'] if not isNew else self.regions[0],
#                                          row=6)
#         self.lastRow = 7
#         self.afterLoad(isNew)
#
#     def loadMatchImages(self, isNew=False):
#         self.beforeLoad(isNew)
#         self.inputs['name'] = MyInput(self.frame, 'name', self.selected if not isNew else "", row=0)
#
#         self.afterLoad(isNew)
#
#     def loadRegion(self, isNew=False):
#         self.beforeLoad(isNew)
#
#         self.inputs["name"] = MyInput(self.frame, "name", self.selected if not isNew else "", row=0)
#         self.inputs['x'] = MyInput(self.frame, 'x', self.datas[self.selected]['x'] if not isNew else 0, row=1)
#         self.inputs['y'] = MyInput(self.frame, 'y', self.datas[self.selected]['y'] if not isNew else 0, row=2)
#         self.inputs['w'] = MyInput(self.frame, 'w', self.datas[self.selected]['w'] if not isNew else 0, row=3)
#         self.inputs['h'] = MyInput(self.frame, 'h', self.datas[self.selected]['h'] if not isNew else 0, row=4)
#         self.inputs['ratio'] = MyInput(self.frame, 'ratio', self.datas[self.selected]['ratio'] if not isNew else 1.0,
#                                        row=5)
#         self.lastRow = 6
#         self.afterLoad(isNew)
#
#     def stopScan(self):
#         if self.action in ("region", "matchImages"):
#             tmp = self.parent.parent.game.imSave.getRectangle()
#             if tmp is not None:
#                 self.setValueIfExist(tmp, "x")
#                 self.setValueIfExist(tmp, "y")
#                 self.setValueIfExist(tmp, "w")
#                 self.setValueIfExist(tmp, "h")
#                 if self.action != "region":
#                     self.setValueIfExist(tmp, "region")
#
#         else:
#             tmp = self.parent.parent.game.imSave.getClick()
#             if tmp is not None:
#                 self.setValueIfExist(tmp, "x")
#                 self.setValueIfExist(tmp, "y")
#                 self.setValueIfExist(tmp, "region")
#
#         self.replaceBtnSelect(init=True)
#
#     def initScan(self):
#         self.replaceBtnSelect(init=False)
#         self.parent.parent.game.imSave.resetClick()
#
#     def setValueIfExist(self, datas, key):
#         if key in self.datas:
#             self.datas[key] = datas[key]
#         if key in self.inputs:
#             if type(self.inputs[key]) is MyInput:
#                 self.inputs[key].value.set(datas[key])
#             elif type(self.inputs[key]) is MySelect:
#                 select = self.inputs[key]
#                 select.select.current(select.datas.index(datas[key]))
#
#     def replaceBtnSelect(self, init=True, row=5, hasOther=False):
#         all = ("region", "matchImages", "pixel", "maskDetection", "action", "tcrScan")
#         rectangle = ("region", "matchImages", "tcrScan")
#         click = ("pixel", "maskDetection", "action")
#         if self.action in all:
#
#             if self.btnSelect is not None:
#                 self.btnSelect.destroy()
#                 self.btnSelect = None
#             if not init and self.action in rectangle + click:
#                 self.btnSelect = MyButton(self.frame if not hasOther else self.otherFrame, "Stop", self.stopScan,
#                                           width=20, col=2, row=self.lastRow + self.otherRow)
#             else:
#                 if self.action in rectangle:
#                     name = "Rectangle"
#                 else:
#                     name = "Coor"
#                 self.btnSelect = MyButton(self.frame if not hasOther else self.otherFrame, f"Select {name}",
#                                           self.initScan, width=20, col=2,
#                                           row=self.lastRow + self.otherRow)
#
#     def clearOther(self):
#         self.otherInputs = {}
#         if self.otherFrame is not None:
#             for child in self.otherFrame.winfo_children():
#                 child.destroy()
#             self.otherFrame.destroy()
#             self.otherFrame = None
#         self.otherRow = 0
#
#     def clear(self):
#         self.inputs = {}
#
#         self.btnSelect = None
#         self.clearOther()
#         for child in self.frame.winfo_children():
#             child.destroy()
#
#     def deleteObj(self):
#
#         del self.datas[self.selected]
#         self.saveObj()
#         self.selected = None
#         self.loadSelect()
#
#     def inputsToObj(self):
#         nameChangedOrNew = False
#         name = self.inputs["name"].getValue()
#
#         if self.selected is None or name != self.selected:
#             if name in self.datas:
#                 name = f"new_{str(time())[-6:]}"
#             if self.selected is None:
#                 self.datas[name] = {}
#             else:
#                 self.datas[name] = self.datas[self.selected]
#                 del self.datas[self.selected]
#             self.selected = name
#             nameChangedOrNew = True
#         for k, val in self.inputs.items():
#             if k == "name":
#                 continue
#             if type(val) is MyInput:
#                 self.datas[name][k] = val.getValue()
#             else:
#                 self.datas[name][k] = val.select.get()
#         return nameChangedOrNew
#
#     def saveObj(self, getInputs=False):
#
#         if getInputs:
#             if self.inputsToObj():
#                 self.loadSelect()
#         self.parent.parent.saveDatas(self.action, self.datas)
#         if self.action == "region":
#             self.getRegions()


class BaseView(ttk.Frame, ABC):
    """
    Base class for all views
    """

    baseClass: Any = None
    app: 'App' = None
    datas: Any = None
    inputs: list = []
    name: str = ""
    rowStart: int = 1

    def __init__(self, app, name, datas):

        super().__init__(app.view)

        self.grid(sticky=W)
        self.clear()
        self.app = app
        self.name = name
        self.datas = datas
        ttk.Label(self, text=self.name).grid(row=0, column=0, sticky=W)

    def updateView(self):
        for elem in self.inputs:
            if elem.canSave():
                exec(f"elem.set(self.datas.{elem.path})")

    def saveInputsInDatas(self):
        for input_ in self.inputs:
            if input_.canSave():
                value = input_.get()
                exec(f"self.datas.{input_.path} = value")

    def clear(self):
        self.inputs = []
        for child in self.winfo_children():
            child.destroy()

    def save(self, saveOnly=False):
        if not saveOnly:
            self.saveInputsInDatas()
        self.app.game.config.saveOnly(self.name, reload=True)
        self.updateView()

    def addBtnByHint(self, hints):
        for col, hint in enumerate(hints):
            if hint == 'save':
                MyButton(self, "Save", lambda: self.save(), row=self.rowStart, col=col)


class BaseViewWithSelect(BaseView, ABC):
    """
    Base class for all views with a select button
    """
    selected: Any = None
    select: Union[Select, None] = None
    isEmpty = False
    btnDoCoor: Union[MyButton, None] = None
    btnDoRectangle: Union[MyButton, None] = None
    rowStart: int = 2

    def clear(self):
        self.inputs = {}
        childs = self.winfo_children()

        for idx, child in enumerate(self.winfo_children()):
            if type(child) is not ttk.Frame and idx > 0:
                child.destroy()

    def __init__(self, app, name, datas):
        super().__init__(app, name, datas)
        self.datas = datas

        self.name = name
        self.initSelect()

    def delete(self):
        self.datas.remove(self.selected.name)
        self.datas = self.app.game.config.set(self.name, self.datas, save=True, load=True)
        self.selected = None

        self.select.updatesValues(self.datas, self.selected)
        self.doSelect(None)

        # self.initSelect()

    def test(self):
        pass

    def initSelect(self):
        if self.datas.isEmpty():
            self.isEmpty = True
        else:
            self.selected = self.datas.fromIdx(0)
        if self.select is not None:
            self.select.select.values = [""] + self.datas.keyAsList()
        else:
            ttk.Label(self, text=self.name.upper(), width=15).grid(row=0, column=0, sticky=W)
            self.select = Select(self, self.datas, self.selected, row=1)
        if not self.isEmpty:
            self.select.doSelect()

    def doSelect(self, selected: Any):
        print('pass select')
        if selected is not None:
            self.selected = selected
        else:
            self.selected = None
            self.doNew()
        self.load()

    def actionRectangle(self, cancel=False):
        if self.btnDoRectangle is not None:

            if not cancel:
                self.app.game.imSave.reset()
                self.btnDoRectangle.variable.set("Stop")
                self.btnDoRectangle.config(command=lambda: self.actionRectangle(cancel=True))
            else:
                rectangle = self.app.game.imSave.getRectangle()
                if rectangle is not None:
                    if 'region' in self.inputs:
                        self.inputs['region'].value.set(rectangle['region'])
                    if 'rectangle' in self.inputs:
                        self.inputs['rectangle']['x'].value.set(rectangle['x'])
                        self.inputs['rectangle']['y'].value.set(rectangle['y'])
                        self.inputs['rectangle']['w'].value.set(rectangle['w'])
                        self.inputs['rectangle']['h'].value.set(rectangle['h'])

                self.btnDoRectangle.variable.set("Do Rectangle")
                self.btnDoRectangle.config(command=lambda: self.actionRectangle(cancel=False))

    def actionCoor(self, cancel=False):
        if self.btnDoCoor is not None:
            if not cancel:
                self.app.game.imSave.reset()
                self.btnDoCoor.variable.set("Stop")
                self.btnDoCoor.config(command=lambda: self.actionCoor(cancel=True))
            else:
                coor = self.app.game.imSave.getCoor()
                if coor is not None:

                    if 'coor' in self.inputs:
                        if 'region' in self.inputs['coor']:
                            self.inputs['coor']['region'].value.set(coor['region'])
                        self.inputs['coor']['x'].value.set(coor['x'])
                        self.inputs['coor']['y'].value.set(coor['y'])
                    elif 'pixel' in self.inputs:
                        if 'region' in self.inputs['pixel']:
                            self.inputs['pixel']['region'].value.set(coor['region'])
                        self.inputs['pixel']['coor']['x'].value.set(coor['x'])
                        self.inputs['pixel']['coor']['y'].value.set(coor['y'])
                        self.inputs['pixel']['color']['r'].value.set(coor['color']['r'])
                        self.inputs['pixel']['color']['g'].value.set(coor['color']['g'])
                        self.inputs['pixel']['color']['b'].value.set(coor['color']['b'])

                self.btnDoCoor.variable.set("Do Coor")
                self.btnDoCoor.config(command=lambda: self.actionCoor(cancel=False))

    def doNew(self):
        self.selected = self.baseClass.from_dict({})

    def save(self):
        self.saveInputsInDatas()
        self.datas = self.app.game.config.set(self.name, self.datas, save=True, load=True)
        self.select.updatesValues(self.datas, self.selected)
        self.load()


class BaseViewSelectWithChild(BaseViewWithSelect):
    childClass: Any = None
    selectedChild: Any = None
    childSelect: MyListSelect = None
    selectedChildIdx: Union[int, None] = None
    childsInputs = {}

    def __init__(self, app, name, datas):
        super().__init__(app, name, datas)

    @abstractmethod
    def initChild(self):
        pass

    @abstractmethod
    def doChildDelete(self, idx):
        pass

    @abstractmethod
    def loadChild(self):
        pass

    def clearChilds(self):
        for child in self.childsInputs:
            self.childsInputs[child].destroy()
        self.childsInputs = {}

    def doNewChild(self):
        self.selectedChild = self.childClass.from_dict({})
        self.selected.images.append(self.selectedChild)
        self.selectedChildIdx = len(self.selected.images)
        self.childSelect.updatesValues(self.selected.images, self.selectedChild)
        self.loadChild()

    @abstractmethod
    def doChildSelect(self, idx):
        pass


class BaseViewWithSelect2(BaseView, ABC):
    parentSelect: ParentSelect = None
    btnSave: MyButton = None
    btnDelete: MyButton = None
    btnCoor: MyButton = None
    btnCoorRectangle: MyButton = None
    btnTest: MyButton = None

    def __init__(self, app, name, datas):
        super().__init__(app, name, datas)
        self.parentSelect = ParentSelect(self, datas=self.datas, row=self.rowStart)
        self.rowStart += 1

    def updateView(self, event=None):
        data = self.parentSelect.getObj()
        for input_ in self.inputs:

            if input_.canSave():
                print(input_.path, input_.get())
                exec(f'input_.set({input_.path})')

    def saveInputsInDatas(self):
        data = self.parentSelect.getObj()
        for idx, input_ in enumerate(self.inputs):
            if input_.canSave():
                value = input_.get()
                if idx == 0 and input_.path == 'data.name':
                    self.datas.updateName(data.name, value)
                    self.parentSelect.set(value)
                exec(f"{input_.path} = value")

    def addBtnByHint(self, hints):
        for col, hint in enumerate(hints):
            if hint == 'save':
                self.btnSave = MyButton(self, "Save", lambda: self.save(), row=self.rowStart, col=col)

            elif hint == 'delete':
                self.btnDelete = MyButton(self, "Delete", lambda: self.parentSelect.remove(), row=self.rowStart,
                                          col=col)

            elif hint == 'coor':
                self.btnCoorRectangle = MyButton(self, "Scan Coor", lambda: self.scanCoor("coor", first=True),
                                                 row=self.rowStart, col=col)
            elif hint == 'rectangle':
                self.btnCoorRectangle = MyButton(self, "Scan Rectangle", lambda: self.scan("rectangle", first=True),
                                                 row=self.rowStart, col=col)
            elif hint == "test":
                self.btnTest = MyButton(self, "Test", lambda: self.test(), row=self.rowStart, col=col)

    def test(self):
        print("test")

    def scan(self, hint, first=False):
        if first:
            self.app.game.imSave.reset()
            self.btnCoorRectangle.set('Cancel')
            self.btnCoorRectangle.config(command=lambda: self.scan(hint=hint, first=False))
        else:
            self.btnCoorRectangle.set('Scan Rectangle' if hint == 'rectangle' else 'Scan Coor')
            self.btnCoorRectangle.config(command=lambda: self.scan(hint=hint, first=True))
            if hint == 'rectangle':
                scanned = self.app.game.imSave.getRectangle()
            else:
                scanned = self.app.game.imSave.getCoor()
            if scanned is not None:
                self.saveDictInDatas(hint, scanned)
                self.updateView()

    def saveDictInDatas(self, hint, myDict: dict):
        self.save()
        data = self.parentSelect.getObj()
        for input_ in self.inputs:
            if input_.canSave():
                pathSplit = input_.path.split('.')
                if len(pathSplit) > 1:
                    if pathSplit[-2] == hint:
                        exec(f"{input_.path} = myDict[pathSplit[-1]]")
                if 'region' in input_.path:
                    exec(f"{input_.path} = myDict['region']")

    def save(self, saveOnly=False):
        super().save(saveOnly=saveOnly)
        self.parentSelect.update()


class BVWS2ChildSelect(BaseViewWithSelect2, ABC):
    childClass: Any = None
    childSelect: MyListSelect = None

    def __init__(self, app, name, datas):
        super().__init__(app, name, datas)

    def initChildSelect(self, datas, row=0):
        self.childSelect = MyListSelect(self, datas=datas, row=row)


class MenuT():
    elemToConfig = [
        "Window",
        "Regions",
        "Pixels",
        "Match Images",
        "Tcr Scans",
        "Mask Detections",
        "Actions"
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


class WindowView(BaseView):
    datas: WindowConfig = None

    def __init__(self, app: 'App'):
        super().__init__(app, "window", app.game.config.window)
        self.inputs.append(MyInput(parent=self, label="Name", value=self.datas.name, row=self.rowStart,
                                   path="name"
                                   ))

        self.inputs.append(MyInput(parent=self, label="Cropped Y", value=self.datas.cropped_y, row=self.rowStart + 1,
                                   path="cropped_y"
                                   ))
        self.inputs.append(MyInput(parent=self, label="Height Diff", value=self.datas.h_diff, row=self.rowStart + 2,
                                   path="h_diff"
                                   ))
        self.inputs.append(MyInput(parent=self, label="Cropped X", value=self.datas.cropped_x, row=self.rowStart + 3,
                                   path="cropped_x"
                                   ))
        self.inputs.append(MyInput(parent=self, label="Width Diff", value=self.datas.w_diff, row=self.rowStart + 4,
                                   path="w_diff"
                                   ))
        self.rowStart += 5
        self.addBtnByHint(["save"])


class RegionsView(BaseViewWithSelect2):
    datas: RegionConfigs = None
    baseClass: RegionConfig = RegionConfig

    def __init__(self, app: 'App'):
        super().__init__(app, "regions", app.game.config.regions)
        data = self.parentSelect.getObj()
        self.inputs.append(MyInput(self, label="Name", value=data.name, row=self.rowStart, path="data.name"))
        self.inputs.append(MyInput(self, label="Ratio", value=data.ratio, row=self.rowStart + 1, path="data.ratio"))

        self.inputs.append(
            MyInput(self, label="X", value=data.rectangle.x, row=self.rowStart + 2, path="data.rectangle.x"))
        self.inputs.append(
            MyInput(self, label="Y", value=data.rectangle.y, row=self.rowStart + 3, path="data.rectangle.y"))
        self.inputs.append(
            MyInput(self, label="W", value=data.rectangle.w, row=self.rowStart + 4, path="data.rectangle.w"))
        self.inputs.append(
            MyInput(self, label="H", value=data.rectangle.h, row=self.rowStart + 5, path="data.rectangle.h"))
        self.rowStart += 6
        self.addBtnByHint(["save", "delete", "rectangle", "test"])


class PixelsView(BVWS2ChildSelect):
    baseClass = PixelConfig

    childClass: Pixel = Pixel
    datas: PixelConfigs = None

    def __init__(self, app: 'App'):
        super().__init__(app, "pixels", app.game.config.pixels)
        data = self.parentSelect.getObj()
        self.inputs.append(MyInput(self, label="Name", value=data.name, row=self.rowStart, path="data.name"))
        self.inputs.append(
            MyStringEnumSelect(self, "Type", enum=PixelConfigType, value=data.type, row=self.rowStart + 1,
                               path="data.type"))
        self.initChildSelect(datas=data.pixels, row=self.rowStart + 2)

        idx = self.childSelect.get()
        self.inputs.append(MyInput(self, label="Region", value=data.pixels[idx].region, row=self.rowStart + 3,
                                   path=f"data.pixels[{idx}].region"))
        self.inputs.append(MyInput(self, label="X", value=data.pixels[idx].coor.x, row=self.rowStart + 4,
                                   path=f"data.pixels[{idx}].coor.x"))
        self.inputs.append(MyInput(self, label="Y", value=data.pixels[idx].coor.y, row=self.rowStart + 5,
                                   path=f"data.pixels[{idx}].coor.y"))
        self.inputs.append(MyInput(self, label="R", value=data.pixels[idx].color.r, row=self.rowStart + 6,
                                   path=f"data.pixels[{idx}].color.r"))
        self.inputs.append(MyInput(self, label="G", value=data.pixels[idx].color.g, row=self.rowStart + 7,
                                   path=f"data.pixels[{idx}].color.g"))
        self.inputs.append(MyInput(self, label="B", value=data.pixels[idx].color.b, row=self.rowStart + 8,
                                   path=f"data.pixels[{idx}].color.b"))
        self.rowStart += 9
        self.addBtnByHint(["save", "delete", "coor", "test"])
        # TODO : find a  better way to add new pixel rectangle and coor


class MatchImagesView(BaseViewSelectWithChild):

    def doChildDelete(self, idx):
        self.selected.images.pop(idx - 1)
        self.loadChild()

    baseClass = ImageMatchConfig
    datas: ImageMatchConfigs = None
    selected: ImageMatchConfig = None
    childClass = ImageMatchItemConfig
    selectedChild: ImageMatchItemConfig = None

    def doChildSelect(self, idx):
        self.selectedChild = idx
        if idx is None or len(self.selected.images) == 0:
            self.doNewChild()
        else:

            self.selectedChild = self.selected.images[idx - 1]
        self.loadChild()

    def loadChild(self):

        if self.childsInputs != {}:
            self.childsInputs['path'] = MyInput(self, "Path", self.selectedChild.path, row=self.rowStart + 3)
            self.childsInputs['region'] = MyInput(self, "Region", self.selectedChild.region, row=self.rowStart + 4)
            # self.childsInputs['path'].value.set(self.selectedChild.path)
            # self.childsInputs['region'].value.set(self.selectedChild.region)
        else:
            self.childsInputs['path'] = MyInput(self, "Path", self.selectedChild.path, row=self.rowStart + 3)
            self.childsInputs['region'] = MyInput(self, "Region", self.selectedChild.region, row=self.rowStart + 4)

    def initChild(self):
        if len(self.selected.images) == 0:
            self.doNewChild()

        else:
            self.selectedChild = self.selected.images[0]
        if self.childSelect is not None:
            self.select.select.values = [""] + [str(i) for i in range(len(self.selected.images))]
        else:
            ttk.Label(self, text="Pixels", width=10).grid(row=2, column=0, sticky=W)
            self.childSelect = MyListSelect(self, values=self.selected.images,
                                            selected=1 if len(self.selected.images) > 0 else None,
                                            row=self.rowStart + 2)
        if not self.isEmpty:
            self.childSelect.doSelect()

    def saveInputsInDatas(self):
        pass

    def load(self):
        self.clear()
        self.inputs['name'] = MyInput(self, "Name", self.selected.name, row=self.rowStart)
        self.initChild()
        self.loadChild()
        MyButton(self, "Save", lambda: self.save(), row=self.rowStart + 5, col=0, width=12)
        MyButton(self, "Delete", lambda: self.delete(), row=self.rowStart + 5, col=1, width=12)
        var = tkinter.StringVar()
        var.set("Do Rectangle")
        self.btnDoRectangle = MyButton(self, textvariable=var, command=lambda: self.actionRectangle(cancel=False),
                                       row=self.rowStart + 5, col=2, width=12)
        MyButton(self, "Test", lambda: self.test(), row=self.rowStart + 5, col=3, width=12)

    def __init__(self, app: 'App'):
        super().__init__(app, "matchImages", app.game.config.matchImages)
        self.load()


class TcrScansView(BaseViewWithSelect2):
    datas: TcrScanConfigs = None
    baseClass: TcrScanConfig = TcrScanConfig
    selected: TcrScanConfig = None

    def __init__(self, app: 'App'):
        super().__init__(app, "tcrScans", app.game.config.tcrScans)
        data = self.parentSelect.getObj()
        self.inputs.append(MyInput(self, "Name", data.name, row=self.rowStart, path="data.name"))
        self.inputs.append(
            MyStringEnumSelect(self, "Type", enum=VarType, value=data.type, row=self.rowStart + 1, path="data.type"))
        self.inputs.append(MyInput(self, "Region", data.region, row=self.rowStart + 2, path="data.region"))
        self.inputs.append(MyInput(self, "X", data.rectangle.x, row=self.rowStart + 3, path="data.rectangle.x"))
        self.inputs.append(MyInput(self, "Y", data.rectangle.y, row=self.rowStart + 4, path="data.rectangle.y"))
        self.inputs.append(MyInput(self, "w", data.rectangle.w, row=self.rowStart + 5, path="data.rectangle.w"))
        self.inputs.append(MyInput(self, "h", data.rectangle.h, row=self.rowStart + 6, path="data.rectangle.h"))
        self.rowStart += 7
        self.addBtnByHint(['save', 'delete', 'rectangle', 'test'])


class MaskDetectionsView(BaseViewWithSelect):
    baseClass = MaskDetectionConfig
    selected: MaskDetectionConfig = None
    datas: MaskDetectionConfigs = None

    def saveInputsInDatas(self):
        pass

    def load(self):
        self.clear()

    def __init__(self, app: 'App'):
        super().__init__(app, "MaskDetections", app.game.config.maskDetections)
        self.load()


class ActionsView(BaseViewWithSelect):
    baseClass = ActionConfig
    datas: ActionConfigs = None
    selected: ActionConfig = None

    def saveInputsInDatas(self):
        pass

    def load(self):
        self.clear()

    def __init__(self, app: 'App'):
        super().__init__(app, "Actions", app.game.config.actions)
        self.load()


class MainFrame(tkinter.Frame):
    game = None
    parent: tkinter.Tk = None
    menu: MenuT = None
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
        elif config == "Actions":
            self.app.view.addView(ActionsView(self.app))

    def doAction(self, toDo, state):
        print('doAction', toDo, state)
        if state == "freeze":
            self.app.game.toggleFreeze()
        else:
            self.app.game.setState(GameState[state])
        self.app.menu.rebuildStateMenu()


class App(tkinter.Tk):
    view: MainFrame = None
    game = None
    controller: Controller = None

    def __init__(self, game):
        print('init app')
        super().__init__()
        self.game = game
        self.menu = MenuT(self)

        self.config(menu=self.menu.menu)
        self.title("Bot Control")
        self.geometry("800x700")
        self.resizable(width=False, height=False)
        self.style = ttk.Style(self)
        self.style.theme_use("vista")
        self.controller = Controller(self)
        self.view = MainFrame(self)
        self.view.grid(sticky=W)

    def afterInit(self):
        pass
        # self.config(menu=self.view.menu.menu)

    def jsonNameFromAction(self, action):
        return (action.lower()[0] + action[1:]).replace(" ", "")

    def multipleObjConfig(self, action):
        datas = getJson(action)
        self.select = Select(self.view, datas, action)

    def baseObjConfig(self, action):
        # get json of action with first letter lowered
        datas = getJson(action)
        self.addObjInputs(datas)
        MyButton(self.view, text="Save", command=lambda: self.saveObj(action), row=len(self.inputs) + 1, colspan=2)

    def saveDatas(self, action, datas):
        """
        :param action: json file to save obj
        :param datas: all datas
        :return:
        """
        name = self.jsonNameFromAction(action)
        toJson(action, datas)
        if name == "pixel":
            self.game.dpc.loadPixels()
        elif action == "maskDetection":
            self.game.dpc.loadMaskDetections()
        elif action == "region":
            self.game.regions.dict = datas
            self.game.cv2Controller.refreshRegion = True
            self.game.toggleFreeze(double=True)
        elif name == "tcrScan":
            self.game.dpc.loadTcrScans()
        elif name == "action":
            self.game.actions = datas
        elif name == "matchImages":
            self.game.dpc.loadMatchImages()

    def saveObj(self, action):
        datas = {k: input_.getValue() for k, input_ in self.inputs.items()}
        toJson(action, datas)
        self.game.wc.loadConfig()
        if datas['window_name'] != self.game.wc.window_name:
            datas['window_name'] = self.game.wc.window_name
            toJson(action, datas)
            self.inputs['window_name'].value.set(self.game.wc.window_name)
        self.game.toggleFreeze(double=True)

    def save(self, jsonName, action):
        pass

    def addObjInputs(self, obj):
        i = 0
        for k, v in obj.items():
            self.inputs[k] = MyInput(self.view, f"{k} :", v, row=i)
            i += 1

    def initConfigWindow(self):
        conf = getJson('window')
        self.addObjInputs(conf)
        ttk.Button(self.view, text="Save", command=lambda: print('save'))

    def initConfigRegion(self):
        pass

    def initConfigPixel(self):
        pass

    def initConfigMatchImage(self):
        pass

    def initConfigTcrScan(self):
        pass

    def initConfigMaskDetection(self):
        pass

    def initConfigAction(self):
        pass
