from PyQt5.QtWidgets import QMainWindow
from Ui_display import Ui_MainWindow as ui_display

class display_ui(QMainWindow, ui_display):
    def __init__(self):
        super(display_ui, self).__init__()
        self.setupUi(self)