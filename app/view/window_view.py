from app.components.my_input import MyInput
from baseclass.my_dataclass.window_config import WindowConfig
from app.view.base_view import BaseView


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
