from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def createColorWidget(color):
    color_lb = QLabel()
    color_lb.setStyleSheet(f"background-color: rgb({color[0]}, {color[1]}, {color[2]});")
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(color_lb.sizePolicy().hasHeightForWidth())
    color_lb.setSizePolicy(sizePolicy)
    color_layout = QVBoxLayout()
    color_layout.addWidget(color_lb)
    color_layout.setContentsMargins(0, 0, 0, 0)
    color_layout.setSpacing(0)
    color_widget = QWidget()  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
    color_widget.setLayout(color_layout)
    return color_widget