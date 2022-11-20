import json
from abc import ABC
from tkinter import ttk, W
from typing import Any, Union

from app.components.my_input import MyButton, MySimpleInput, MyImg, MyTextArea
from app.components.my_select import ParentSelect, MyChildSelect
from util.timer import wait_few_sec


class EzView(ttk.Frame, ABC):
    base_class: Any = None
    child_class: Any = None
    app: 'App' = None
    datas: Any = None
    text: MyTextArea = None
    parent_select: ParentSelect = None
    btn_save: MyButton = None
    btn_delete: MyButton = None
    btn_record: MyButton = None
    btn_replay: MyButton = None
    btn_test: MyButton = None
    btn_coor_rectangle: MyButton = None
    test_result: MySimpleInput = None

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

        self.parent_select = ParentSelect(self, datas=self.datas, row=self.rowStart)
        self.text = MyTextArea(self, row=self.rowStart + 2)

        self.rowStart += 3
        self.add_btn_by_hint()
        self.text.set(json.dumps(self.parent_select.get_obj().to_dict(), indent=4))

    def clear(self):
        if self.text is not None:
            self.text.set("")

    def save(self, save_only=False):
        text_data = self.text.get()
        old_obj = self.parent_select.get_obj()
        new_obj = self.base_class.from_dict(json.loads(text_data))

        self.datas.set(new_obj, old_obj.name)
        self.parent_select.update()
        self.parent_select.set(new_obj.name)
        self.app.game.config.saveOnly(self.name, reload=save_only)

    def update_view(self, event=None):
        data = self.parent_select.get_obj()
        self.text.set(json.dumps(data.to_dict(), indent=4))

    def add_btn_by_hint(self):
        for col, hint in enumerate(self.hints):
            if hint == 'save':
                self.btn_save = MyButton(self, "Save", lambda: self.save(), row=self.rowStart, col=col)

            elif hint == 'delete':
                self.btn_delete = MyButton(self, "Delete", lambda: self.parent_select.remove(), row=self.rowStart,
                                           col=col)

            elif hint == 'coor':
                self.btn_coor_rectangle = MyButton(self, "Scan Coor", lambda: self.scan("coor"),
                                                   row=self.rowStart, col=col)
            elif hint == 'rectangle':
                self.btn_coor_rectangle = MyButton(self, "Scan Rectangle", lambda: self.scan("rectangle"),
                                                   row=self.rowStart, col=col)

            elif hint == 'pixel':
                self.btn_coor_rectangle = MyButton(self, "Scan Pixel", lambda: self.scan("pixel"),
                                                   row=self.rowStart, col=col)
            elif hint == 'image':
                self.btn_coor_rectangle = MyButton(self, "Scan Image", lambda: self.scan("image"),
                                                   row=self.rowStart, col=col)
            elif hint == 'mask':
                self.btn_coor_rectangle = MyButton(self, "Scan Mask", lambda: self.scan("mask"),
                                                   row=self.rowStart, col=col)

            elif hint == "test":
                self.btn_test = MyButton(self, "Test", self.test, row=self.rowStart, col=col)

            elif hint == "record":
                self.btn_record = MyButton(self, "Record", lambda: self.record(is_first=True), row=self.rowStart,
                                           col=col)
            elif hint == "replay":
                self.btn_replay = MyButton(self, "Replay", lambda: self.replay(is_first=True), row=self.rowStart,
                                           col=col)
            elif hint == 'minify':
                MyButton(self, "Minify", lambda: self.minify(), row=self.rowStart, col=col)

            # self.testResult = MySimpleInput(self, col=1, row=self.rowStart + 1, colspan=3)

    def minify(self, event=None):
        data = self.parent_select.get_obj()
        t = 0.1
        for action in data.all():
            action.start_at = t
            action.endAt = t + 0.05
            t += 0.1

        self.save()
        self.text.set(json.dumps(data.to_dict(), indent=2))

    def record(self, is_first: bool):
        if is_first:
            self.btn_record.set('Stop Record')
            self.app.game.actionListener.start()
        else:
            self.btn_record.set('Record')
            if not self.app.game.actionListener.stopped:
                self.app.game.actionReplay.stop()
            obj = self.parent_select.get_obj()
            obj.keys = self.app.game.actionListener.selected.keys
            obj.clicks = self.app.game.actionListener.selected.clicks
            self.update_view()
        self.btn_record.config(command=lambda: self.record(is_first=not is_first))

    def replay(self, is_first):
        if is_first:
            self.btn_replay.set('Stop Replay')
            self.app.game.actionReplay.select(self.parent_select.get())
            wait_few_sec(3)
            self.app.game.actionReplay.start()
        else:
            self.btn_replay.set('Replay')
            if not self.app.game.actionReplay.stopped:
                self.app.game.actionReplay.stop()
        self.btn_replay.config(command=lambda: self.replay(is_first=not is_first))
        pass

    def test(self):
        self.save()
        res = self.app.controller.test(config=self.name, hint=self.parent_select.get())
        if res is not None:
            self.test_result.set(str(res))

    def scan(self, config):
        print('scan ' + config)


