from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def createVisibleWidget(visible):
    visible_lb = QLabel() # 创建一个label，并将其放置在 QVBoxLayout 中
    if visible:
        visible_lb.setStyleSheet("image: url(:/visible/unvisible.png);")
    else:
        visible_lb.setStyleSheet("image: url(:/visible/visible.png);")
    # visible_btn.setFlat(True)
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(visible_lb.sizePolicy().hasHeightForWidth())
    visible_lb.setSizePolicy(sizePolicy)
    visible_layout = QVBoxLayout()
    visible_layout.addWidget(visible_lb)
    visible_layout.setContentsMargins(0, 0, 0, 0)
    visible_layout.setSpacing(0)
    visible_widget = QWidget()  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
    visible_widget.setLayout(visible_layout)
    return visible_widget