# coding = utf-8
import sys
import vtk
import numpy as np
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from UI.interface_v1_ui import Ui_MainWindow as ui_interface
from UI.make_display_ui import display_ui
from UI.make_adjustment_ui import adjustment_ui
import copy
#from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as QVTKWidget
#import resource.navigation_rc


class ui_all(QMainWindow, ui_interface):
    def __init__(self):
        super(ui_all, self).__init__()
        self.setupUi(self)
        self.setupSplitters()
        self.initVTKview()
        self.initRegisterMark()
        # self.initAdjustment()
        self.initWidget()
        QApplication.processEvents()
    
    def initVTKview(self):
        self.views_layout = [self.view_box0.layout(), self.view_box1.layout(), self.view_box2.layout(), self.view_box3.layout()]
        self.ui_displays = [display_ui(), display_ui(), display_ui(), display_ui()]#,display_ui(), display_ui(), display_ui(), display_ui()] 
        # 0:transverse view,  1:3d view, 2:sagittal view, 3:coronal view]
        for i in range(4):
            if i < 4:
                self.views_layout[i].addWidget(self.ui_displays[i].box)
        self.update()
            
    def initAdjustment(self):
        self.adjustment_ui = adjustment_ui()
        self.adjustment_ui.setFixedSize(900, 600)
        # 确保没有设置最小/最大大小
        self.adjustment_ui.setMinimumSize(900, 600)
        self.adjustment_ui.setMaximumSize(900, 600)
        
        self.adjustment_ui.box2D0.layout().removeWidget(self.adjustment_ui.box2D0)
        self.ui_displays[4].view.resize(299,249)
        self.adjustment_ui.box2D0.layout().addWidget(self.ui_displays[4].view)
        self.adjustment_ui.box3D.layout().removeWidget(self.adjustment_ui.box3D)
        self.ui_displays[5].view.resize(448,288)
        self.adjustment_ui.box3D.layout().addWidget(self.ui_displays[5].view)
        self.adjustment_ui.box2D1.layout().removeWidget(self.adjustment_ui.box2D1)
        self.ui_displays[6].view.resize(299,249)
        self.adjustment_ui.box2D1.layout().addWidget(self.ui_displays[6].view)
        self.adjustment_ui.box2D2.layout().removeWidget(self.adjustment_ui.box2D2)
        self.ui_displays[7].view.resize(299,249)
        self.adjustment_ui.box2D2.layout().addWidget(self.ui_displays[7].view)
        # self.adjustment_ui.box3D.layout().removeWidget(self.adjustment_ui.box3D)
        # self.adjustment_ui.box3D.layout().addWidget(self.ui_displays[5].view)
        # self.adjustment_ui.view3D_layout.addWidget(self.ui_displays[5].view)
        # self.adjustment_ui.views2D_layout.addWidget(self.ui_displays[6].view)
        # self.adjustment_ui.views2D_layout.addWidget(self.ui_displays[7].view)
        # self.adjustment_ui.views2D_layout.setStretch(0, 1)
        # self.adjustment_ui.views2D_layout.setStretch(1, 1)
        # self.adjustment_ui.views2D_layout.setStretch(2, 1)
        
    def initRegisterMark(self):
        # 用的时候根据点数num取出需要的Label:tmp = self.regisMarks[-num:]
        self.regisMarks = [self.regis_mark1, self.regis_mark2, self.regis_mark3, self.regis_mark4, self.regis_mark5, self.regis_mark6, self.regis_mark7, self.regis_mark8, self.regis_mark9, self.regis_mark10, self.regis_mark11, self.regis_mark12 ]
        for r in self.regisMarks:
            r.setVisible(False) 
        pass
    
    def initWidget(self):
        self.info_te.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.dataWidget.tabBar().setExpanding(True)
                
    def setVTKview(self):
        pass
            
    def setupDisplay(self):
        pass
    
    def setupButton(self):
        pass
        # setStyleSheet(
        #     "QPushButton{color: black}"
        #     "QPushButton{font: 22pt \"Agency FB\";\n}"
        #     "QPushButton{border-image: url(image/blue_label.png)}"
        #     "QPushButton:hover{border-image: url(image/blue_label_3.png)}"
        #     "QPushButton:pressed{border-image: url(image/blue_label_2.png)}"
        #     "QPushButton{border-radius:20px;}")
        # self.visual.setStyleSheet("QPushButton{border-radius:20px;background-color: rgb(80, 80, 80);}")
        # self.isolate.setStyleSheet("QPushButton{border-radius:20px;background-color: rgb(80, 80, 80);}")
        # self.predict.setStyleSheet("QPushButton{border-radius:20px;background-color: rgb(80, 80, 80);}")
        # self.model_select.setEditable(True)
        # self.model_select.lineEdit().setReadOnly(True)
        # self.model_select.lineEdit().setAlignment(Qt.AlignCenter)
        # self.modelIdx = 0
        # font = QFont()
        # items = ['finalNet_mean','ResNet18_reg','ResNet18_seg','ResNet34_reg','ResNet34_seg','DenseNet121_reg','DenseNet121_seg', 'DenseNet169_reg','DenseNet169_seg',
        #          'UNet_reg', 'UNet_seg','DenseRegNet_mean', "stRegNet_mean"]
        # # font.setFamily("Times New Roman")
        # # font.setPointSize(16)
        # # font.setBold(True)
        # # font.setWeight(75)
        # self.model_select.addItems(items)
        # self.model_select.setStyleSheet("background-color: rgb(80, 80, 80);\n""font: 75 16pt \"Times New Roman\";\n""font-weight: bold;")
        # # self.model_select.setFont(font)
        # self.model_select.setItemData(self.model_select.currentIndex(), font, role=Qt.FontRole)
        # #self.model_select.setStyleSheet("QCombobox{background-color: rgb(80, 80, 80);}")
        
    def setupSplitters(self):
        pass
        # self.horizonSplitter.setStyleSheet("background-color:rgb(180, 180, 180);border:0px solid green")
        # self.verticalSplitter.setStyleSheet("background-color:rgb(180, 180, 180);border:0px solid green")
        # self.verticalSplitter.setHandleWidth(0)
        # self.verticalSplitter.setChildrenCollapsible(1)
        # self.horizonSplitter.setHandleWidth(0)
        # self.horizonSplitter.setChildrenCollapsible(1)
        # self.verticalSplitter.addWidget(self.working_tree) 
        # self.verticalSplitter.addWidget(self.label_4)
        # self.verticalSplitter.addWidget(self.groupBox_4)
        # self.verticalSplitter.addWidget(self.groupBox)
        # self.verticalSplitter.addWidget(self.groupBox_3)
        # self.working_tree.setColumnWidth(0, 800)
        # self.groupBox_2.hide()
        # self.horizonSplitter.addWidget(self.verticalSplitter)
        # self.horizonSplitter.addWidget(self.main_widget)
        # self.widget.layout().replaceWidget(self.groupBox_5, self.horizonSplitter)
        # self.groupBox_5.hide()
        # self.horizonSplitter.setMouseTracking(True)
        # self.horizonSplitter.setStretchFactor(0, 6)
        # self.horizonSplitter.setStretchFactor(1, 4)
        
    def setupCache(self, direc):
        if not os.path.exists(direc):  
            os.makedirs(direc)
        