class BaseView(ttk.Frame, ABC):
    """
    Base class for all views
    """

    base_class: Any = None
    app: 'App' = None
    datas: Any = None
    inputs: list = []
    name: str = ""
    row_start: int = 1
    with_test: bool = True

    def __init__(self, app, name, datas):

        super().__init__(app.view)

        self.grid(sticky=W)
        self.clear()
        self.app = app
        self.name = name
        self.datas = datas
        ttk.Label(self, text=self.name).grid(row=0, column=0, sticky=W)

    def update_view(self):
        for elem in self.inputs:
            if elem.canSave():
                exec(f"elem.set(self.datas.{elem.path})")

    def save_inputs_in_datas(self):
        for input_ in self.inputs:
            if input_.canSave():
                value = input_.get()
                exec(f"self.datas.{input_.path} = value")

    def clear(self):
        self.inputs = []
        for child in self.winfo_children():
            child.destroy()

    def save(self, save_only=False):
        if not save_only:
            self.save_inputs_in_datas()
        self.app.game.config.saveOnly(self.name, reload=True)
        self.update_view()

    def add_btn_by_hint(self, hints):
        for col, hint in enumerate(hints):
            if hint == 'save':
                MyButton(self, "Save", lambda: self.save(), row=self.row_start, col=col)


