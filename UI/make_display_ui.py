from PyQt5.QtWidgets import QMainWindow
from UI.Ui_display import Ui_MainWindow as ui_display
from PyQt5 import QtWidgets

class display_ui(QMainWindow, ui_display):
    def __init__(self):
        super(display_ui, self).__init__()
        self.setupUi(self)
        # 为了消除不刷新的bug
        self.view.resize(self.view.size())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        self.slider.setStyleSheet("QScrollBar { background: transparent; }")