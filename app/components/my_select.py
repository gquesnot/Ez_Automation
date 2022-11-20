import tkinter
from time import time
from tkinter import ttk, W
from typing import Union, Any

from app.components.my_input import MyButton
from baseclass.my_dataclass.base_dataclass import GetSetDict


class MyStringEnumSelect:
    label: str = ''
    path: Union[str, None] = None
    w_value: tkinter.StringVar = None
    w_select: ttk.Combobox = None
    w_label: ttk.Label = None
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
        self.w_label = ttk.Label(self.parent, text=label, anchor="w", width=len(label) + 3)
        self.w_label.grid(column=self.col, row=self.row, padx=10, pady=10, sticky=W)
        self.w_value = tkinter.StringVar()
        self.w_value.set(enum[value])
        self.w_entry = ttk.Combobox(self.parent, values=self.datas, textvariable=self.w_value, width=20,
                                    state="readonly")
        self.w_entry.grid(column=self.col + 1, row=self.row, padx=10, pady=10, sticky=W)

    def get(self):
        if self.canSave():
            return self.enum[self.w_value.get()]

    def updatePath(self, path):
        self.path = path

    def set(self, value):
        self.w_value.set(self.enum[value])

    def canSave(self):
        return self.path is not None


class MyChildSelect:
    datas: list = []
    w_select: ttk.Combobox = None
    w_value: tkinter.StringVar = None
    btn_new: MyButton = None
    btn_del: MyButton = None
    prev_value: int = False

    def __init__(self, parent, datas, row=0):
        self.row = row
        self.parent = parent
        self.datas = datas
        self.w_value = tkinter.StringVar()
        if len(self.datas) > 0:
            self.set(0)
        self.w_select = ttk.Combobox(self.parent, values=[str(i) for i in range(len(self.datas))],
                                     textvariable=self.w_value, state='readonly')
        self.w_select.grid(column=0, row=row, padx=10, pady=10, sticky=W)
        self.w_select.bind("<<ComboboxSelected>>", lambda event: self.do_select())
        MyButton(self.parent, text="New", command=lambda: self.do_new(with_view_update=True), width=10, col=1,
                 row=row)
        MyButton(self.parent, text="Delete", command=self.remove, width=10, col=2, row=row)
        if len(self.datas) == 0:
            self.do_new(with_view_update=False)

    def set(self, value):
        old_value = self.get()
        if old_value is not None:
            self.prev_value = self.get()
        self.update_all_path(new=value, old=old_value)
        self.w_value.set(str(value))
        self.prev_value = value

    def do_select(self):
        self.update_all_path(new=self.get(), old=self.prev_value)

        self.prev_value = self.get()
        self.parent.update_view()
        self.update()

    def get(self):
        tmp = self.w_value.get()

        if tmp == '':
            return None
        return int(tmp)

    def remove(self):
        self.datas.pop(self.get())
        self.update()
        if len(self.datas) == 0:
            self.do_new(with_view_update=True)
        else:
            self.set(0)
        self.parent.save(save_only=True)

    def update_all_path(self, new, old=None):

        if new is not None:
            for input_ in self.parent.inputs:
                if input_.canSave():
                    if f"[{old}]" in input_.path:
                        if old is not None:
                            input_.path = input_.path.replace(f"[{old}]", f"[{new}]")

    def update(self):
        self.w_select.configure(values=[str(i) for i in range(len(self.datas))])

        if self.parent.img is not None:
            self.parent.img.update(self.datas[self.get()].path)

    def do_new(self, with_view_update=True):
        if self.prev_value is not None:
            self.update_all_path(new=0, old=self.prev_value)
        new_data = self.parent.child_class.from_dict({})

        self.datas.append(new_data)
        self.update()
        self.set(len(self.datas) - 1)
        if with_view_update:
            self.parent.update_view()


class ParentSelect:
    w_select: ttk.Combobox = None
    w_value: tkinter.StringVar = None
    w_btn_new: ttk.Button = None
    datas: GetSetDict = None
    parent: Any = None

    def is_empty(self):
        if self.datas is not None:
            return self.datas.is_empty()

    def __init__(self, parent, datas, row=0, colspan=1, col=0):
        self.parent = parent
        self.datas = datas
        self.row = row
        self.col = col
        self.w_value = tkinter.StringVar()
        if not self.datas.is_empty():
            self.w_value.set(self.datas.from_idx(0).name)

        self.w_select = ttk.Combobox(self.parent, values=self.datas.key_as_list(), state='readonly',
                                     textvariable=self.w_value, width=15)
        self.w_select.grid(column=0, row=row, columnspan=colspan, padx=10, pady=10, sticky=W)
        self.w_select.bind("<<ComboboxSelected>>", self.parent.update_view)
        self.w_btn_new = MyButton(self.parent, text="New", command=self.do_new, width=10, col=1, row=row)
        if self.datas.is_empty():
            self.do_new(with_view_update=False)

    def remove(self):
        self.datas.remove(self.get())
        if self.datas.is_empty():
            self.do_new(with_view_update=True)
        else:
            self.set(self.datas.from_idx(0).name)
        self.parent.save(save_only=True)

    def get(self):
        return self.w_value.get()

    def get_obj(self):
        return self.datas.get(self.get())

    def set(self, value):
        self.w_value.set(value)

    def update(self):
        self.w_select.configure(values=self.datas.key_as_list())

    def do_new(self, with_view_update=True):
        new_name = str(int(time()))
        new_data = self.parent.base_class.from_dict({"name": new_name})
        self.datas.set(new_data)
        self.w_select.config(values=self.datas.key_as_list())
        self.set(new_name)

        if with_view_update:
            self.parent.update_view()
