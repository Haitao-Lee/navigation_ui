# coding = utf-8
import sys
import vtk
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow
import system_manager
import UI.make_adjustment_ui

#解决屏幕比例不一致的变形问题
QtGui.QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
# 适应高DPI设备
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
# 解决图片在不同分辨率显示模糊问题
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
#不同屏幕分辨率自适应
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    navi_sys = system_manager.system_manager()
    # navi_sys.ui.show()
    navi_sys.ui.showMaximized()
    sys.exit(app.exec_())