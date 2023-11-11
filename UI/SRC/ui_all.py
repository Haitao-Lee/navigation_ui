# coding = utf-8
import sys
import vtk
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from Ui_interface_v1 import Ui_MainWindow as ui_interface
from config import ALLWIN, TRANSS, SAGITA, VIEW3D
from make_display_ui import display_ui
#from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as QVTKWidget
#import resource.navigation_rc


class ui_all(QMainWindow, ui_interface):
    def __init__(self):
        super(ui_all, self).__init__()
        self.setupUi(self)
        self.setupSplitters()
        self.initVTKview()
        QApplication.processEvents()
    
    def initVTKview(self):
        self.dlsplay_status = ALLWIN            #当前显示状态，widget显示四个窗口还是某一个窗口
        self.views_layout = [self.view_box0.layout(), self.view_box1.layout(), self.view_box2.layout(), self.view_box3.layout()]
        self.ui_displays = [display_ui(), display_ui(), display_ui(), display_ui()] 
        self.vtk_rederWinbdows = []
        self.renderers = []
        self.styles = []
        self.irens = []
        # 0:transverse view,  1:3d view, 2:sagittal view, 3:coronal view]
        for i in range(4):
            self.vtk_rederWinbdows.append(self.ui_displays[i].view.GetRenderWindow())
            self.views_layout[i].addWidget(self.ui_displays[i].centralwidget)
            self.renderers.append(vtk.vtkRenderer())
            self.irens.append(vtk.vtkRenderWindowInteractor())
            self.styles.append(vtk.vtkInteractorStyleTrackballCamera()) 
            # 3d窗口设置渐变色
            if i == 1:
                self.renderers[i].SetBackground(1.0, 1.0, 1.0)              # 设置页面底部颜色值
                self.renderers[i].SetBackground2(0.529, 0.8078, 0.92157)    # 设置页面顶部颜色值
                self.renderers[i].SetGradientBackground(1)                  # 开启渐变色背景设置
            else: 
                self.renderers[i].SetBackground(0, 0, 0)
            self.irens[i].SetInteractorStyle(self.styles[i])
            self.irens[i].SetRenderWindow(self.vtk_rederWinbdows[i])
            self.vtk_rederWinbdows[i].AddRenderer(self.renderers[i])
            # self.irens[i].Initialize()
            # self.vtk_rederWinbdows[i].Render()   
            # self.irens[i].Start()
                
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
        