class BaseViewWithSelect(BaseView, ABC):
    parent_select: ParentSelect = None
    btn_save: MyButton = None
    btn_delete: MyButton = None
    btn_coor: MyButton = None
    btn_coor_rectangle: MyButton = None
    btn_test: MyButton = None
    test_result: MySimpleInput = None

    def __init__(self, app, name, datas):
        super().__init__(app, name, datas)
        self.parent_select = ParentSelect(self, datas=self.datas, row=self.row_start)
        self.row_start += 1

    def update_view(self, event=None):
        data = self.parent_select.get_obj()
        if self.with_test:
            self.test_result.set('')
        for input_ in self.inputs:

            if input_.canSave():
                exec(f'input_.set({input_.path})')

    def save_inputs_in_datas(self):
        data = self.parent_select.get_obj()
        for idx, input_ in enumerate(self.inputs):
            if input_.canSave():
                value = input_.get()
                if idx == 0 and input_.path == 'data.name':
                    self.datas.update_name(data.name, value)
                    self.parent_select.set(value)
                exec(f"{input_.path} = value")

    def add_btn_by_hint(self, hints):

        for col, hint in enumerate(hints):
            if hint == 'save':
                self.btn_save = MyButton(self, "Save", lambda: self.save(), row=self.row_start, col=col)

            elif hint == 'delete':
                self.btn_delete = MyButton(self, "Delete", lambda: self.parent_select.remove(), row=self.row_start,
                                           col=col)

            elif hint == 'coor':
                self.btn_coor_rectangle = MyButton(self, "Scan Coor", lambda: self.scan("coor", first=True),
                                                   row=self.row_start, col=col)
            elif hint == 'rectangle':
                self.btn_coor_rectangle = MyButton(self, "Scan Rectangle", lambda: self.scan("rectangle", first=True),
                                                   row=self.row_start, col=col)
            elif hint == "test":
                self.btn_test = MyButton(self, "Test", self.test, row=self.row_start, col=col)
            elif hint == "mask":
                self.btn_coor_rectangle = MyButton(self, "Scan Mask", lambda: self.scan("mask", first=True),
                                                   row=self.row_start, col=col)
            elif hint == "test mask":
                self.btn_test = MyButton(self, "Test Mask", lambda: self.test_mask(isFirst=True), row=self.row_start,
                                         col=col)
        if self.with_test:
            self.test_result = MySimpleInput(self, col=1, row=self.row_start + 1, colspan=2)

    def test_mask(self, isFirst=False):
        if isFirst:
            self.btn_test.set("Cancel Test")
            self.btn_test.config(command=lambda: self.test_mask(isFirst=False))
            self.app.game.config.maskTest = self.parent_select.get()
        else:
            self.btn_test.set("Test Mask")
            self.btn_test.config(command=lambda: self.test_mask(isFirst=True))
            self.app.game.config.maskTest = None

    def test(self):
        self.save()
        res = self.app.controller.test(config=self.name, hint=self.parent_select.get())
        if res is not None:
            self.test_result.set(str(res))

    def scan(self, hint, first=False):
        if first:
            self.app.game.im_save.reset()
            self.btn_coor_rectangle.set('Cancel')
            self.btn_coor_rectangle.config(command=lambda: self.scan(hint=hint, first=False))
        else:
            self.btn_coor_rectangle.set(f"Scan {hint}")
            self.btn_coor_rectangle.config(command=lambda: self.scan(hint=hint, first=True))
            scanned = None
            if hint == 'rectangle':
                scanned = self.app.game.im_save.getRectangle()
            elif hint == 'coor':
                scanned = self.app.game.im_save.getCoor()
            elif hint == 'mask':
                scanned = self.app.game.im_save.getMask()

            if scanned is not None:
                if hint != "mask":
                    self.save_dict_in_datas(hint, scanned)
                else:
                    self.save_mask_datas(scanned)
                self.update_view()

    def save_mask_datas(self, mask):
        self.save()
        data = self.parent_select.get_obj()
        self.try_match(data, mask, 'lower.r', "['lower']['r']")
        self.try_match(data, mask, 'lower.g', "['lower']['g']")
        self.try_match(data, mask, 'lower.b', "['lower']['b']")
        self.try_match(data, mask, 'upper.r', "['upper']['r']")
        self.try_match(data, mask, 'upper.g', "['upper']['g']")
        self.try_match(data, mask, 'upper.b', "['upper']['b']")
        self.try_match(data, mask, 'region', "['region']")

    def apply_mask(self):
        pass

    def save_dict_in_datas(self, hint, my_dict: dict):
        self.save()
        data = self.parent_select.get_obj()
        for input_ in self.inputs:
            if input_.canSave():
                path_split = input_.path.split('.')
                if len(path_split) > 1:
                    if path_split[-2] == hint:
                        exec(f"{input_.path} = myDict[path_split[-1]]")
                if 'region' in input_.path:
                    exec(f"{input_.path} = myDict['region']")

    def save(self, save_only=False):
        super().save(save_only=save_only)
        self.parent_select.update()

    def try_match(self, data, my_dict: dict, match, dict_path: str):
        new_path = self.get_path_by_match(match)
        if new_path is not None:
            exec(f"{new_path} = myDict{dict_path}")

    def get_path_by_match(self, match):
        for input_ in self.inputs:
            if input_.canSave():

                if match in input_.path:
                    return input_.path
        return None


