from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def createOpacityWidget():
    slider = QSlider(Qt.Horizontal)
    slider.setValue(100) 
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    slider_layout = QHBoxLayout()
    slider_layout.addWidget(slider)
    slider_widget = QWidget()
    slider_widget.setLayout(slider_layout)
    return slider_widget, slider