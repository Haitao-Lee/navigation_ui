import UI.ui_all as ui_all
import slot_functions
import config
from functools import partial
import vtkmodules.all as vtk
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Message.print_info as print_info
from config import ALLWIN, AXIAL, SAGITA, CORNAL, VIEW3D
import numpy as np
import Interaction.m_interactorStyle as m_interactorStyle
import landmark
import Visualization.createLine as createLine
import Visualization.createSphere as createSphere
import Visualization.createAxesActor as createAxesActor
import Visualization.createCubeActor as createCubeActor


class system_manager(QThread):
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
        self.probeDeviateMatrix = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.TrackerHostName = None

        
        # adjustment
        self.lookupTable = vtk.vtkLookupTable()
        self.lower2Dvalues = config.lower2Dvalue
        self.upper2Dvalues = config.upper2Dvalue
        self.lower3Dvalues = config.lower3Dvalue
        self.upper3Dvalues = config.upper3Dvalue


        # data
        # 若要添加新的tag，涉及颜色改变的表头请命名为‘Color’，涉及可视化的请命名为‘Visible’
        self.dicoms = []
        self.meshes =[]
        self.mesh_opacity_sliders = []
        self.implants =[]
        self.implant_opacity_sliders = []
        self.ui.implant_tw.setEditTriggers(QTableWidget.DoubleClicked)
        self.tools = []
        self.tool_opacity_sliders = []
        self.landmarks =[]
        self.landmark_opacity_sliders = []
        self.ui.landmark_tw.setEditTriggers(QTableWidget.DoubleClicked)
        self.roms = []
        self.current_dicom_index =None
        self.current_visual_dicom_index =None
        self.current_mesh_index =None
        self.current_implant_index = None
        self.current_tool_index = None
        self.current_landmark_index = None
        self.current_rom_index = None
        
        
        # visulization
        self.dlsplay_status = None     #当前显示状态，widget显示四个窗口还是某一个窗口
        self.cross_line_sign = 1
        self.bot_color = None
        self.top_color = None
        self.box_color = None
        self.LUT2D = None # 设置2D切面窗宽窗位
        self.CTF3D = None # 设置3D体绘制颜色传输函数，窗宽窗位
        self.PWF3D = None # 设置3D体绘制透明传输函数
        self.views = []
        self.vtk_renderWindows = []
        self.renderers = []
        self.contour_renderers = []
        self.styles = []
        self.irens = []
        self.picker = vtk.vtkCellPicker()
        self.lineCenter = np.array([0, 0, 0])
        self.lineActors = [createLine.get_line_actor(self.lineCenter-config.cross_line_length*np.array([1,0,0])/8, self.lineCenter+config.cross_line_length*np.array([1,0,0])/8, color=[0,1,0]),
                           createLine.get_line_actor(self.lineCenter-config.cross_line_length*np.array([0,1,0])/8, self.lineCenter+config.cross_line_length*np.array([0,1,0])/8, color=[0,0,1]),
                           createLine.get_line_actor(self.lineCenter-config.cross_line_length*np.array([0,0,1])/8, self.lineCenter+config.cross_line_length*np.array([0,0,1])/8, color=[1,0,0]),
                           createLine.get_line_actor([self.lineCenter[0], self.lineCenter[1]-config.cross_line_length/2, config.lineActorZOffset], [self.lineCenter[0], self.lineCenter[1]+config.cross_line_length/2, config.lineActorZOffset], color=[0,1,0], linewidth=0.5),
                           createLine.get_line_actor([self.lineCenter[0]-config.cross_line_length/2, self.lineCenter[1], config.lineActorZOffset], [self.lineCenter[0]+config.cross_line_length/2, self.lineCenter[1], config.lineActorZOffset], color=[0,0,1], linewidth=0.5),
                           createLine.get_line_actor([self.lineCenter[1]-config.cross_line_length/2, self.lineCenter[2], config.lineActorZOffset], [self.lineCenter[1]+config.cross_line_length/2, self.lineCenter[2], config.lineActorZOffset], color=[1,0,0], linewidth=0.5),
                           createLine.get_line_actor([self.lineCenter[1], self.lineCenter[2]-config.cross_line_length/2, config.lineActorZOffset], [self.lineCenter[1], self.lineCenter[2]+config.cross_line_length/2, config.lineActorZOffset], color=[0,0,1], linewidth=0.5),
                           createLine.get_line_actor([self.lineCenter[0]-config.cross_line_length/2, self.lineCenter[2], config.lineActorZOffset], [self.lineCenter[0]+config.cross_line_length/2, self.lineCenter[2], config.lineActorZOffset], color=[1,0,0], linewidth=0.5),
                           createLine.get_line_actor([self.lineCenter[0], self.lineCenter[2]-config.cross_line_length/2, config.lineActorZOffset], [self.lineCenter[0], self.lineCenter[2]+config.cross_line_length/2, config.lineActorZOffset], color=[0,1,0], linewidth=0.5)
                          ]
        self.localization_actor = createSphere.get_sphere_actor(createSphere.get_sphere_polydata(np.array([0,0,0]), radius=2))
        self.measure_actors = [createSphere.get_sphere_actor(createSphere.get_sphere_polydata(np.array([0,0,0]), radius=2)), createSphere.get_sphere_actor(createSphere.get_sphere_polydata(np.array([0,0,0]), radius=2))]
        self.measure_sign = 0
        self.measure_pos = [np.array([0, 0, 0]), np.array([0, 0, 0])]
        self.projectActors = []
        self.probAssemble = None
        self.m_3DOrientationWidget = None
        
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
        self.bot_color = config.bottom_3Dcolor
        self.top_color = config.top_3Dcolor
        self.box_color = self.top_color*255
        # 0:transverse view,  1:3d view, 2:sagittal view, 3:coronal view]
        for i in range(4):
            self.views.append(self.ui.ui_displays[i].view)
            self.vtk_renderWindows.append(self.ui.ui_displays[i].view.GetRenderWindow())
            self.renderers.append(vtk.vtkRenderer())
            self.contour_renderers.append(vtk.vtkRenderer())
            self.irens.append(self.vtk_renderWindows[i].GetInteractor())
            if i == 1:
                self.styles.append(vtk.vtkInteractorStyleTrackballCamera()) 
                self.ui.ui_displays[i].box.setStyleSheet("border:None;\n"
                                                      f"background-color: rgb({self.box_color[0]}, {self.box_color[1]}, {self.box_color[2]});")
                self.renderers[i].SetBackground(self.bot_color)              # 设置页面底部颜色值
                self.renderers[i].SetBackground2(self.top_color)    # 设置页面顶部颜色值
                self.renderers[i].SetGradientBackground(1)                  # 开启渐变色背景设置
                self.irens[i].SetInteractorStyle(self.styles[i])
                self.irens[i].SetRenderWindow(self.vtk_renderWindows[i])
                self.vtk_renderWindows[i].AddRenderer(self.renderers[i])
                self.vtk_renderWindows[i].Render() 
                self.irens[i].Initialize()
                self.irens[i].Start()
            else: 
                self.styles.append(vtk.vtkInteractorStyleImage())#.CustomInteractorStyle())
                self.renderers[i].SetBackground(config.initial_2Dcolor)
                self.irens[i].SetInteractorStyle(self.styles[i])
                self.irens[i].SetRenderWindow(self.vtk_renderWindows[i])
                self.vtk_renderWindows[i].AddRenderer(self.renderers[i])
                self.contour_renderers[i].SetActiveCamera(self.renderers[i].GetActiveCamera())
                self.vtk_renderWindows[i].AddRenderer(self.contour_renderers[i])
                self.vtk_renderWindows[i].SetNumberOfLayers(2)
                self.contour_renderers[i].SetLayer(1)
                self.renderers[i].SetLayer(0)
                self.vtk_renderWindows[i].Render()  
                self.irens[i].Start()
        self.LUT2D = vtk.vtkLookupTable()
        self.LUT2D.SetRange(config.lower2Dvalue, config.upper2Dvalue)
        self.LUT2D.SetValueRange(0.0, 1.0)
        self.LUT2D.SetSaturationRange(0.0, 0.0)
        self.LUT2D.SetRampToLinear()
        self.LUT2D.Build()
        self.CTF3D = vtk.vtkColorTransferFunction()
        self.CTF3D.AddRGBPoint(config.lower3Dvalue, config.volume_color1[0], config.volume_color1[1], config.volume_color1[2])
        self.CTF3D.AddRGBPoint((config.lower3Dvalue + config.upper3Dvalue)/2, config.volume_color2[0], config.volume_color2[1], config.volume_color2[2])
        self.CTF3D.AddRGBPoint(config.upper3Dvalue, config.volume_color3[0], config.volume_color3[1], config.volume_color3[2])
        self.PWF3D = vtk.vtkPiecewiseFunction()
        self.PWF3D.AddPoint(config.lower3Dvalue, 1)
        self.PWF3D.AddPoint(config.lower3Dvalue+1, 0.5*config.volume_opacity)
        self.PWF3D.AddPoint((config.lower3Dvalue + config.upper3Dvalue)/2, 0.7*config.volume_opacity) 
        self.PWF3D.AddPoint(config.upper3Dvalue-1, 0.8*config.volume_opacity)
        self.PWF3D.AddPoint(config.upper3Dvalue, config.volume_opacity)
        self.PWF3D.ClampingOff()
        self.renderers[1].AddActor(self.lineActors[0])
        self.renderers[1].AddActor(self.lineActors[1])
        self.renderers[1].AddActor(self.lineActors[2])
        self.add2DLineActors()
        self.irens[0].AddObserver("LeftButtonPressEvent", self.updateSliceByLeftClicking0)
        self.irens[1].AddObserver("LeftButtonPressEvent", self.updateSliceByLeftClicking1)
        self.irens[1].AddObserver("RightButtonPressEvent", self.updateSliceByRightClicking1)
        self.irens[2].AddObserver("LeftButtonPressEvent", self.updateSliceByLeftClicking2)
        self.irens[3].AddObserver("LeftButtonPressEvent", self.updateSliceByLeftClicking3)
        # 设置方向widget
        # 创建一个vtkNamedColors对象
        m_3DAxesActor = createAxesActor.createAxesActor()
        m_3DCubeActor = vtk.vtkAnnotatedCubeActor()	
        m_3DCubeActor.SetScale(10)
        self.m_3DOrientationWidget = createCubeActor.createCubeActor()
        self.m_3DOrientationWidget.SetInteractor(self.irens[1])
        # self.probAssemble = vtk.vtkPropAssembly()
        # self.probAssemble.AddPart(m_3DAxesActor)
        # self.probAssemble.AddPart(m_3DCubeActor)
        # self.m_3DOrientationWidget = vtk.vtkOrientationMarkerWidget()
        # self.m_3DOrientationWidget.SetOrientationMarker(self.probAssemble)
        # self.m_3DOrientationWidget.SetInteractor(self.irens[1])
        # self.m_3DOrientationWidget.SetViewport(0, 0, 0.2, 0.2)
        # self.m_3DOrientationWidget.SetOutlineColor(0, 0, 0)
        self.m_3DOrientationWidget.SetEnabled(1)
        self.m_3DOrientationWidget.InteractiveOff()
        for i in range(len(self.lineActors)):
            self.lineActors[i].SetVisibility(i >= 3)
        for i in range(4):
            self.contour_renderers[i].DrawOn()
            self.contour_renderers[i].Modified()
        self.updateViews()
      
    def resetCamera(self, renderer, ParallelProjection = 0, viewup = None):
        renderer.GetActiveCamera().SetParallelProjection(ParallelProjection)
        renderer.ResetCamera()
        renderer.GetActiveCamera().Zoom(config.zoom)
        if viewup is not None:
            renderer.GetActiveCamera().SetViewUp(viewup)

    def updateViews(self):
        for view in self.views:
            view.update()
    
    
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
        
    def update3DOpacity(self):
        value = self.ui.ui_displays[1].slider.value()
        value = value/100
        if value > 0.98:
            value = 1
        if value < 0.02:
            value = 0
        for mesh in self.meshes:
            mesh.setOpacity(value)
        self.updateViews()
            
    def updateSlice(self, view_num):
        if self.current_visual_dicom_index is None:
            return
        vtk_img = self.dicoms[self.current_visual_dicom_index].getImageData()
        extent = np.array(vtk_img.GetExtent())
        spacing = np.array(vtk_img.GetSpacing())
        origin = np.array(vtk_img.GetOrigin())
        tmp_lineCenter = [0, 0, 0]
        tmp_lineCenter[2] = spacing[2] * (self.ui.ui_displays[0].slider.value()+extent[4]) + origin[2]
        tmp_lineCenter[0] = spacing[0] * (self.ui.ui_displays[2].slider.value()+extent[0]) + origin[0]
        tmp_lineCenter[1] = spacing[1] * (self.ui.ui_displays[3].slider.value()+extent[2]) + origin[1]
        diff = [tmp_lineCenter[0]-self.lineCenter[0], tmp_lineCenter[1]-self.lineCenter[1], tmp_lineCenter[2]-self.lineCenter[2]]
        for i in range(3):
            self.lineActors[i].AddPosition(diff[0], diff[1], diff[2])
        self.lineActors[3].AddPosition(-diff[0], 0, 0)
        self.lineActors[4].AddPosition(0, diff[1], 0)
        self.lineActors[5].AddPosition(0, diff[2], 0)
        self.lineActors[6].AddPosition(diff[1], 0, 0)
        self.lineActors[7].AddPosition(0, diff[2], 0)
        self.lineActors[8].AddPosition(diff[0], 0, 0)
        self.lineCenter = tmp_lineCenter
        self.dicoms[self.current_visual_dicom_index].adjustActors([self.lineCenter[2], self.lineCenter[0], self.lineCenter[1]])
        self.slot_fs.updateProject2D(self, view_num)    
        self.updateViews()
            
    def add2DLineActors(self):
        self.contour_renderers[0].AddActor(self.lineActors[3])
        self.contour_renderers[0].AddActor(self.lineActors[4])
        self.contour_renderers[2].AddActor(self.lineActors[5])
        self.contour_renderers[2].AddActor(self.lineActors[6])
        self.contour_renderers[3].AddActor(self.lineActors[7])
        self.contour_renderers[3].AddActor(self.lineActors[8])
        self.updateViews()
    
    def reposition2DLineActors(self):
        self.lineActors[3].SetPosition(0, 0, config.lineActorZOffset)
        self.lineActors[4].SetPosition(0, 0, config.lineActorZOffset)
        self.lineActors[5].SetPosition(0, 0, config.lineActorZOffset)
        self.lineActors[6].SetPosition(0, 0, config.lineActorZOffset)
        self.lineActors[7].SetPosition(0, 0, config.lineActorZOffset)
        self.lineActors[8].SetPosition(0, 0, config.lineActorZOffset)
        
    def updateSliceByLeftClicking0(self, obj, event):
        if self.current_visual_dicom_index is None or self.cross_line_sign == 0:
            return
        click_pos = self.irens[0].GetEventPosition()
        self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderers[0])
        pos = self.picker.GetPickPosition()
        vtk_img = self.dicoms[self.current_visual_dicom_index].getImageData()
        extent = np.array(vtk_img.GetExtent())
        spacing = np.array(vtk_img.GetSpacing())
        self.ui.ui_displays[2].slider.setValue(int((extent[1] - extent[0])/2 + (-pos[0])/spacing[0]))
        self.ui.ui_displays[3].slider.setValue(int((extent[3] - extent[2])/2 + (pos[1])/spacing[1]))
        if self.ui.location_btn.isChecked():
            self.printInfo(f'Picking the point at: ({self.lineCenter[0]:.3f}, {self.lineCenter[1]:.3f}, {self.lineCenter[2]:.3f})')
            self.localization_actor.SetPosition(self.lineCenter)
            self.views[1].update()
    
    def updateSliceByLeftClicking1(self, obj, event):
        if self.ui.location_btn.isChecked():
            click_pos = self.irens[1].GetEventPosition()
            self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderers[1])
            pos = self.picker.GetPickPosition()
            self.printInfo(f'Picking the point at: ({pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f})')
            self.localization_actor.SetPosition(pos)
            self.views[1].update()
        if self.current_visual_dicom_index is None or self.cross_line_sign !=2:
            return
        click_pos = self.irens[1].GetEventPosition()
        self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderers[1])
        pos = self.picker.GetPickPosition()
        vtk_img = self.dicoms[self.current_visual_dicom_index].getImageData()
        spacing = np.array(vtk_img.GetSpacing())
        self.ui.ui_displays[0].slider.setValue(self.ui.ui_displays[0].slider.value() + int((pos[2] - self.lineCenter[2])/spacing[2]))
        self.ui.ui_displays[2].slider.setValue(self.ui.ui_displays[2].slider.value() + int((pos[0] - self.lineCenter[0])/spacing[0]))
        self.ui.ui_displays[3].slider.setValue(self.ui.ui_displays[3].slider.value() + int((pos[1] - self.lineCenter[1])/spacing[1]))
    
    def updateSliceByRightClicking1(self, obj, event):
        if self.ui.measure_btn.isChecked():
            click_pos = self.irens[1].GetEventPosition()
            self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderers[1])
            pos = self.picker.GetPickPosition()
            self.measure_actors[self.measure_sign].SetPosition(pos)
            self.measure_pos[self.measure_sign] = np.array(pos)
            self.views[1].update()
            self.measure_sign = (self.measure_sign + 1)%2
            self.printInfo(f'The distance of selected points: {np.linalg.norm(self.measure_pos[1] - self.measure_pos[0]):.3f} mm')
     
    def updateSliceByLeftClicking2(self, obj, event):
        if self.current_visual_dicom_index is None or self.cross_line_sign ==0:
            return
        click_pos = self.irens[2].GetEventPosition()
        self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderers[2])
        pos = self.picker.GetPickPosition()
        vtk_img = self.dicoms[self.current_visual_dicom_index].getImageData()
        extent = np.array(vtk_img.GetExtent())
        spacing = np.array(vtk_img.GetSpacing())
        self.ui.ui_displays[3].slider.setValue(int((extent[3] - extent[2])/2 + (pos[0])/spacing[1]))
        self.ui.ui_displays[0].slider.setValue(int((extent[5] - extent[4])/2 + (pos[1])/spacing[2]))
        if self.ui.location_btn.isChecked():
            self.printInfo(f'Picking the point at: ({self.lineCenter[0]:.3f}, {self.lineCenter[1]:.3f}, {self.lineCenter[2]:.3f})')
            self.localization_actor.SetPosition(self.lineCenter)
            self.views[1].update()
        
    def updateSliceByLeftClicking3(self, obj, event):
        if self.current_visual_dicom_index is None or self.cross_line_sign ==0:
            return
        click_pos = self.irens[3].GetEventPosition()
        self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderers[3])
        pos = self.picker.GetPickPosition()
        vtk_img = self.dicoms[self.current_visual_dicom_index].getImageData()
        extent = np.array(vtk_img.GetExtent())
        spacing = np.array(vtk_img.GetSpacing())
        self.ui.ui_displays[2].slider.setValue(int((extent[1] - extent[0])/2 + (pos[0])/spacing[0]))
        self.ui.ui_displays[0].slider.setValue(int((extent[5] - extent[4])/2 + (pos[1])/spacing[2]))
        if self.ui.location_btn.isChecked():
            self.printInfo(f'Picking the point at: ({self.lineCenter[0]:.3f}, {self.lineCenter[1]:.3f}, {self.lineCenter[2]:.3f})')
            self.localization_actor.SetPosition(self.lineCenter)
            self.views[1].update()
    
    def updateSagittalSlice(self, value):
        pass
    
    def updateCornalSlice(self, value):
        pass
    
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
        self.PWF3D.ClampingOff()
        self.updateViews()
            
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
        self.ui.ui_displays[0].slider.valueChanged.connect(partial(self.updateSlice, 0))
        self.ui.ui_displays[1].slider.valueChanged.connect(self.update3DOpacity)
        self.ui.ui_displays[2].slider.valueChanged.connect(partial(self.updateSlice, 2))
        self.ui.ui_displays[3].slider.valueChanged.connect(partial(self.updateSlice, 3))
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
        self.ui.crossline_btn.clicked.connect(partial(self.slot_fs.cross_line,self))
        self.ui.reset_btn.clicked.connect(partial(self.slot_fs.reset,self))
        self.ui.measure_btn.clicked.connect(partial(self.slot_fs.measure, self))
        self.ui.volume_btn.clicked.connect(partial(self.slot_fs.volume_calculation, self))
        self.ui.project_btn.clicked.connect(partial(self.slot_fs.project2D, self))
        self.ui.addDicom_btn.clicked.connect(partial(self.slot_fs.addDicom, self))
        self.ui.deleteDicom_btn.clicked.connect(partial(self.slot_fs.deleteDicom, self))
        self.ui.exportDicom_btn.clicked.connect(partial(self.slot_fs.exportDICOM, self))
        self.ui.addMesh_btn.clicked.connect(partial(self.slot_fs.addMesh, self))
        self.ui.deleteMesh_btn.clicked.connect(partial(self.slot_fs.deleteMesh, self))
        self.ui.exportMesh_btn.clicked.connect(partial(self.slot_fs.exportMesh, self))
        self.ui.addImplant_btn.clicked.connect(partial(self.slot_fs.addImplant, self))
        self.ui.deleteImplant_btn.clicked.connect(partial(self.slot_fs.deleteImplant, self))
        self.ui.exportImplant_btn.clicked.connect(partial(self.slot_fs.exportImplants, self))
        self.ui.addlandmark_btn.clicked.connect(partial(self.slot_fs.addLandmark, self))
        self.ui.deleteLandmark_btn.clicked.connect(partial(self.slot_fs.deleteLandmark, self))
        self.ui.exportLandmark_btn.clicked.connect(partial(self.slot_fs.exportLandmark, self))
        self.ui.addRom__btn.clicked.connect(partial(self.slot_fs.addRom, self))
        self.ui.deleteRom_btn.clicked.connect(partial(self.slot_fs.deleteRom, self))
        self.ui.exportRom_btn.clicked.connect(partial(self.slot_fs.exportRom, self))
        self.ui.addTool_btn.clicked.connect(partial(self.slot_fs.addTool, self))
        self.ui.deleteTool_btn.clicked.connect(partial(self.slot_fs.deleteTool, self))
        self.ui.exportTool_btn.clicked.connect(partial(self.slot_fs.exportTool, self))
        self.ui.volume_cbox.stateChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.mesh_cbox.stateChanged.connect(partial(self.slot_fs.adjust, self))
        self.ui.dicom_tw.cellClicked.connect(partial(self.slot_fs.on_dicom_table_clicked, self))
        self.ui.dicom_tw.itemDoubleClicked.connect(partial(self.slot_fs.on_dicom_table_doubleClicked, self))    
        self.ui.mesh_tw.cellClicked.connect(partial(self.slot_fs.on_mesh_table_clicked, self))  
        self.ui.mesh_tw.customContextMenuRequested.connect(partial(self.slot_fs.on_mesh_table_right_clicked, self))  
        self.ui.landmark_tw.cellClicked.connect(partial(self.slot_fs.on_landmark_table_clicked, self))  
        self.ui.landmark_tw.itemChanged.connect(partial(self.slot_fs.lmtw_cell_data_update, self))  
        self.ui.implant_tw.cellClicked.connect(partial(self.slot_fs.on_implant_table_clicked, self))  
        self.ui.implant_tw.itemChanged.connect(partial(self.slot_fs.iptw_cell_data_update, self))  
        self.ui.rom_tw.cellClicked.connect(partial(self.slot_fs.on_rom_table_clicked, self))  
        self.ui.tool_tw.cellClicked.connect(partial(self.slot_fs.on_tool_table_clicked, self))
        self.ui.ui_displays[0].resetCamera_btn.clicked.connect(partial(self.slot_fs.resetCamera0, self))
        self.ui.ui_displays[1].resetCamera_btn.clicked.connect(partial(self.slot_fs.resetCamera1, self))
        self.ui.ui_displays[2].resetCamera_btn.clicked.connect(partial(self.slot_fs.resetCamera2, self))
        self.ui.ui_displays[3].resetCamera_btn.clicked.connect(partial(self.slot_fs.resetCamera3, self))
        self.ui.ui_displays[0].rotate90_btn.clicked.connect(partial(self.slot_fs.rotate_view0, self))
        self.ui.ui_displays[1].rotate90_btn.clicked.connect(partial(self.slot_fs.rotate_view1, self))
        self.ui.ui_displays[2].rotate90_btn.clicked.connect(partial(self.slot_fs.rotate_view2, self))
        self.ui.ui_displays[3].rotate90_btn.clicked.connect(partial(self.slot_fs.rotate_view3, self))
        self.ui.ui_displays[0].zoom_btn.clicked.connect(partial(self.slot_fs.zoom_view0, self))
        self.ui.ui_displays[1].zoom_btn.clicked.connect(partial(self.slot_fs.zoom_view1, self))
        self.ui.ui_displays[2].zoom_btn.clicked.connect(partial(self.slot_fs.zoom_view2, self))
        self.ui.ui_displays[3].zoom_btn.clicked.connect(partial(self.slot_fs.zoom_view3, self))
        self.ui.volume_cbox.stateChanged.connect(partial(self.slot_fs.change_volume_visual_state, self))
        self.ui.mesh_cbox.stateChanged.connect(partial(self.slot_fs.change_mesh_visual_state, self))
        self.ui.color3D_btn_bot.clicked.connect(partial(self.slot_fs.set3DBackgroundBot, self))
        self.ui.color3D_btn_top.clicked.connect(partial(self.slot_fs.set3DBackgroundTop, self))
        pass
        
        