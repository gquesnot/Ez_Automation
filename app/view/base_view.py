import json
from abc import ABC
from tkinter import ttk, W
from typing import Any, Union

from app.components.my_input import MyButton, MySimpleInput, MyImg, MyTextArea
from app.components.my_select import ParentSelect, MyChildSelect


class EzView(ttk.Frame, ABC):
    baseClass: Any = None
    childClass: Any = None
    app: 'App' = None
    datas: Any = None
    text: MyTextArea = None
    parentSelect: ParentSelect = None
    btnSave: MyButton = None
    btnDelete: MyButton = None
    btnTest: MyButton = None
    btnCoorRectangle: MyButton = None
    testResult: MySimpleInput = None
    name: str = ""
    rowStart: int = 1
    hints = ["save", "delete", "test"]

    def __init__(self, app: 'App', datas: Any, name: str):
        super().__init__(app.view)
        self.grid(sticky=W)
        self.app = app
        self.name = name
        self.datas = datas
        ttk.Label(self, text=self.name).grid(row=0, column=0, sticky=W)

        self.parentSelect = ParentSelect(self, datas=self.datas, row=self.rowStart)
        self.text = MyTextArea(self, row=self.rowStart + 1)

        self.rowStart += 2
        self.addBtnByHint()
        self.text.set(json.dumps(self.parentSelect.getObj().to_dict(), indent=4))

    def clear(self):
        if self.text is not None:
            self.text.set("")

    def save(self, saveOnly=False):
        textData = self.text.get()
        data = self.baseClass.from_dict(json.loads(textData))
        self.datas.set(data)

        self.app.game.config.saveOnly(self.name, reload=saveOnly)

    def updateView(self, event=None):
        data = self.parentSelect.getObj()
        self.text.set(json.dumps(data.to_dict(), indent=4))

    def addBtnByHint(self):
        for col, hint in enumerate(self.hints):
            if hint == 'save':
                self.btnSave = MyButton(self, "Save", lambda: self.save(), row=self.rowStart, col=col)

            elif hint == 'delete':
                self.btnDelete = MyButton(self, "Delete", lambda: self.parentSelect.remove(), row=self.rowStart,
                                          col=col)

            elif hint == 'coor':
                self.btnCoorRectangle = MyButton(self, "Scan Coor", lambda: self.scan("coor"),
                                                 row=self.rowStart, col=col)
            elif hint == 'rectangle':
                self.btnCoorRectangle = MyButton(self, "Scan Rectangle", lambda: self.scan("rectangle"),
                                                 row=self.rowStart, col=col)

            elif hint == 'pixel':
                self.btnCoorRectangle = MyButton(self, "Scan Pixel", lambda: self.scan("pixel"),
                                                 row=self.rowStart, col=col)
            elif hint == 'image':
                self.btnCoorRectangle = MyButton(self, "Scan Image", lambda: self.scan("image"),
                                                 row=self.rowStart, col=col)
            elif hint == 'mask':
                self.btnCoorRectangle = MyButton(self, "Scan Mask", lambda: self.scan("mask"),
                                                 row=self.rowStart, col=col)

            elif hint == "test":
                self.btnTest = MyButton(self, "Test", self.test, row=self.rowStart, col=col)
            self.testResult = MySimpleInput(self, col=2, row=self.rowStart - 1, colspan=2)

    def test(self):
        self.save()
        res = self.app.controller.test(config=self.name, hint=self.parentSelect.get())
        if res is not None:
            self.testResult.set(str(res))

    def scan(self, config):
        print('scan ' + config)


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
    withTest: bool = True

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
    parentSelect: ParentSelect = None
    btnSave: MyButton = None
    btnDelete: MyButton = None
    btnCoor: MyButton = None
    btnCoorRectangle: MyButton = None
    btnTest: MyButton = None
    testResult: MySimpleInput = None

    def __init__(self, app, name, datas):
        super().__init__(app, name, datas)
        self.parentSelect = ParentSelect(self, datas=self.datas, row=self.rowStart)
        self.rowStart += 1

    def updateView(self, event=None):
        data = self.parentSelect.getObj()
        if self.withTest:
            self.testResult.set('')
        for input_ in self.inputs:

            if input_.canSave():
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
                self.btnCoorRectangle = MyButton(self, "Scan Coor", lambda: self.scan("coor", first=True),
                                                 row=self.rowStart, col=col)
            elif hint == 'rectangle':
                self.btnCoorRectangle = MyButton(self, "Scan Rectangle", lambda: self.scan("rectangle", first=True),
                                                 row=self.rowStart, col=col)
            elif hint == "test":
                self.btnTest = MyButton(self, "Test", self.test, row=self.rowStart, col=col)
        if self.withTest:
            self.testResult = MySimpleInput(self, col=1, row=self.rowStart + 1, colspan=2)

    def test(self):
        self.save()
        res = self.app.controller.test(config=self.name, hint=self.parentSelect.get())
        if res is not None:
            self.testResult.set(str(res))

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