class BaseViewSelectWithChild(BaseViewWithSelect, ABC):
    child_class: Any = None
    child_select: MyChildSelect = None
    img: Union[MyImg, None] = None
    child_class_list_name = ""

    def __init__(self, app, name, datas):
        super().__init__(app, name, datas)

    def update_view(self, event=None):
        if self.with_test:
            self.test_result.set('')
        data = self.parent_select.get_obj()
        idx = self.child_select.get()
        self.child_select.datas = getattr(data, self.child_class_list_name)
        if len(self.child_select.datas) > 0:
            self.child_select.update()
        else:
            self.child_select.do_new(with_view_update=False)
        # self.img.update(data.images[idx].path)
        for input_ in self.inputs:

            if input_.canSave():
                exec(f'input_.set({input_.path})')

    def init_child_select(self, datas, row=0):
        self.child_select = MyChildSelect(self, datas=datas, row=row)

    def add_btn_by_hint(self, hints):
        for col, hint in enumerate(hints):
            if hint == 'save':
                self.btn_save = MyButton(self, "Save", lambda: self.save(), row=self.row_start, col=col)

            elif hint == 'delete':
                self.btn_delete = MyButton(self, "Delete", lambda: self.parent_select.remove(), row=self.row_start,
                                           col=col)

            elif hint == 'coor':
                self.btn_coor_rectangle = MyButton(self, "Scan Coor", lambda: self.scanCoor("coor", first=True),
                                                   row=self.row_start, col=col)
            elif hint == 'rectangle':
                self.btn_coor_rectangle = MyButton(self, "Scan Rectangle", lambda: self.scan("rectangle", first=True),
                                                   row=self.row_start, col=col)

            elif hint == 'pixel':
                self.btn_coor_rectangle = MyButton(self, "Scan Pixel", lambda: self.scan("pixel", first=True),
                                                   row=self.row_start, col=col)
            elif hint == 'image':
                self.btn_coor_rectangle = MyButton(self, "Scan Image", lambda: self.scan("image", first=True),
                                                   row=self.row_start, col=col)
            elif hint == 'mask':
                self.btn_coor_rectangle = MyButton(self, "Scan Mask", lambda: self.scan("mask", first=True),
                                                   row=self.row_start, col=col)

            elif hint == "test":
                self.btn_test = MyButton(self, "Test", self.test, row=self.row_start, col=col)
            if self.with_test:
                self.test_result = MySimpleInput(self, col=2, row=self.row_start - 1, colspan=2)

    def scan(self, hint, first=False):
        if first:
            self.app.game.im_save.reset()
            self.btn_coor_rectangle.set('Cancel')
            self.btn_coor_rectangle.config(command=lambda: self.scan(hint=hint, first=False))
        else:
            self.btn_coor_rectangle.set(f'Scan {hint}')
            self.btn_coor_rectangle.config(command=lambda: self.scan(hint=hint, first=True))
            if hint in ('rectangle', 'image'):
                scanned = self.app.game.im_save.getRectangle()
            else:

                scanned = self.app.game.im_save.getCoor()
            if scanned is not None and hint not in 'image':
                self.save_dict_in_datas(hint, scanned)
                self.update_view()
            elif scanned is not None and hint == 'image':
                directory = self.parent_select.get()
                name = f"{self.child_select.get()}.png"
                path = f"img/{directory}/{name}"
                self.app.game.im_save.saveImage(scanned, path=f"img/{directory}", name=name)
                self.save_dict_in_datas(hint, {
                    'path': path,
                    'region': scanned['region'],
                })
                self.img.update(path)
                self.update_view()

    def save_dict_in_datas(self, hint, new_obj: dict):
        self.save()
        data = self.parent_select.get_obj()
        idx = self.child_select.get()
        if hint == 'coor':
            self.try_match(data, new_obj, 'coor.x', 'x')
            self.try_match(data, new_obj, 'coor.y', 'y')
        elif hint == 'rectangle':
            self.try_match(data, new_obj, 'rectangle.x', 'x')
            self.try_match(data, new_obj, 'rectangle.y', 'y')
            self.try_match(data, new_obj, 'rectangle.w', 'w')
            self.try_match(data, new_obj, 'rectangle.h', 'h')
        elif hint == 'pixel':
            self.try_match(data, new_obj, 'color.r', "['color']['r']")
            self.try_match(data, new_obj, 'color.g', "['color']['g']")
            self.try_match(data, new_obj, 'color.b', "['color']['b']")
            self.try_match(data, new_obj, 'coor.x', "['x']")
            self.try_match(data, new_obj, 'coor.y', "['y']")
            self.try_match(data, new_obj, 'region', "['region']")
        elif hint == 'image':
            self.try_match(data, new_obj, 'path', "['path']")
            self.try_match(data, new_obj, 'region', "['region']")

    def replace_image(self, data, new_obj):
        pass
