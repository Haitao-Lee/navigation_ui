# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\work_and_study\code\navigation\software\SRC\UI\adjustment.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(902, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("background-color: rgb(30, 30,30);\n"
"border:none;\n"
"color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        self.groupBox.setFont(font)
        self.groupBox.setTitle("")
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.views2Dlayout = QtWidgets.QHBoxLayout()
        self.views2Dlayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.views2Dlayout.setSpacing(0)
        self.views2Dlayout.setObjectName("views2Dlayout")
        self.box2D0 = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box2D0.sizePolicy().hasHeightForWidth())
        self.box2D0.setSizePolicy(sizePolicy)
        self.box2D0.setMinimumSize(QtCore.QSize(300, 249))
        self.box2D0.setMaximumSize(QtCore.QSize(300, 249))
        self.box2D0.setTitle("")
        self.box2D0.setObjectName("box2D0")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.box2D0)
        self.horizontalLayout_9.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.openGLWidget_0 = QtWidgets.QOpenGLWidget(self.box2D0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openGLWidget_0.sizePolicy().hasHeightForWidth())
        self.openGLWidget_0.setSizePolicy(sizePolicy)
        self.openGLWidget_0.setMinimumSize(QtCore.QSize(300, 249))
        self.openGLWidget_0.setMaximumSize(QtCore.QSize(300, 249))
        self.openGLWidget_0.setObjectName("openGLWidget_0")
        self.horizontalLayout_9.addWidget(self.openGLWidget_0)
        self.views2Dlayout.addWidget(self.box2D0)
        self.box2D1 = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box2D1.sizePolicy().hasHeightForWidth())
        self.box2D1.setSizePolicy(sizePolicy)
        self.box2D1.setMinimumSize(QtCore.QSize(300, 249))
        self.box2D1.setMaximumSize(QtCore.QSize(300, 249))
        self.box2D1.setTitle("")
        self.box2D1.setObjectName("box2D1")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.box2D1)
        self.horizontalLayout_11.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.openGLWidget_1 = QtWidgets.QOpenGLWidget(self.box2D1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openGLWidget_1.sizePolicy().hasHeightForWidth())
        self.openGLWidget_1.setSizePolicy(sizePolicy)
        self.openGLWidget_1.setMinimumSize(QtCore.QSize(300, 249))
        self.openGLWidget_1.setMaximumSize(QtCore.QSize(300, 249))
        self.openGLWidget_1.setObjectName("openGLWidget_1")
        self.horizontalLayout_11.addWidget(self.openGLWidget_1)
        self.views2Dlayout.addWidget(self.box2D1)
        self.box2D2 = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box2D2.sizePolicy().hasHeightForWidth())
        self.box2D2.setSizePolicy(sizePolicy)
        self.box2D2.setMinimumSize(QtCore.QSize(300, 249))
        self.box2D2.setMaximumSize(QtCore.QSize(300, 249))
        self.box2D2.setTitle("")
        self.box2D2.setObjectName("box2D2")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.box2D2)
        self.horizontalLayout_12.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.openGLWidget_2 = QtWidgets.QOpenGLWidget(self.box2D2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openGLWidget_2.sizePolicy().hasHeightForWidth())
        self.openGLWidget_2.setSizePolicy(sizePolicy)
        self.openGLWidget_2.setMinimumSize(QtCore.QSize(300, 249))
        self.openGLWidget_2.setMaximumSize(QtCore.QSize(300, 249))
        self.openGLWidget_2.setObjectName("openGLWidget_2")
        self.horizontalLayout_12.addWidget(self.openGLWidget_2)
        self.views2Dlayout.addWidget(self.box2D2)
        self.views2Dlayout.setStretch(0, 1)
        self.views2Dlayout.setStretch(1, 1)
        self.views2Dlayout.setStretch(2, 1)
        self.verticalLayout.addLayout(self.views2Dlayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(449, 37))
        self.groupBox_3.setMaximumSize(QtCore.QSize(449, 37))
        self.groupBox_3.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_3.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lower2Dbox = QtWidgets.QSpinBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lower2Dbox.sizePolicy().hasHeightForWidth())
        self.lower2Dbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        self.lower2Dbox.setFont(font)
        self.lower2Dbox.setObjectName("lower2Dbox")
        self.horizontalLayout_3.addWidget(self.lower2Dbox)
        self.lower2Dslider = QtWidgets.QSlider(self.groupBox_3)
        self.lower2Dslider.setOrientation(QtCore.Qt.Horizontal)
        self.lower2Dslider.setObjectName("lower2Dslider")
        self.horizontalLayout_3.addWidget(self.lower2Dslider)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 6)
        self.horizontalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMinimumSize(QtCore.QSize(449, 37))
        self.groupBox_4.setMaximumSize(QtCore.QSize(449, 37))
        self.groupBox_4.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_4.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.upper2Dbox = QtWidgets.QSpinBox(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upper2Dbox.sizePolicy().hasHeightForWidth())
        self.upper2Dbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        self.upper2Dbox.setFont(font)
        self.upper2Dbox.setAutoFillBackground(False)
        self.upper2Dbox.setFrame(True)
        self.upper2Dbox.setObjectName("upper2Dbox")
        self.horizontalLayout_4.addWidget(self.upper2Dbox)
        self.upper2Dslider = QtWidgets.QSlider(self.groupBox_4)
        self.upper2Dslider.setOrientation(QtCore.Qt.Horizontal)
        self.upper2Dslider.setObjectName("upper2Dslider")
        self.horizontalLayout_4.addWidget(self.upper2Dslider)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 6)
        self.horizontalLayout_2.addWidget(self.groupBox_4)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 7)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.box3D = QtWidgets.QGroupBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box3D.sizePolicy().hasHeightForWidth())
        self.box3D.setSizePolicy(sizePolicy)
        self.box3D.setMinimumSize(QtCore.QSize(448, 288))
        self.box3D.setMaximumSize(QtCore.QSize(448, 288))
        self.box3D.setTitle("")
        self.box3D.setObjectName("box3D")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.box3D)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.openGLWidget = QtWidgets.QOpenGLWidget(self.box3D)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openGLWidget.sizePolicy().hasHeightForWidth())
        self.openGLWidget.setSizePolicy(sizePolicy)
        self.openGLWidget.setMinimumSize(QtCore.QSize(448, 288))
        self.openGLWidget.setMaximumSize(QtCore.QSize(488, 288))
        self.openGLWidget.setObjectName("openGLWidget")
        self.horizontalLayout.addWidget(self.openGLWidget)
        self.horizontalLayout_5.addWidget(self.box3D)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setContentsMargins(-1, 20, -1, 40)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_7.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.lower3Dbox = QtWidgets.QSpinBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lower3Dbox.sizePolicy().hasHeightForWidth())
        self.lower3Dbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        self.lower3Dbox.setFont(font)
        self.lower3Dbox.setObjectName("lower3Dbox")
        self.horizontalLayout_7.addWidget(self.lower3Dbox)
        self.lower3Dslider = QtWidgets.QSlider(self.groupBox_5)
        self.lower3Dslider.setOrientation(QtCore.Qt.Horizontal)
        self.lower3Dslider.setObjectName("lower3Dslider")
        self.horizontalLayout_7.addWidget(self.lower3Dslider)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 6)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setMinimumSize(QtCore.QSize(448, 64))
        self.groupBox_6.setMaximumSize(QtCore.QSize(448, 64))
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_8.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.upper3Dbox = QtWidgets.QSpinBox(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upper3Dbox.sizePolicy().hasHeightForWidth())
        self.upper3Dbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        self.upper3Dbox.setFont(font)
        self.upper3Dbox.setObjectName("upper3Dbox")
        self.horizontalLayout_8.addWidget(self.upper3Dbox)
        self.upper3Dslider = QtWidgets.QSlider(self.groupBox_6)
        self.upper3Dslider.setOrientation(QtCore.Qt.Horizontal)
        self.upper3Dslider.setObjectName("upper3Dslider")
        self.horizontalLayout_8.addWidget(self.upper3Dslider)
        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 6)
        self.verticalLayout_2.addWidget(self.groupBox_6)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_10.setContentsMargins(20, -1, 100, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.volumn_check_box = QtWidgets.QCheckBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volumn_check_box.sizePolicy().hasHeightForWidth())
        self.volumn_check_box.setSizePolicy(sizePolicy)
        self.volumn_check_box.setMinimumSize(QtCore.QSize(162, 24))
        self.volumn_check_box.setMaximumSize(QtCore.QSize(162, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        self.volumn_check_box.setFont(font)
        self.volumn_check_box.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.volumn_check_box.setObjectName("volumn_check_box")
        self.horizontalLayout_10.addWidget(self.volumn_check_box)
        self.mesh_check_box = QtWidgets.QCheckBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mesh_check_box.sizePolicy().hasHeightForWidth())
        self.mesh_check_box.setSizePolicy(sizePolicy)
        self.mesh_check_box.setMinimumSize(QtCore.QSize(162, 24))
        self.mesh_check_box.setMaximumSize(QtCore.QSize(162, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        self.mesh_check_box.setFont(font)
        self.mesh_check_box.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.mesh_check_box.setObjectName("mesh_check_box")
        self.horizontalLayout_10.addWidget(self.mesh_check_box)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.volumn_check_box.setText(_translate("MainWindow", "Volume"))
        self.mesh_check_box.setText(_translate("MainWindow", "Mesh"))
