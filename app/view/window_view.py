from app.components.my_input import MyInput
from app.view.base_view import BaseView
from baseclass.my_dataclass.window_config import WindowConfig


class WindowView(BaseView):
    datas: WindowConfig = None

    def __init__(self, app: 'App'):
        super().__init__(app, "window", app.game.config.window)
        self.inputs.append(MyInput(parent=self, label="Name", value=self.datas.name, row=self.row_start,
                                   path="name"
                                   ))

        self.inputs.append(MyInput(parent=self, label="Cropped Y", value=self.datas.cropped_y, row=self.row_start + 1,
                                   path="cropped_y"
                                   ))
        self.inputs.append(MyInput(parent=self, label="Height Diff", value=self.datas.h_diff, row=self.row_start + 2,
                                   path="h_diff"
                                   ))
        self.inputs.append(MyInput(parent=self, label="Cropped X", value=self.datas.cropped_x, row=self.row_start + 3,
                                   path="cropped_x"
                                   ))
        self.inputs.append(MyInput(parent=self, label="Width Diff", value=self.datas.w_diff, row=self.row_start + 4,
                                   path="w_diff"
                                   ))
        self.row_start += 5
        self.add_btn_by_hint(["save"])
