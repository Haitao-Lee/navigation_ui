from PyQt5.QtWidgets import QMainWindow
from UI.Ui_adjustment import Ui_MainWindow as ui_adjustment

class adjustment_ui(QMainWindow, ui_adjustment):
    def __init__(self):
        super(adjustment_ui, self).__init__()
        self.setupUi(self)
        # self.setFixedSize(800, 600)

        # # 确保没有设置最小/最大大小
        # self.setMinimumSize(800, 600)
        # self.setMaximumSize(800, 600)