class BaseViewSelectWithChild(BaseViewWithSelect, ABC):
    childClass: Any = None
    childSelect: MyChildSelect = None
    img: Union[MyImg, None] = None
    childClassListName = ""

    def __init__(self, app, name, datas):
        super().__init__(app, name, datas)

    def updateView(self, event=None):
        if self.withTest:
            self.testResult.set('')
        data = self.parentSelect.getObj()
        idx = self.childSelect.get()
        self.childSelect.datas = getattr(data, self.childClassListName)
        if len(self.childSelect.datas) > 0:
            self.childSelect.update()
        else:
            self.childSelect.doNew(withViewUpdate=False)
        # self.img.update(data.images[idx].path)
        for input_ in self.inputs:

            if input_.canSave():
                exec(f'input_.set({input_.path})')

    def initChildSelect(self, datas, row=0):
        self.childSelect = MyChildSelect(self, datas=datas, row=row)

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

            elif hint == 'pixel':
                self.btnCoorRectangle = MyButton(self, "Scan Pixel", lambda: self.scan("pixel", first=True),
                                                 row=self.rowStart, col=col)
            elif hint == 'image':
                self.btnCoorRectangle = MyButton(self, "Scan Image", lambda: self.scan("image", first=True),
                                                 row=self.rowStart, col=col)
            elif hint == 'mask':
                self.btnCoorRectangle = MyButton(self, "Scan Mask", lambda: self.scan("mask", first=True),
                                                 row=self.rowStart, col=col)

            elif hint == "test":
                self.btnTest = MyButton(self, "Test", self.test, row=self.rowStart, col=col)
            if self.withTest:
                self.testResult = MySimpleInput(self, col=2, row=self.rowStart - 1, colspan=2)

    def scan(self, hint, first=False):
        if first:
            self.app.game.imSave.reset()
            self.btnCoorRectangle.set('Cancel')
            self.btnCoorRectangle.config(command=lambda: self.scan(hint=hint, first=False))
        else:
            self.btnCoorRectangle.set(f'Scan {hint}')
            self.btnCoorRectangle.config(command=lambda: self.scan(hint=hint, first=True))
            if hint in ('rectangle', 'image'):
                scanned = self.app.game.imSave.getRectangle()
            else:

                scanned = self.app.game.imSave.getCoor()
            if scanned is not None and hint not in 'image':
                self.saveDictInDatas(hint, scanned)
                self.updateView()
            elif scanned is not None and hint == 'image':
                directory = self.parentSelect.get()
                name = f"{self.childSelect.get()}.png"
                path = f"img/{directory}/{name}"
                self.app.game.imSave.saveImage(scanned, path=f"img/{directory}", name=name)
                self.saveDictInDatas(hint, {
                    'path': path,
                    'region': scanned['region'],
                })
                self.img.update(path)
                self.updateView()

    def saveDictInDatas(self, hint, newObj: dict):
        self.save()
        data = self.parentSelect.getObj()
        idx = self.childSelect.get()
        if hint == 'coor':
            self.tryMatch(data, newObj,'coor.x', 'x')
            self.tryMatch(data, newObj,'coor.y', 'y')
        elif hint == 'rectangle':
            self.tryMatch(data, newObj,'rectangle.x', 'x')
            self.tryMatch(data, newObj,'rectangle.y', 'y')
            self.tryMatch(data, newObj,'rectangle.w', 'w')
            self.tryMatch(data, newObj,'rectangle.h', 'h')
        elif hint == 'pixel':
            self.tryMatch(data, newObj,'color.r', "['color']['r']")
            self.tryMatch(data, newObj,'color.g', "['color']['g']")
            self.tryMatch(data, newObj,'color.b', "['color']['b']")
            self.tryMatch(data, newObj,'coor.x', "['x']")
            self.tryMatch(data, newObj,'coor.y', "['y']")
            self.tryMatch(data, newObj,'region', "['region']")
        elif hint == 'image':
            self.tryMatch(data, newObj,'path', "['path']")
            self.tryMatch(data, newObj,'region', "['region']")

    def replaceImage(self, data, newObj):
        pass

    def tryMatch(self,data, myDict, match, dictPath):
        newPath = self.getPathByMatch(match)
        if newPath is not None:
            exec(f"{newPath} = myDict{dictPath}")

    def getPathByMatch(self, match):
        for input_ in self.inputs:
            if input_.canSave():

                if match in input_.path:
                    return input_.path
        return None
