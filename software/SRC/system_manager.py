import UI.ui_all as ui_all
import slot_functions
import config
from functools import partial
import vtkmodules.all as vtk
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Message.print_info as print_info
from config import ALLWIN, TRANSS, SAGITA, VIEW3D
import numpy as np


class system_manager():
    def __init__(self):
        super(system_manager, self).__init__()
        # ui
        self.ui = ui_all.ui_all()
        self.slot_fs = slot_functions.slot_functions()
        self.showProgress(0)
        
        # thread
        self.signal_thread = QThread() # connect成功后才启动
        
        
        # timer
        self.signal_timer = QTimer()
        self.regis_timer = QTimer()
        
        
        # setting
        self.connections = None
        self.robotics = None
        self.probeDeviateMatrix = None
        self.TrackerHostName = None

        
        # adjustment
        self.lookupTable = vtk.vtkLookupTable()
        self.lower2Dvalues = config.lower2Dvalue
        self.upper2Dvalues = config.upper2Dvalue
        self.lower3Dvalues = config.lower3Dvalue
        self.upper3Dvalues = config.upper3Dvalue


        # data
        self.dicoms = []
        self.meshs =[]
        self.implants =[]
        self.tools = []
        self.landmarks =[]
        self.roms = []
        
        
        # visulization
        self.dlsplay_status = None     #当前显示状态，widget显示四个窗口还是某一个窗口
        self.bot_color = None
        self.top_color = None
        self.box_color = None
        self.LUT2D = None # 设置2D切面窗宽窗位
        self.CTF3D = None # 设置3D体绘制颜色传输函数，窗宽窗位
        self.PWF3D = None # 设置3D体绘制透明传输函数
        self.views = []
        self.vtk_renderWindows = []
        self.renderers = []
        self.styles = []
        self.irens = []
        
        
        # setup
        self.initVTKProperty()
        self.setupConnections()       
    
    
    # infomation
    def printInfo(self, message):
        print_info.print_info(self.ui.info_te, '--'+message)
        
    def showProgress(self, value):
        if value >= 100:
            value = 100
        elif value < 0:
            value = 0
        self.ui.progressBar.setValue(value)
        if self.ui.progressBar.value() == 100:
            self.ui.progressBar.setValue(0)
        
    def ProgressStart(self):
        self.showProgress(0)
        for i in range(config.pg_start):
            self.showProgress(i)
            
    def ProgressMiddle(self):
        for i in range(self.ui.progressBar.value(), config.pg_middle):
            self.showProgress(i)
            
    def ProgressEnd(self):
        for i in range(self.ui.progressBar.value(), config.pg_end+1):
            self.showProgress(i)
    
    
    # visualization
    def initVTKProperty(self):
        self.dlsplay_status = ALLWIN            #当前显示状态，widget显示四个窗口还是某一个窗口
        self.bot_color = np.array([1, 1, 1])
        self.top_color = np.array([0.529, 0.8078, 0.92157])
        self.box_color = self.top_color*255
        # 0:transverse view,  1:3d view, 2:sagittal view, 3:coronal view]
        for i in range(4):
            self.views.append(self.ui.ui_displays[i].view)
            self.vtk_renderWindows.append(self.ui.ui_displays[i].view.GetRenderWindow())
            self.renderers.append(vtk.vtkRenderer())
            self.irens.append(vtk.vtkRenderWindowInteractor())
            self.styles.append(vtk.vtkInteractorStyleTrackballCamera()) 
            # 3d窗口设置渐变色
            if i == 1:
                self.ui.ui_displays[i].box.setStyleSheet("border:None;\n"
                                                      f"background-color: rgb({self.box_color[0]}, {self.box_color[1]}, {self.box_color[2]});")
                self.renderers[i].SetBackground(self.bot_color)              # 设置页面底部颜色值
                self.renderers[i].SetBackground2(self.top_color)    # 设置页面顶部颜色值
                self.renderers[i].SetGradientBackground(1)                  # 开启渐变色背景设置
            else: 
                self.renderers[i].SetBackground(0, 0, 0)
            self.irens[i].SetInteractorStyle(self.styles[i])
            self.irens[i].SetRenderWindow(self.vtk_renderWindows[i])
            self.vtk_renderWindows[i].AddRenderer(self.renderers[i])
            # self.irens[i].Initialize()   
            # self.irens[i].Start()
            self.vtk_renderWindows[i].Render()  
        self.LUT2D = vtk.vtkLookupTable()
        self.LUT2D.SetRange(config.lower2Dvalue, config.upper2Dvalue)
        self.LUT2D.SetValueRange(0.0, 1.0)
        self.LUT2D.SetSaturationRange(0.0, 0.0)
        self.LUT2D.SetRampToLinear()
        self.LUT2D.Build()
        self.CTF3D = vtk.vtkColorTransferFunction()
        self.CTF3D.AddRGBPoint(config.lower3Dvalue, config.volume_color1[0], config.volume_color1[1], config.volume_color1[2])
        self.CTF3D.AddRGBPoint((config.lower3Dvalue + config.upper3Dvalue)/2, config.volume_color2[0], config.volume_color2[1], config.volume_color2[2])
        self.CTF3D.AddRGBPoint(config.upper3Dvalue, config.volume_color2[0], config.volume_color3[1], config.volume_color3[2])
        self.PWF3D = vtk.vtkPiecewiseFunction()
        self.PWF3D.AddPoint(config.lower3Dvalue, 1)
        self.PWF3D.AddPoint(config.lower3Dvalue+1, 0.5*config.volume_opacity)
        self.PWF3D.AddPoint((config.lower3Dvalue + config.upper3Dvalue)/2, 0.7*config.volume_opacity) 
        self.PWF3D.AddPoint(config.upper3Dvalue-1, 0.8*config.volume_opacity)
        self.PWF3D.AddPoint(config.upper3Dvalue, config.volume_opacity)
      
    # synchronization
    def updateLower2D(self, value):
        max_val = self.ui.upper2Dslider.value()
        val = min(max_val, value)
        self.ui.lower2Dbox.setValue(val)
        self.ui.lower2Dslider.setValue(val)
        self.updateProperty()
    
    def updateUpper2D(self, value):
        min_val = self.ui.lower2Dslider.value()
        val = max(min_val, value)
        self.ui.upper2Dbox.setValue(val)
        self.ui.upper2Dslider.setValue(val)
        self.updateProperty()
    
    def updateLower3D(self, value):
        max_val = self.ui.upper3Dslider.value()
        val = min(max_val, value)
        self.ui.lower3Dbox.setValue(val)
        self.ui.lower3Dslider.setValue(val)
        self.updateProperty()
    
    def updateUpper3D(self, value):
        min_val = self.ui.lower3Dslider.value()
        val = max(min_val, value)
        self.ui.upper3Dbox.setValue(val)
        self.ui.upper3Dslider.setValue(val)
        self.updateProperty()
        
    def update3DOpacity(self, value):
        # self.printInfo(str(value))
        for mesh in self.meshs:
            mesh.setOpacity(value)
        for view in self.views:
            view.update()
    
    def updateProperty(self):
        self.LUT2D.SetRange(self.ui.lower2Dbox.value(), self.ui.upper2Dbox.value())
        self.CTF3D.RemoveAllPoints()
        self.CTF3D.AddRGBPoint(self.ui.lower3Dbox.value(), config.volume_color1[0], config.volume_color1[1], config.volume_color1[2])
        self.CTF3D.AddRGBPoint((self.ui.lower3Dbox.value() + self.ui.upper3Dbox.value())/2, config.volume_color2[0], config.volume_color2[1], config.volume_color2[2])
        self.CTF3D.AddRGBPoint(self.ui.upper3Dbox.value(), config.volume_color2[0], config.volume_color3[1], config.volume_color3[2])
        self.PWF3D.RemoveAllPoints()
        self.PWF3D.AddPoint(self.ui.lower3Dbox.value(), 1)
        self.PWF3D.AddPoint(self.ui.lower3Dbox.value()+1, 0.5*config.volume_opacity)
        self.PWF3D.AddPoint((self.ui.lower3Dbox.value() + self.ui.upper3Dbox.value())/2, 0.7*config.volume_opacity) 
        self.PWF3D.AddPoint(self.ui.upper3Dbox.value()-1, 0.8*config.volume_opacity)
        self.PWF3D.AddPoint(self.ui.upper3Dbox.value(), config.volume_opacity)
        for view in self.views:
            view.update()
        
                
    # signals and slots
    def setupConnections(self):
        self.ui.lower2Dbox.valueChanged.connect(self.updateLower2D)
        self.ui.lower2Dslider.valueChanged.connect(self.updateLower2D)
        self.ui.upper2Dbox.valueChanged.connect(self.updateUpper2D)
        self.ui.upper2Dslider.valueChanged.connect(self.updateUpper2D)
        self.ui.lower3Dbox.valueChanged.connect(self.updateLower3D)
        self.ui.lower3Dslider.valueChanged.connect(self.updateLower3D)
        self.ui.upper3Dbox.valueChanged.connect(self.updateUpper3D)
        self.ui.upper3Dslider.valueChanged.connect(self.updateUpper3D)
        self.ui.ui_displays[1].slider.valueChanged.connect(self.update3DOpacity)
        self.ui.file_btn.clicked.connect(partial(self.slot_fs.import_file, self))
        self.ui.folder_btn.clicked.connect(partial(self.slot_fs.import_folder, self))
        self.ui.save_all_btn.clicked.connect(partial(self.slot_fs.save_all, self))
        self.ui.setting_btn.clicked.connect(partial(self.slot_fs.open_setting, self))
        self.ui.quit_btn.clicked.connect(partial(self.slot_fs.quit_system,self))
        self.ui.connect_btn.clicked.connect(partial(self.slot_fs.conect2ndi, self))
        self.ui.registration_btn.clicked.connect(partial(self.slot_fs.registration,self))
        self.ui.callibration_btn.clicked.connect(partial(self.slot_fs.calibration, self))
        self.ui.robotics_btn.clicked.connect(partial(self.slot_fs.conect2robo, self))
        self.ui.location_btn.clicked.connect(partial(self.slot_fs.localization,self))
        self.ui.undo_btn.clicked.connect(partial(self.slot_fs.undo,self))
        self.ui.reset_btn.clicked.connect(partial(self.slot_fs.reset,self))
        self.ui.measure_btn.clicked.connect(partial(self.slot_fs.measure, self))
        self.ui.show3d_btn.clicked.connect(partial(self.slot_fs.show3D, self))
        self.ui.project_btn.clicked.connect(partial(self.slot_fs.project2D, self))
        self.ui.addDicom_btn.clicked.connect(partial(self.slot_fs.addDicom, self))
        self.ui.deleteDicom_btn.clicked.connect(partial(self.slot_fs.deleteDicom, self))
        self.ui.addMesh_btn.clicked.connect(partial(self.slot_fs.addMesh, self))
        self.ui.deleteMesh_btn.clicked.connect(partial(self.slot_fs.deleteMesh, self))
        self.ui.addImplant_btn.clicked.connect(partial(self.slot_fs.addImplant, self))
        self.ui.deleteImplant_btn.clicked.connect(partial(self.slot_fs.deleteImplant, self))
        self.ui.addlandmark_btn.clicked.connect(partial(self.slot_fs.addLandmark, self))
        self.ui.deleteLandmark_btn.clicked.connect(partial(self.slot_fs.deleteLandmark, self))
        self.ui.addTool_btn.clicked.connect(partial(self.slot_fs.addTool, self))
        self.ui.deleteTool_btn.clicked.connect(partial(self.slot_fs.deleteTool, self))
        self.ui.lower2Dslider.valueChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.upper2Dslider.valueChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.lower3Dslider.valueChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.upper3Dslider.valueChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.lower2Dbox.valueChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.upper2Dbox.valueChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.lower3Dbox.valueChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.upper3Dbox.valueChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.volume_cbox.stateChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.mesh_cbox.stateChanged.connect(partial(self.slot_fs.adjust, self))    
        pass
        
        