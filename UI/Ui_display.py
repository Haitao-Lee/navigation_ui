# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\work_and_study\code\navigation\software\SRC\UI\display.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import UI.my_qvtkWidget as my_qvtkWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1055, 789)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("background-color: rgb(100, 100, 100);border:none;")
        self.centralwidget.setObjectName("centralwidget")
        self.central_h_layoout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.central_h_layoout.setContentsMargins(0, 0, 0, 0)
        self.central_h_layoout.setSpacing(0)
        self.central_h_layoout.setObjectName("central_h_layoout")
        self.box = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box.sizePolicy().hasHeightForWidth())
        self.box.setSizePolicy(sizePolicy)
        self.box.setStyleSheet("background-color: rgb(0, 0, 0);border:none;")
        self.box.setTitle("")
        self.box.setFlat(False)
        self.box.setObjectName("box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.box)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.editWidget_box = QtWidgets.QGroupBox(self.box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editWidget_box.sizePolicy().hasHeightForWidth())
        self.editWidget_box.setSizePolicy(sizePolicy)
        self.editWidget_box.setStyleSheet("border:None;")
        self.editWidget_box.setTitle("")
        self.editWidget_box.setFlat(True)
        self.editWidget_box.setObjectName("editWidget_box")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.editWidget_box)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(8)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.zoom_btn = QtWidgets.QPushButton(self.editWidget_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoom_btn.sizePolicy().hasHeightForWidth())
        self.zoom_btn.setSizePolicy(sizePolicy)
        self.zoom_btn.setStyleSheet("image: url(:/display/全屏.png);border:none;")
        self.zoom_btn.setText("")
        self.zoom_btn.setCheckable(True)
        self.zoom_btn.setObjectName("zoom_btn")
        self.horizontalLayout_6.addWidget(self.zoom_btn)
        self.rotate90_btn = QtWidgets.QPushButton(self.editWidget_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rotate90_btn.sizePolicy().hasHeightForWidth())
        self.rotate90_btn.setSizePolicy(sizePolicy)
        self.rotate90_btn.setStyleSheet("image: url(:/display/90.png);\nborder:none;"
"")
        self.rotate90_btn.setText("")
        self.rotate90_btn.setFlat(True)
        self.rotate90_btn.setObjectName("rotate90_btn")
        self.horizontalLayout_6.addWidget(self.rotate90_btn)
        self.resetCamera_btn = QtWidgets.QPushButton(self.editWidget_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetCamera_btn.sizePolicy().hasHeightForWidth())
        self.resetCamera_btn.setSizePolicy(sizePolicy)
        self.resetCamera_btn.setStyleSheet("image: url(:/display/房子.png);\nborder:none;"
"")
        self.resetCamera_btn.setText("")
        self.resetCamera_btn.setFlat(True)
        self.resetCamera_btn.setObjectName("resetCamera_btn")
        self.horizontalLayout_6.addWidget(self.resetCamera_btn)
        self.slider = QtWidgets.QScrollBar(self.editWidget_box)
        self.slider.setStyleSheet("color: rgb(17, 149, 218);")
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.horizontalLayout_6.addWidget(self.slider)
        self.label = QtWidgets.QLabel(self.editWidget_box)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 2)
        self.horizontalLayout_6.setStretch(2, 1)
        self.horizontalLayout_6.setStretch(3, 20)
        self.horizontalLayout_6.setStretch(4, 4)
        self.verticalLayout_2.addWidget(self.editWidget_box)
        self.view = my_qvtkWidget.MyVTKWidget(self.box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.view.setFont(font)
        self.view.setStyleSheet("background-color: rgb(0, 0, 0);border:none;")
        self.view.setObjectName("view")
        self.verticalLayout_2.addWidget(self.view)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 39)
        self.central_h_layoout.addWidget(self.box)
        MainWindow.setCentralWidget(self.centralwidget)
        self.action_open_folder = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\work_and_study\\code\\navigation\\software\\SRC\\UI\\resource/文件夹_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_open_folder.setIcon(icon)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        self.action_open_folder.setFont(font)
        self.action_open_folder.setObjectName("action_open_folder")
        self.action_close = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("c:\\work_and_study\\code\\navigation\\software\\SRC\\UI\\resource/退出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_close.setIcon(icon1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.action_close.setFont(font)
        self.action_close.setObjectName("action_close")
        self.actionopen_file = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("c:\\work_and_study\\code\\navigation\\software\\SRC\\UI\\resource/文件.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionopen_file.setIcon(icon2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.actionopen_file.setFont(font)
        self.actionopen_file.setObjectName("actionopen_file")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.zoom_btn.setToolTip(_translate("MainWindow", "global"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.action_open_folder.setText(_translate("MainWindow", "open folder"))
        self.action_close.setText(_translate("MainWindow", "quit"))
        self.actionopen_file.setText(_translate("MainWindow", "open file"))
import UI.resource.navigation_rc
