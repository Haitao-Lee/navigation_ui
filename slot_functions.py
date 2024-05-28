from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import numpy as np
from vtk.util import numpy_support
import itk
from config import ALLWIN, AXIAL, SAGITA, CORNAL, VIEW3D
import ImportAndSave.importDicom as importDicom
import ImportAndSave.importImplant as importImplant
import ImportAndSave.importIni as importIni
import ImportAndSave.importMesh as importMesh
import ImportAndSave.importTool as importTool
import ImportAndSave.importTxt as importTxt
import Geometry.volumeOfMesh as volumeOfMesh
import dicom as m_dicom
import mesh as m_mesh
import implant as m_implant
import landmark as m_landmark
import rom as m_rom
import tool as m_tool
import SimpleITK as sitk
import Adjustment.get_pixels_hu as get_pixels_hu
import copy
import config
import vtk
import Visualization.createColorWidget as createColorWidget
import Visualization.createVisibleWidget as createVisibleWidget
import Visualization.createOpacityWidget as createOpacityWidget
import Adjustment.rotateImage as rotateImage
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import Visualization.createPrjActor as createPrjActor
import util
from functools import partial
import Geometry.dcmCenter as dcmCenter
import Visualization.createSphere as createSphere
import ImportAndSave.saveSTL as saveSTL
import ImportAndSave.saveImplant as saveImplant
import ImportAndSave.saveSetting as saveSetting
import ImportAndSave.saveROM as saveROM
import ImportAndSave.saveDicom as saveDicom
import shutil


class slot_functions(QThread):
    """
    初始化slot_functions类的实例。
    
    这个构造函数没有参数，并且没有返回值。
    它主要用来初始化类的内部状态。
    """
    def __init__(self):
        # 调用父类的构造函数来确保正确的初始化
        super(slot_functions, self).__init__()
        
    def addTableDicoms(self, sysman, new_dicom):
        """
        向系统管理器中添加一个新的DICOM项，并在UI的表格中显示相关信息。
        
        :param sysman: 系统管理器对象，包含DICOM数据和UI界面控制。
        :param new_dicom: 一个新的DICOM数据项，包含DICOM的相关信息。
        """
        # 计算当前表格行数，以便在末尾插入新行
        current_row = len(sysman.dicoms)
        # 将新的DICOM数据添加到系统管理器的DICOM列表中
        sysman.dicoms.append(new_dicom)
        # 在UI的DICOM表格中插入新行
        sysman.ui.dicom_tw.insertRow(current_row)
        # 为新插入的行设置姓名、年龄、分辨率和文件路径项
        # 设置姓名项
        nameItem = QTableWidgetItem(sysman.dicoms[-1].name)
        nameItem.setTextAlignment(0x0004 | 0x0080)
        nameItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sysman.ui.dicom_tw.setItem(current_row, 0, nameItem)
        # 设置年龄项
        ageItem = QTableWidgetItem(sysman.dicoms[-1].age)
        ageItem.setTextAlignment(0x0004 | 0x0080)
        ageItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sysman.ui.dicom_tw.setItem(current_row, 1, ageItem)
        # 设置分辨率项
        resolutionItem = QTableWidgetItem(str(sysman.dicoms[-1].resolution[0]) + "x" + str(sysman.dicoms[-1].resolution[1]) + "x" + str(sysman.dicoms[-1].resolution[2]))
        resolutionItem.setTextAlignment(0x0004 | 0x0080)
        resolutionItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sysman.ui.dicom_tw.setItem(current_row, 2, resolutionItem)
        # 设置文件路径项
        pathItem = QTableWidgetItem(sysman.dicoms[-1].path)
        pathItem.setTextAlignment(0x0004 | 0x0080)
        pathItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sysman.ui.dicom_tw.setItem(current_row, 3, pathItem)
        # 调整表格列宽，以适应其中内容的宽度
        for j in range(sysman.ui.dicom_tw.columnCount()):
            max_width = 0
            for i in range(sysman.ui.dicom_tw.rowCount()):
                item = sysman.ui.dicom_tw.item(i, j)
                if item:
                    text_width = sysman.ui.dicom_tw.fontMetrics().boundingRect(item.text()).width()
                    if text_width > max_width:
                        max_width = text_width*config.text_margin
            sysman.ui.dicom_tw.setColumnWidth(j, max(max_width, config.min_margin))

    def addTableMesh(self, sysman, newMesh):
        """
        向系统管理器中添加一个新的网格对象，并在UI的表格视图中显示相关信息。

        :param sysman: 系统管理器对象，负责管理和维护场景中的所有网格。
        :param newMesh: 新的网格对象，包含网格的基本信息如名称、路径、颜色、透明度等。
        """
        # 计算新网格应该插入的行号
        current_row = len(sysman.meshes)
        # 将新网格添加到系统管理器的网格列表中
        sysman.meshes.append(newMesh)
        # 在UI的表格视图中插入新行
        sysman.ui.mesh_tw.insertRow(current_row)
        
        # 为新网格创建可见性、颜色和透明度的UI组件
        visible_widget = createVisibleWidget.createVisibleWidget(sysman.meshes[-1].visible)
        color_widget = createColorWidget.createColorWidget(np.array(sysman.meshes[-1].color)*255)
        opacity_widget, opacity_slider = createOpacityWidget.createOpacityWidget()
        
        # 创建并设置名称单元格，包括对齐方式和交互功能
        nameItem = QTableWidgetItem(sysman.meshes[-1].name)
        nameItem.setTextAlignment(0x0004 | 0x0080)
        nameItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sysman.ui.mesh_tw.setItem(current_row, 0, nameItem)
        
        # 将可见性、透明度和颜色的UI组件设置到对应的表格单元格中
        sysman.ui.mesh_tw.setCellWidget(current_row, 1, visible_widget)
        sysman.ui.mesh_tw.setCellWidget(current_row, 2, opacity_widget)
        sysman.ui.mesh_tw.setCellWidget(current_row, 3, color_widget)
        
        # 将透明度滑块添加到系统管理器的滑块列表中，用于后续操作
        sysman.mesh_opacity_sliders.append(opacity_slider)
        # 绑定透明度滑块值变化事件，用于更新网格的透明度
        opacity_slider.valueChanged.connect(partial(sysman.slot_fs.updateMeshOpacity, sysman))
        
        # 创建并设置路径单元格，与名称单元格设置类似
        pathItem = QTableWidgetItem(sysman.meshes[-1].path)
        pathItem.setTextAlignment(0x0004 | 0x0080)
        pathItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sysman.ui.mesh_tw.setItem(current_row, 4, pathItem)
        
        # 根据表格中各列内容的长度动态调整列宽度，确保内容能完全显示
        for j in range(sysman.ui.mesh_tw.columnCount()):
            max_width = 0
            for i in range(sysman.ui.mesh_tw.rowCount()):
                item = sysman.ui.mesh_tw.item(i, j)
                if item:
                    text_width = sysman.ui.mesh_tw.fontMetrics().boundingRect(item.text()).width()
                    if text_width > max_width:
                        max_width = text_width*config.text_margin
            sysman.ui.mesh_tw.setColumnWidth(j, max(max_width, config.min_margin))
        
        # 渲染新添加的网格
        self.renderMeshes(sysman.meshes[-1], sysman)
        
    def addTableImplant(self, sysman, newImplant):
        try:
            current_row = len(sysman.implants)
            sysman.implants.append(newImplant)
            # 更新UI中的列表
            sysman.ui.implant_tw.insertRow(current_row)
            visible_widget = createVisibleWidget.createVisibleWidget(sysman.implants[-1].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
            color_widget = createColorWidget.createColorWidget(np.array(sysman.implants[-1].color)*255)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
            opacity_widget, opacity_slider = createOpacityWidget.createOpacityWidget()
            startItem = QTableWidgetItem(f"{sysman.implants[-1].start[0]}, {sysman.implants[-1].start[1]}, {sysman.implants[-1].start[2]}")
            startItem.setTextAlignment(0x0004 | 0x0080)
            sysman.ui.implant_tw.setItem(current_row, 0, startItem)
            sysman.ui.implant_tw.item(current_row, 0).setFlags(sysman.ui.implant_tw.item(current_row, 0).flags() | Qt.ItemIsEditable)
            endItem = QTableWidgetItem(f"{sysman.implants[-1].end[0]}, {sysman.implants[-1].end[1]}, {sysman.implants[-1].end[2]}")
            endItem.setTextAlignment(0x0004 | 0x0080)
            sysman.ui.implant_tw.setItem(current_row, 1, endItem)
            sysman.ui.implant_tw.item(current_row, 1).setFlags(sysman.ui.implant_tw.item(current_row, 1).flags() | Qt.ItemIsEditable)
            radiusItem = QTableWidgetItem(f"{sysman.implants[-1].radius}")
            radiusItem.setTextAlignment(0x0004 | 0x0080)
            sysman.ui.implant_tw.setItem(current_row, 2, radiusItem)
            sysman.ui.implant_tw.item(current_row, 2).setFlags(sysman.ui.implant_tw.item(current_row, 2).flags() | Qt.ItemIsEditable)
            sysman.ui.implant_tw.setCellWidget(current_row, 3, color_widget)
            sysman.ui.implant_tw.setCellWidget(current_row, 4, visible_widget) 
            sysman.ui.implant_tw.setCellWidget(current_row, 5, opacity_widget)
            sysman.implant_opacity_sliders.append(opacity_slider)
            opacity_slider.valueChanged.connect(partial(sysman.slot_fs.updateImplantOpacity, sysman))
            # 设置列宽度以适应每列中各自字符串的长度
            for j in range(sysman.ui.implant_tw.columnCount()):
                max_width = 0
                for i in range(sysman.ui.implant_tw.rowCount()):
                    item = sysman.ui.implant_tw.item(i, j)
                    if item:
                        text_width = sysman.ui.implant_tw.fontMetrics().boundingRect(item.text()).width()
                        if text_width > max_width:
                            max_width = text_width*config.text_margin
                sysman.ui.implant_tw.setColumnWidth(j, max(max_width, config.min_margin))
            self.renderImplants(sysman.implants[-1], sysman)
        except ValueError:
            QMessageBox.warning(sysman.ui, 'Warning', 'Implant error!', QMessageBox.Ok)
            sysman.printInfo("Invalid string format for float conversion! Please check your implant file!")
            
    def addTableLandmark(self, sysman, newLandmark):
        current_row = len(sysman.landmarks)
        sysman.landmarks.append(newLandmark)
        # 更新UI中的列表
        sysman.ui.landmark_tw.insertRow(current_row)
        visible_widget = createVisibleWidget.createVisibleWidget(sysman.landmarks[-1].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
        color_widget = createColorWidget.createColorWidget(np.array(sysman.landmarks[-1].color)*255)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
        opacity_widget, opacity_slider = createOpacityWidget.createOpacityWidget()
        scalarItem = QTableWidgetItem(f"{sysman.landmarks[-1].scalar[0]}, {sysman.landmarks[-1].scalar[1]}, {sysman.landmarks[-1].scalar[2]}")
        scalarItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.landmark_tw.setItem(current_row, 0, scalarItem)
        sysman.ui.landmark_tw.item(current_row, 0).setFlags(sysman.ui.landmark_tw.item(current_row, 0).flags() | Qt.ItemIsEditable)
        sysman.ui.landmark_tw.setCellWidget(current_row, 1, color_widget)
        sysman.ui.landmark_tw.setCellWidget(current_row, 2, visible_widget) 
        sysman.ui.landmark_tw.setCellWidget(current_row, 3, opacity_widget) 
        sysman.landmark_opacity_sliders.append(opacity_slider)
        opacity_slider.valueChanged.connect(partial(sysman.slot_fs.updateLandmarkOpacity, sysman))
        radiusItem = QTableWidgetItem(f"{config.lm_radius}")
        radiusItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.landmark_tw.setItem(current_row, 4, radiusItem)
        sysman.ui.landmark_tw.item(current_row, 4).setFlags(sysman.ui.landmark_tw.item(current_row, 4).flags() | Qt.ItemIsEditable)
        # 设置列宽度以适应每列中各自字符串的长度
        for j in range(sysman.ui.landmark_tw.columnCount()):
            max_width = 0
            for i in range(sysman.ui.landmark_tw.rowCount()):
                item = sysman.ui.landmark_tw.item(i, j)
                if item:
                    text_width = sysman.ui.landmark_tw.fontMetrics().boundingRect(item.text()).width()
                    if text_width > max_width:
                        max_width = text_width*config.text_margin
            sysman.ui.landmark_tw.setColumnWidth(j, max(max_width, config.min_margin))
        self.renderLandmarks(sysman.landmarks[-1], sysman)
            
    def addTableTool(self, sysman, newTool):
        current_row = len(sysman.tools)
        sysman.tools.append(newTool)
        sysman.ui.tool_tw.insertRow(current_row)
        # 更新UI中的列表
        visible_widget = createVisibleWidget.createVisibleWidget(sysman.tools[-1].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
        color_widget = createColorWidget.createColorWidget(np.array(sysman.tools[-1].color)*255)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
        opacity_widget, opacity_slider = createOpacityWidget.createOpacityWidget()
        nameItem = QTableWidgetItem(sysman.tools[-1].name)
        nameItem.setTextAlignment(0x0004 | 0x0080)
        nameItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sysman.ui.tool_tw.setItem(current_row, 0, nameItem)
        sysman.ui.tool_tw.setCellWidget(current_row, 1, visible_widget)
        sysman.ui.tool_tw.setCellWidget(current_row, 2, opacity_widget)
        sysman.ui.tool_tw.setCellWidget(current_row, 3, color_widget)
        sysman.tool_opacity_sliders.append(opacity_slider)
        opacity_slider.valueChanged.connect(partial(sysman.slot_fs.updateToolOpacity, sysman))
        pathItem = QTableWidgetItem(sysman.tools[-1].path)
        pathItem.setTextAlignment(0x0004 | 0x0080)
        pathItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sysman.ui.tool_tw.setItem(current_row, 4, pathItem)
        # 设置列宽度以适应每列中各自字符串的长度
        for j in range(sysman.ui.tool_tw.columnCount()):
            max_width = 0
            for i in range(sysman.ui.tool_tw.rowCount()):
                item = sysman.ui.tool_tw.item(i, j)
                if item:
                    text_width = sysman.ui.tool_tw.fontMetrics().boundingRect(item.text()).width()
                    if text_width > max_width:
                        max_width = text_width*config.text_margin
            sysman.ui.tool_tw.setColumnWidth(j, max(max_width, config.min_margin))
            
    def addTableRom(self, sysman, newRom):
        current_row = len(sysman.roms)
        sysman.roms.append(newRom)
        sysman.ui.rom_tw.insertRow(current_row)
        nameItem = QTableWidgetItem(sysman.roms[-1].name)
        nameItem.setTextAlignment(0x0004 | 0x0080)
        nameItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sysman.ui.rom_tw.setItem(current_row, 0, nameItem)
        pathItem = QTableWidgetItem(sysman.roms[-1].path)
        pathItem.setTextAlignment(0x0004 | 0x0080)
        pathItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        sysman.ui.rom_tw.setItem(current_row, 1, pathItem)
        # 设置列宽度以适应每列中各自字符串的长度
        for j in range(sysman.ui.rom_tw.columnCount()):
            max_width = 0
            for i in range(sysman.ui.rom_tw.rowCount()):
                item = sysman.ui.rom_tw.item(i, j)
                if item:
                    text_width = sysman.ui.rom_tw.fontMetrics().boundingRect(item.text()).width()
                    if text_width > max_width:
                        max_width = text_width*config.text_margin
            sysman.ui.rom_tw.setColumnWidth(j, max(max_width, config.min_margin))
            
    def addSystemDicoms(self, path, sysman):
        sysman.ui.setEnabled(False)
        dicom_series, images = importDicom.importDicom(path)
        sysman.ui.setEnabled(True)
        if images is None:
            sysman.printInfo("There is no dicom file in the folder:" + path)
            return False
        # 获取患者姓名
        patient_name = 'unknown'
        patient_age = 'unknown'
        if 'PatientName' in dicom_series[0]:
            patient_name = str(dicom_series[0].PatientName)
        # 获取患者年龄
        if 'PatientAge' in dicom_series[0]:
            patient_age = dicom_series[0].PatientAge
        image_array = sitk.GetArrayFromImage(images)
        origin = images.GetOrigin() 
        spacing = images.GetSpacing()
        size = images.GetSize()
        if (0x0018, 0x0050) in dicom_series[0]:
            spacing = (spacing[0], spacing[1],  float(dicom_series[0][(0x0018, 0x0050)].value))
        # 创建VTK图像数据
        vtk_image = vtk.vtkImageData()
        vtk_image.SetDimensions(size[0],size[1],size[2])
        vtk_image.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)
        QCoreApplication.processEvents()
        if origin[1] != 0: # 判定是否需要倒过来的判据, 经过多个例子试出来的，暂时不清楚原因
            image_array  = image_array[::-1,:,:]
            # 创建一个平移变换
            extent = vtk_image.GetExtent()
            origin = (origin[0], origin[1], origin[2] + spacing[2]*(extent[4] - extent[5]))
        vtk_image.SetOrigin(origin[0], origin[1], origin[2])
        vtk_image.SetSpacing(spacing[0], spacing[1], spacing[2])
        vtk_array = numpy_support.numpy_to_vtk(image_array.ravel(), deep=True)
        vtk_image.GetPointData().SetScalars(vtk_array) # 将NumPy数组数据复制到VTK图像数据中
        QCoreApplication.processEvents()
        new_dicom = m_dicom.dicom(arrayData=image_array, imageData=vtk_image, Name=patient_name, Age=patient_age, resolution=image_array.shape, filePath=path)
        QCoreApplication.processEvents()
        new_dicom.createActors(sysman.LUT2D, sysman.CTF3D, sysman.PWF3D)
        self.addTableDicoms(sysman, new_dicom)     
        return True  
    
    def addSystemSTL(self, path, sysman):
        new_stl = importMesh.importSTL(path)
        path = path.replace("\\", "/")
        name = path.split("/")[-1].split('.')[0]
        newMesh = m_mesh.mesh(polydata=new_stl, Name=name, filePath=path, color=config.mesh_colors[len(sysman.meshes)%(len(config.mesh_colors)-1)])
        self.addTableMesh(sysman, newMesh)
    
    def addSystemOBJ(self, path, sysman):
        new_stl = importMesh.importOBJ(path)
        path = path.replace("\\", "/")
        name = path.split("/")[-1].split('.')[0]
        newMesh = m_mesh.mesh(polydata=new_stl, Name=name, filePath=path, color=config.mesh_colors[len(sysman.meshes)%(len(config.mesh_colors)-1)])
        self.addTableMesh(sysman, newMesh)
        
    def addSystemImplant(self, path, sysman):
        implants = importImplant.importImplant(path)
        for implant in implants:
            newImplant = m_implant.implants(start=np.array([float(element) for element in implant[0]]), end=np.array([float(element) for element in implant[1]]), radius=float(implant[2])/2, color=np.array([int(element) for element in implant[3]]))
            self.addTableImplant(sysman, newImplant)
                
    def addSystemLandmark(self, pointlist, sysman):
        tmp_point = []
        for i in range(len(pointlist)):
            tmp_point.append(round(float(pointlist[i]), 3))
            if len(tmp_point) == 3:
                newLandmark = m_landmark.landmark(scalar = copy.deepcopy(tmp_point))
                self.addTableLandmark(sysman, newLandmark)
                tmp_point = []
                
    def addSystemRom(self, path, sysman):
        path = path.replace("\\", "/")
        name = path.split("/")[-1].split('.')[0]
        newRom = m_rom.rom(Name=name, filePath=path)
        self.addTableRom(sysman, newRom)
                
    def buildSystemTools(self, path, sysman):
        TOOL_filter = "stl"
        TOOL_list = [file for file in os.listdir(path) if file.split(".")[-1] == TOOL_filter and os.path.isfile(os.path.join(path, file))]
        for file in TOOL_list:
            tool_path = os.path.join(path, file).replace("\\", "/")
            new_stl = importMesh.importSTL(tool_path)
            name = tool_path.split("/")[-1].split('.')[0]
            newTool = m_tool.tool(polydata=new_stl, Name=name, filePath=tool_path)
            self.addTableTool(sysman, newTool)
                
    def buildSystemSetting(self, path, sysman):
        settings = importIni.importIni(path)
        pointlist= settings.get('General', 'FiducialPoints').split(",")
        # sysman.landmarks = [] # 清空原来的定点
        sysman.TrackerHostName = None # 清空原来的设备名，用于判断是否读取成功
        self.addSystemLandmark(pointlist, sysman)
        sysman.TrackerHostName = settings.get('General', 'TrackerHostName')
        tmp_matrix = settings.get('General', 'probeDeviateMatrix').split(",")
        try:
            sysman.probeDeviateMatrix = np.array([float(element) for element in tmp_matrix])#.reshape(4, 4)
        except ValueError:
            QMessageBox.warning(sysman.ui, 'Warning', 'Setting error!', QMessageBox.Ok)
            sysman.printInfo("Invalid string format for float conversion! Please check your setting file!")    
        
    def buildSystemRom(self, path, sysman):
        # 定义过滤器和文件列表
        SROM_filter = "rom"
        SROM_list = [file for file in os.listdir(path) if file.split(".")[-1] == SROM_filter and os.path.isfile(os.path.join(path, file))]
        for file in SROM_list:
            SROM_path = os.path.join(path, file)
            self.addSystemRom(SROM_path, sysman)
            
    def buildAll(self, path, sysman):
        if not os.path.exists(path):
            sysman.printInfo("Path:\""+path+"\" does not work!")
            return 
        files = os.listdir(path)
        num_files = len(files)
        for i in range(num_files):
            QCoreApplication.processEvents() # 防卡顿
            sysman.showProgress(int(100*i/num_files))
            f = files[num_files-i-1]
            file_path = os.path.join(path, f).replace('\\','/')
            numOfSTLs = len(sysman.meshes)
            numOfImplants = len(sysman.implants)
            numOfDicomss = len(sysman.dicoms)
            numOfRoms = len(sysman.roms)
            numOfTools = len(sysman.tools)
            if f.lower().endswith('.stl'):
                self.addSystemSTL(file_path, sysman)
                if len(sysman.meshes) > numOfSTLs:
                    sysman.printInfo("Add STL:\""+file_path+"\".")
            elif f.lower().endswith('.implant'):
                self.addSystemImplant(file_path, sysman)
                if len(sysman.implants) > numOfImplants:
                    sysman.printInfo("Add implants:\""+file_path+"\".")
            elif f.lower().endswith('.ini'):
                self.buildSystemSetting(file_path, sysman)
                if sysman.TrackerHostName is not None:
                    sysman.printInfo("Add settings:\""+file_path+"\".")
                else:
                    sysman.printInfo("Lacking TrackerHostName in:\""+file_path+"\".")
            elif 'NDIFiles' in f:
                self.buildSystemRom(file_path, sysman)
                if len(sysman.roms) > numOfRoms:
                    sysman.printInfo("Add ROM files in:"+file_path+".")
                self.buildSystemTools(file_path, sysman)
                if len(sysman.tools) > numOfTools:
                    sysman.printInfo("Add tool files in:"+file_path+".")
            else:
                self.addSystemDicoms(file_path, sysman)
                if len(sysman.dicoms) > numOfDicomss:
                    sysman.printInfo("Add DICOMs in:" + path)
        sysman.ProgressEnd()
                
    def import_file(self, sysman, file_type=None): 
        file_name = None
        if file_type:
            file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a {file_type} file', "C:/", f"{file_type}(*.{file_type});All Files(*)")
        else: 
            file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a file', "C:/", f"All Files(*)")
        if not os.path.exists(file_name):
            sysman.printInfo("No document was selected!")
            return
        sysman.ProgressStart()
        if '\\' in file_name:
            file_name = file_name.replace("\\", "/")
        name = file_name.split("/")[-1]
        file_extension = name.split(".")[-1]
        if file_extension == "stl" or file_extension == "STL":
            self.addSystemSTL(file_name, sysman)
        elif file_extension == "obj":
            self.addSystemOBJ(file_name, sysman)
        elif file_extension == "implant":
            self.addSystemImplant(file_name, sysman)
        elif file_extension == "txt":
            lines = importTxt.importTxt(file_name)
            content = "\n*******************************************************************************"
            for line in lines:
                content = str(content) + '\n' + line
            sysman.printInfo(content+"\n*******************************************************************************")
        elif file_extension == "rom":
            self.addSystemRom(file_name, sysman)
        elif file_extension == "ini":
            self.buildSystemSetting(file_name, sysman)
        else:
            QMessageBox.warning(sysman.ui, 'Warning', 'The file is not appropriate!', QMessageBox.Ok)
            return
        sysman.ProgressEnd()
        sysman.printInfo("Import file:" + file_name)
        pass
           
    def import_folder(self, sysman):
        path = QFileDialog.getExistingDirectory(sysman.ui, 'Choose Source File Which Should Include Image, NDI File, Implant Files and so on', os.getcwd())
        if not os.path.exists(path):
            sysman.printInfo("No folder is selected!")
            return
        self.buildAll(path, sysman)
    
    def save_all(self, sysman):
        directory_path = QFileDialog.getExistingDirectory(None, "select a folder", "")
        if directory_path:
            sysman.ProgressStart()
            for dicom in sysman.dicoms:
                dicom_folder = directory_path + '/' + dicom.getName()
                if os.path.exists(dicom_folder):  # 检查目录是否存在, 覆盖文件
                    shutil.rmtree(directory_path)
                os.makedirs(dicom_folder) 
                saveDicom.saveDicom(dicom, dicom_folder)
            sysman.showProgress(50)  
            for mesh in sysman.meshes:
                saveSTL.save_polydata_as_stl(mesh.getPolydata(), directory_path + '/' + mesh.getName() + '.stl')
            sysman.showProgress(60)  
            if len(sysman.implants) > 0:
                content = [f"{len(sysman.implants)}\n"]
                for i in range(len(sysman.implants)):
                    start = sysman.implants[i].getStart()
                    end = sysman.implants[i].getEnd()
                    color = sysman.implants[i].getColor()
                    content.append(f"{start[0]} {end[0]} {color[0]}\n")
                    content.append(f"{start[1]} {end[1]} {color[1]}\n")
                    content.append(f"{start[2]} {end[2]} {color[2]}\n")
                    content.append(f"{sysman.implants[i].getRadius()}\n")
                saveImplant.save_content_to_txt(content, directory_path + '/implants.implant')
            sysman.showProgress(70)  
            content = f"[General]\n"
            if len(sysman.landmarks) > 0:
                content = content + f"FiducialPoints="
                for i in range(len(sysman.landmarks)):
                    scalar = sysman.landmarks[i].getScalar()
                    content = content+f'{scalar[0]}, {scalar[1]}, {scalar[2]}'
                    if i != len(sysman.landmarks)-1:
                        content = content+', '
                    else:
                        content = content+'\n'
            content = content + f'probeDeviateMatrix={sysman.probeDeviateMatrix[0]}, {sysman.probeDeviateMatrix[1]}, {sysman.probeDeviateMatrix[2]}, {sysman.probeDeviateMatrix[3]}, {sysman.probeDeviateMatrix[4]}, {sysman.probeDeviateMatrix[5]}, {sysman.probeDeviateMatrix[6]}, {sysman.probeDeviateMatrix[7]}, {sysman.probeDeviateMatrix[8]}, {sysman.probeDeviateMatrix[9]}, {sysman.probeDeviateMatrix[10]}, {sysman.probeDeviateMatrix[11]}, {sysman.probeDeviateMatrix[12]}, {sysman.probeDeviateMatrix[13]}, {sysman.probeDeviateMatrix[14]}, {sysman.probeDeviateMatrix[15]}\n'
            if sysman.TrackerHostName:
                content = content + 'TrackerHostName=' + sysman.TrackerHostName
            saveSetting.saveSetting(content, directory_path + '/setting.ini')  
            sysman.showProgress(80) 
            for rom in sysman.roms:
                saveROM.saveRom(rom, directory_path + '/NDIFiles/' + rom.getName() + '.rom')
            sysman.showProgress(90) 
            for tool in sysman.tools:
                saveSTL.save_polydata_as_stl(tool.getPolydata(), directory_path + '/NDIFiles/' + tool.getName() + '.stl')
            sysman.ProgressEnd()
            sysman.printInfo("The files were saved to " + directory_path + '.')

        else:
            sysman.printInfo("No path was selected.")
        
    
    def open_setting(self, sysman):
        pass
    
    def open_help(self, sysman):
        pass
    
    def quit_system(self, sysman):
        app = QApplication.instance()
        app.quit()
    
    def conect2ndi(self, sysman):
        if sysman.ui.connect_btn.isChecked():
            sysman.ui.l1.setVisible(True) 
            sysman.ui.l2.setVisible(True)
            sysman.ui.l3.setVisible(True) 
        else:
            sysman.ui.l1.setVisible(False) 
            sysman.ui.l2.setVisible(False)
            sysman.ui.l3.setVisible(False) 
        pass
    
    def registration(self, sysman):
        if sysman.ui.registration_btn.isChecked():
            numOfLight = min(config.numOfLight, len(sysman.landmarks))
            if numOfLight:
                tmp_marks = sysman.ui.regisMarks[-numOfLight:]
                for mark in tmp_marks:
                    mark.setVisible(True)
        else:
            for mark in sysman.ui.regisMarks:
                mark.setVisible(False)
        pass
    
    def calibration(self, sysman):
        pass
    
    def conect2robo(self, sysman):
        pass
    
    def localization(self, sysman):
        if sysman.ui.location_btn.isChecked():
            sysman.renderers[1].AddActor(sysman.localization_actor)
        else:
            sysman.renderers[1].RemoveActor(sysman.localization_actor)
        sysman.views[1].update()
    
    def cross_line(self, sysman):
        sysman.cross_line_sign = (sysman.cross_line_sign + 1) % 3
        if sysman.cross_line_sign == 0:
            for i in range(len(sysman.lineActors)):
                sysman.lineActors[i].SetVisibility(0) 
        elif sysman.cross_line_sign == 1:
            for i in range(len(sysman.lineActors)):
                sysman.lineActors[i].SetVisibility(i >= 3)
        elif sysman.cross_line_sign == 2:
            for i in range(len(sysman.lineActors)):
                sysman.lineActors[i].SetVisibility(1)
        sysman.updateViews()     
    
    def reset(self, sysman):
        pass
    
    def measure(self, sysman):
        if sysman.ui.measure_btn.isChecked():
            self.measure_sign = 0
            sysman.renderers[1].AddActor(sysman.measure_actors[0])
            sysman.renderers[1].AddActor(sysman.measure_actors[1])
        else:
            sysman.renderers[1].RemoveActor(sysman.measure_actors[0])
            sysman.renderers[1].RemoveActor(sysman.measure_actors[1])
        sysman.views[1].update()
        
    def volume_calculation(self, sysman):
        if sysman.current_mesh_index is None:
            sysman.printInfo("Please select a mesh!")
            return 
        volume = volumeOfMesh.volumeOfMesh(sysman.meshes[sysman.current_mesh_index].getPolydata())
        sysman.printInfo(f"The volume of "+sysman.meshes[sysman.current_mesh_index].getName()+f": {volume:.3f} mm{config.cubic}") # 加粗加红
    
    def project2D(self, sysman):
        for i in [0, 2, 3]:
            sysman.contour_renderers[i].RemoveAllViewProps()
        sysman.add2DLineActors()
        if sysman.ui.project_btn.isChecked():
            view_center = [0, 0, 0]
            if sysman.current_dicom_index is not None:
                vtk_img = sysman.dicoms[sysman.current_dicom_index].getImageData()
                view_center = dcmCenter.getDCMCenter(vtk_img)
            for i in range(len(sysman.meshes)):
                projectActors = createPrjActor.createPrjActors(sysman.meshes[i], sysman.lineCenter, view_center)
                sysman.meshes[i].setPrjActors(projectActors)
                sysman.contour_renderers[0].AddActor(projectActors[2])
                sysman.contour_renderers[2].AddActor(projectActors[0])
                sysman.contour_renderers[3].AddActor(projectActors[1])
            for i in range(len(sysman.implants)):
                projectActors = createPrjActor.createPrjActors(sysman.implants[i], sysman.lineCenter, view_center)
                sysman.implants[i].setPrjActors(projectActors)
                sysman.contour_renderers[0].AddActor(projectActors[2])
                sysman.contour_renderers[2].AddActor(projectActors[0])
                sysman.contour_renderers[3].AddActor(projectActors[1])
            for i in range(len(sysman.landmarks)):
                projectActors = createPrjActor.createPrjActors(sysman.landmarks[i], sysman.lineCenter, view_center)
                sysman.landmarks[i].setPrjActors(projectActors)
                sysman.contour_renderers[0].AddActor(projectActors[2])
                sysman.contour_renderers[2].AddActor(projectActors[0])
                sysman.contour_renderers[3].AddActor(projectActors[1])
        sysman.contour_renderers[0].DrawOn()
        sysman.contour_renderers[2].DrawOn()
        sysman.contour_renderers[3].DrawOn()
        sysman.contour_renderers[0].Modified()
        sysman.contour_renderers[2].Modified()
        sysman.contour_renderers[3].Modified()
        sysman.updateViews() 
            
    def updateProject2D(self, sysman, view_num):
        if sysman.ui.project_btn.isChecked():
            cor = [2, 0, 0, 1]
            normals = [[0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 1, 0]]  # consistent with the order of views
            view_center = [0, 0, 0]
            if sysman.current_visual_dicom_index is not None:
                vtk_img = sysman.dicoms[sysman.current_visual_dicom_index].getImageData()
                view_center = dcmCenter.getDCMCenter(vtk_img)
            sysman.contour_renderers[view_num].RemoveAllViewProps()
            for i in range(len(sysman.meshes)):
                if sysman.meshes[i].getVisible():
                    if len(sysman.meshes[i].getPrjActors()) > 0:
                        prj_actor = createPrjActor.createPrjActor(sysman.meshes[i], sysman.lineCenter, view_center, normals[view_num])
                        sysman.meshes[i].setPrjActor(prj_actor, cor[view_num])
                    else:
                        projectActors = createPrjActor.createPrjActors(sysman.meshes[i], sysman.lineCenter, view_center)
                        sysman.meshes[i].setPrjActors(projectActors)
                    sysman.contour_renderers[view_num].AddActor(sysman.meshes[i].getPrjActors()[cor[view_num]])
                    sysman.contour_renderers[view_num].DrawOn()
                    sysman.contour_renderers[view_num].Modified()
                    # sysman.contour_renderers[view_num].ResetCamera()
            for i in range(len(sysman.implants)):
                if sysman.implants[i].getVisible():
                    if len(sysman.implants[i].getPrjActors()) > 0:
                        prj_actor = createPrjActor.createPrjActor(sysman.implants[i], sysman.lineCenter, view_center, normals[view_num])
                        sysman.implants[i].setPrjActor(prj_actor, cor[view_num])
                    else:
                        projectActors = createPrjActor.createPrjActors(sysman.implants[i], sysman.lineCenter, view_center)
                        sysman.implants[i].setPrjActors(projectActors)
                    sysman.contour_renderers[view_num].AddActor(sysman.implants[i].getPrjActors()[cor[view_num]])
                    sysman.contour_renderers[view_num].DrawOn()
                    sysman.contour_renderers[view_num].Modified()
            for i in range(len(sysman.landmarks)):
                if sysman.landmarks[i].getVisible():
                    if len(sysman.landmarks[i].getPrjActors()) > 0:
                        prj_actor = createPrjActor.createPrjActor(sysman.landmarks[i], sysman.lineCenter, view_center, normals[view_num])
                        sysman.landmarks[i].setPrjActor(prj_actor, cor[view_num])
                    else:
                        projectActors = createPrjActor.createPrjActors(sysman.landmarks[i], sysman.lineCenter, view_center)
                        sysman.landmarks[i].setPrjActors(projectActors)
                    sysman.contour_renderers[view_num].AddActor(sysman.landmarks[i].getPrjActors()[cor[view_num]])
                    sysman.contour_renderers[view_num].DrawOn()
                    sysman.contour_renderers[view_num].Modified()
            sysman.add2DLineActors()
        sysman.updateViews() 
                
    def addDicom(self, sysman):
        path = QFileDialog.getExistingDirectory(sysman.ui, 'select the dicom folder', os.getcwd())
        if not os.path.exists(path):
            sysman.printInfo("Path:\""+path+"\" does not work!")
            return
        sysman.ProgressStart()
        res = self.addSystemDicoms(path, sysman)
        sysman.ProgressEnd()
        if res:
            sysman.printInfo("Successfully import dicoms in:" + path)
        pass
        
    def deleteDicom(self, sysman):
        if sysman.current_dicom_index == None:
            sysman.printInfo("No DICOM was selected.")
            return
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Confirm")
        msg_box.setText("Do you want to delete the DICOM?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # 设置"Yes"和"No"按钮
        msg_box.setDefaultButton(QMessageBox.No)  # 默认选中"No"
        # 显示消息框并等待用户响应
        response = msg_box.exec_()
        # 根据用户点击的按钮进行处理
        if response == QMessageBox.Yes:
            self.deleteSystemDICOM(sysman)
        elif response == QMessageBox.No:
            return

    def deleteSystemDICOM(self, sysman):
        if sysman.current_visual_dicom_index == sysman.current_dicom_index:
            for i in range(4):
                if i == 1:
                    sysman.renderers[i].RemoveVolume(sysman.dicoms[sysman.current_dicom_index].getActors()[i])
                else:
                    sysman.renderers[i].RemoveAllViewProps()
                sysman.current_visual_dicom_index = None
        elif sysman.current_visual_dicom_index > sysman.current_dicom_index:
            sysman.current_visual_dicom_index -= 1
        sysman.ui.dicom_tw.removeRow(sysman.current_dicom_index)
        del sysman.dicoms[sysman.current_dicom_index]
        sysman.current_dicom_index = None 
        sysman.updateViews()
        
    def exportDICOM(self, sysman):
        if sysman.current_dicom_index == None:
            sysman.printInfo("No DICOM was selected.")
            return
        directory_path = QFileDialog.getExistingDirectory(None, "select a folder", "")
        if directory_path:
            sysman.ProgressStart()
            saveDicom.saveDicom(sysman.dicoms[sysman.current_dicom_index], directory_path)
            sysman.printInfo("The file was saved to " + directory_path + '.')
            sysman.ProgressEnd()
        else:
            sysman.printInfo("No path was selected.")
      
    def addMesh(self, sysman):
        file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a mesh file', "C:/", f"STL(*.stl);OBJ(*.obj);All Files(*)")
        if not os.path.exists(file_name):
            sysman.printInfo("Path:\""+file_name+"\" does not work!")
            return
        name = file_name.split("/")[-1]
        file_extension = name.split(".")[-1]
        if file_extension == "stl" or file_extension == "STL":
            self.addSystemSTL(file_name, sysman)
        elif file_extension == "obj":
            self.addSystemOBJ(file_name, sysman)
        sysman.printInfo("Add Mesh files in:" + file_name + ".")
 
    def changeMeshColor(self, sysman):
        pass
    
    def deleteMesh(self, sysman):
        if sysman.current_mesh_index == None:
            sysman.printInfo("No mesh was selected.")
            return
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Confirm")
        msg_box.setText("Do you want to delete the mesh?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # 设置"Yes"和"No"按钮
        msg_box.setDefaultButton(QMessageBox.No)  # 默认选中"No"
        # 显示消息框并等待用户响应
        response = msg_box.exec_()
        # 根据用户点击的按钮进行处理
        if response == QMessageBox.Yes:
            self.deleteSystemMesh(sysman)
        elif response == QMessageBox.No:
            return
        
    def deleteSystemMesh(self, sysman):
        sysman.ui.mesh_tw.removeRow(sysman.current_mesh_index)
        if util.is_actor_in_renderer(sysman.meshes[sysman.current_mesh_index].getActor(), sysman.renderers[1]):
            sysman.renderers[1].RemoveActor(sysman.meshes[sysman.current_mesh_index].getActor())
            if sysman.meshes[sysman.current_mesh_index].getPrjActors():
                if util.is_actor_in_renderer(sysman.meshes[sysman.current_mesh_index].getPrjActors()[0], sysman.contour_renderers[2]):
                    sysman.contour_renderers[2].RemoveActor(sysman.meshes[sysman.current_mesh_index].getPrjActors()[0])
                if util.is_actor_in_renderer(sysman.meshes[sysman.current_mesh_index].getPrjActors()[1], sysman.contour_renderers[3]):
                    sysman.contour_renderers[3].RemoveActor(sysman.meshes[sysman.current_mesh_index].getPrjActors()[1])
                if util.is_actor_in_renderer(sysman.meshes[sysman.current_mesh_index].getPrjActors()[2], sysman.contour_renderers[0]):
                    sysman.contour_renderers[0].RemoveActor(sysman.meshes[sysman.current_mesh_index].getPrjActors()[2])
        del sysman.meshes[sysman.current_mesh_index]
        sysman.current_mesh_index = None 
        sysman.updateViews()       
    
    def exportMesh(self, sysman):
        if sysman.current_mesh_index == None:
            sysman.printInfo("No mesh was selected.")
            return
        file_name, _ = QFileDialog.getSaveFileName(sysman.ui, "save mesh", "../", "STL (*.stl)")
        if file_name:  # 如果用户没有取消操作
            sysman.ProgressStart()
            saveSTL.save_polydata_as_stl(sysman.meshes[sysman.current_mesh_index].getPolydata(), file_name)
            sysman.printInfo("The file was saved to " + file_name + '.')
            sysman.ProgressEnd()
        else:
            sysman.printInfo("No path was selected.")
    
    def addImplant(self, sysman):
        newImplant = m_implant.implants(start=np.array([0, 0, 0]), end=np.array([0, 0, 0]), radius=2, color=np.array([1, 0, 0]))
        self.addTableImplant(sysman, newImplant)
    
    def changeImplantColor(self, sysman):
        pass
    
    def deleteImplant(self, sysman):
        if sysman.current_implant_index == None:
            sysman.printInfo("No implant was selected.")
            return
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Confirm")
        msg_box.setText("Do you want to delete the implant?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # 设置"Yes"和"No"按钮
        msg_box.setDefaultButton(QMessageBox.No)  # 默认选中"No"
        # 显示消息框并等待用户响应
        response = msg_box.exec_()
        # 根据用户点击的按钮进行处理
        if response == QMessageBox.Yes:
            self.deleteSystemImplant(sysman)
        elif response == QMessageBox.No:
            return
    
    def deleteSystemImplant(self, sysman):
        sysman.ui.implant_tw.removeRow(sysman.current_implant_index)
        if util.is_actor_in_renderer(sysman.implants[sysman.current_implant_index].getTubeActor(), sysman.renderers[1]):
            sysman.renderers[1].RemoveActor(sysman.implants[sysman.current_implant_index].getTubeActor())
            if util.is_actor_in_renderer(sysman.implants[sysman.current_implant_index].getDashActor(), sysman.renderers[1]):
                sysman.renderers[1].RemoveActor(sysman.implants[sysman.current_implant_index].getDashActor())
            if sysman.implants[sysman.current_implant_index].getPrjActors():
                if util.is_actor_in_renderer(sysman.implants[sysman.current_implant_index].getPrjActors()[0], sysman.contour_renderers[2]):
                    sysman.contour_renderers[2].RemoveActor(sysman.implants[sysman.current_implant_index].getPrjActors()[0])
                if util.is_actor_in_renderer(sysman.implants[sysman.current_implant_index].getPrjActors()[1], sysman.contour_renderers[3]):
                    sysman.contour_renderers[3].RemoveActor(sysman.implants[sysman.current_implant_index].getPrjActors()[1])
                if util.is_actor_in_renderer(sysman.implants[sysman.current_implant_index].getPrjActors()[2], sysman.contour_renderers[0]):
                    sysman.contour_renderers[0].RemoveActor(sysman.implants[sysman.current_implant_index].getPrjActors()[2])
        del sysman.implants[sysman.current_implant_index]
        sysman.current_implant_index = None 
        sysman.updateViews()
    
    def exportImplants(self, sysman):
        save_implant_index = []
        for i in range(len(sysman.implants)):
            if sysman.implants[i].getVisible() > 0:
                save_implant_index.append(i)
        if len(save_implant_index) == 0:
            sysman.printInfo("No implant was selected.")
            return
        else:
            content = [f"{len(save_implant_index)}\n"]
            for i in range(len(save_implant_index)):
                start = sysman.implants[save_implant_index[i]].getStart()
                end = sysman.implants[save_implant_index[i]].getEnd()
                color = sysman.implants[save_implant_index[i]].getColor()
                content.append(f"{start[0]} {end[0]} {color[0]}\n")
                content.append(f"{start[1]} {end[1]} {color[1]}\n")
                content.append(f"{start[2]} {end[2]} {color[2]}\n")
                content.append(f"{sysman.implants[save_implant_index[i]].getRadius()}\n")           
            file_name, _ = QFileDialog.getSaveFileName(sysman.ui, "save implants", "../", "implant(*.implant)")
            sysman.ProgressStart()
            if file_name:  # 如果用户没有取消操作
                if saveImplant.save_content_to_txt(content, file_name):
                    sysman.printInfo("The file was saved to "+ file_name +'.')
                else:
                    sysman.printInfo("Saving failed. Please check the format.")
            else:
                sysman.printInfo("No path was selected.")
            sysman.ProgressEnd()

    def addLandmark(self, sysman):
        if len(sysman.landmarks) > 25:
            sysman.printInfo('Up to 25 landmarks can be added!')
            return
        newLandmark = m_landmark.landmark(scalar = np.array([0, 0, 0]))
        self.addTableLandmark(sysman, newLandmark)
        self.registration(sysman)
    
    def changeLandmarkColor(self, sysman):
        pass
    
    def deleteLandmark(self, sysman):
        if sysman.current_landmark_index == None:
            sysman.printInfo("No landmark was selected.")
            return
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Confirm")
        msg_box.setText("Do you want to delete the landmark?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # 设置"Yes"和"No"按钮
        msg_box.setDefaultButton(QMessageBox.No)  # 默认选中"No"
        # 显示消息框并等待用户响应
        response = msg_box.exec_()
        # 根据用户点击的按钮进行处理
        if response == QMessageBox.Yes:
            self.deleteSystemLandmark(sysman)
        elif response == QMessageBox.No:
            return
        
    def deleteSystemLandmark(self, sysman):
        sysman.ui.landmark_tw.removeRow(sysman.current_landmark_index)
        if util.is_actor_in_renderer(sysman.landmarks[sysman.current_landmark_index].getActor(), sysman.renderers[1]):
            sysman.renderers[1].RemoveActor(sysman.landmarks[sysman.current_landmark_index].getActor())
            if sysman.landmarks[sysman.current_landmark_index].getPrjActors():
                if util.is_actor_in_renderer(sysman.landmarks[sysman.current_landmark_index].getPrjActors()[0], sysman.contour_renderers[2]):
                    sysman.contour_renderers[2].RemoveActor(sysman.landmarks[sysman.current_landmark_index].getPrjActors()[0])
                if util.is_actor_in_renderer(sysman.landmarks[sysman.current_landmark_index].getPrjActors()[1], sysman.contour_renderers[3]):
                    sysman.contour_renderers[3].RemoveActor(sysman.landmarks[sysman.current_landmark_index].getPrjActors()[1])
                if util.is_actor_in_renderer(sysman.landmarks[sysman.current_landmark_index].getPrjActors()[2], sysman.contour_renderers[0]):
                    sysman.contour_renderers[0].RemoveActor(sysman.landmarks[sysman.current_landmark_index].getPrjActors()[2])
        del sysman.landmarks[sysman.current_landmark_index]
        sysman.current_landmark_index = None 
        sysman.updateViews()
    
    def exportLandmark(self, sysman):
        save_landmark_index = []
        content = f"[General]\n"
        for i in range(len(sysman.landmarks)):
            if sysman.landmarks[i].getVisible() > 0:
                save_landmark_index.append(i)
        if len(save_landmark_index) == 0:
            sysman.printInfo("No landmark was selected.")
        else:
            content = content + f"FiducialPoints="
            for i in range(len(save_landmark_index)):
                scalar = sysman.landmarks[save_landmark_index[i]].getScalar()
                content = content+f'{scalar[0]}, {scalar[1]}, {scalar[2]}'
                if i != len(save_landmark_index)-1:
                    content = content+', '
                else:
                    content = content+'\n'
        content = content + f'probeDeviateMatrix={sysman.probeDeviateMatrix[0]}, {sysman.probeDeviateMatrix[1]}, {sysman.probeDeviateMatrix[2]}, {sysman.probeDeviateMatrix[3]}, {sysman.probeDeviateMatrix[4]}, {sysman.probeDeviateMatrix[5]}, {sysman.probeDeviateMatrix[6]}, {sysman.probeDeviateMatrix[7]}, {sysman.probeDeviateMatrix[8]}, {sysman.probeDeviateMatrix[9]}, {sysman.probeDeviateMatrix[10]}, {sysman.probeDeviateMatrix[11]}, {sysman.probeDeviateMatrix[12]}, {sysman.probeDeviateMatrix[13]}, {sysman.probeDeviateMatrix[14]}, {sysman.probeDeviateMatrix[15]}\n'
        if sysman.TrackerHostName:
            content = content + 'TrackerHostName=' + sysman.TrackerHostName
        file_name, _ = QFileDialog.getSaveFileName(sysman.ui, "save setting", "../", "setting(*.ini)")
        sysman.ProgressStart()
        if file_name:  # 如果用户没有取消操作
            saveSetting.saveSetting(content, file_name)
            sysman.printInfo("The file was saved to "+ file_name +'.')
            sysman.printInfo("\n" + content)
        else:
            sysman.printInfo("No path was selected.")
        sysman.ProgressEnd()
    
    def addRom(self, sysman):
        file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a ROM file', "C:/", f"ROM(*.rom);All Files(*)")
        if not os.path.exists(file_name):
            sysman.printInfo("Path:\""+file_name+"\" does not work!")
            return
        path = file_name.replace("\\", "/")
        name = path.split("/")[-1].split('.')[0]
        newRom = m_rom.rom(Name=name, filePath=path)
        self.addTableRom(sysman, newRom)
        sysman.printInfo("Add ROM files in:" + file_name + ".")
   
    def deleteRom(self, sysman):
        if sysman.current_rom_index == None:
            sysman.printInfo("No ROM file was selected.")
            return
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Confirm")
        msg_box.setText("Do you want to delete the Rom?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # 设置"Yes"和"No"按钮
        msg_box.setDefaultButton(QMessageBox.No)  # 默认选中"No"
        # 显示消息框并等待用户响应
        response = msg_box.exec_()
        # 根据用户点击的按钮进行处理
        if response == QMessageBox.Yes:
            self.deleteSystemRom(sysman)
        elif response == QMessageBox.No:
            return
    
    def deleteSystemRom(self, sysman):
        sysman.ui.rom_tw.removeRow(sysman.current_rom_index)
        del sysman.roms[sysman.current_rom_index]
        sysman.current_rom_index = None 
        sysman.updateViews()
    
    def exportRom(self, sysman):
        if sysman.current_rom_index == None:
            sysman.printInfo("No ROM file was selected.")
            return
        file_name, _ = QFileDialog.getSaveFileName(sysman.ui, "save Rom", "../", "ROM(*.rom)")
        sysman.ProgressStart()
        if file_name:
            saveROM.saveRom(sysman.roms[sysman.current_rom_index], file_name)
            sysman.printInfo("The file was saved to "+ file_name +'.')
        else:
            sysman.printInfo("No path was selected.")
        sysman.ProgressEnd()    
    
    def addTool(self, sysman):
        file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a TOOL file', "C:/", f"STL(*.stl);OBJ(*.obj);All Files(*)")
        if not os.path.exists(file_name):
            sysman.printInfo("Path:\""+file_name+"\" does not work!")
            return
        path = file_name.replace("\\", "/")
        new_stl = importMesh.importSTL(path)
        name = path.split("/")[-1].split('.')[0]
        newTool = m_tool.tool(polydata=new_stl, Name=name, filePath=path)
        self.addTableTool(sysman, newTool)
        sysman.printInfo("Add Tool files in:" + file_name + ".")
    
    def changeToolColor(self, sysman):
        pass
    
    def deleteTool(self, sysman):
        if sysman.current_tool_index == None:
            sysman.printInfo("No tool was selected.")
            return
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Confirm")
        msg_box.setText("Do you want to delete the tool?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # 设置"Yes"和"No"按钮
        msg_box.setDefaultButton(QMessageBox.No)  # 默认选中"No"
        # 显示消息框并等待用户响应
        response = msg_box.exec_()
        # 根据用户点击的按钮进行处理
        if response == QMessageBox.Yes:
            self.deleteSystemTool(sysman)
        elif response == QMessageBox.No:
            return
        
    def deleteSystemTool(self, sysman):
        sysman.ui.tool_tw.removeRow(sysman.current_tool_index)
        if util.is_actor_in_renderer(sysman.tools[sysman.current_tool_index].getActor(), sysman.renderers[1]):
            sysman.renderers[1].RemoveActor(sysman.tools[sysman.current_tool_index].getActor())
            # if sysman.tools[sysman.current_tool_index].getPrjActors():
            #     if util.is_actor_in_renderer(sysman.tools[sysman.current_tool_index].getPrjActors()[0], sysman.contour_renderers[2]):
            #         sysman.contour_renderers[2].RemoveActor(sysman.tools[sysman.current_tool_index].getPrjActors()[0])
            #     if util.is_actor_in_renderer(sysman.tools[sysman.current_tool_index].getPrjActors()[1], sysman.contour_renderers[3]):
            #         sysman.contour_renderers[3].RemoveActor(sysman.tools[sysman.current_tool_index].getPrjActors()[1])
            #     if util.is_actor_in_renderer(sysman.tools[sysman.current_tool_index].getPrjActors()[2], sysman.contour_renderers[0]):
            #         sysman.contour_renderers[0].RemoveActor(sysman.tools[sysman.current_tool_index].getPrjActors()[2])
        del sysman.tools[sysman.current_tool_index]
        sysman.current_tool_index = None 
        sysman.updateViews()
    
    def exportTool(self, sysman):
        if sysman.current_tool_index == None:
            sysman.printInfo("No tool was selected.")
            return
        file_name, _ = QFileDialog.getSaveFileName(sysman.ui, "save tool", "../", "STL (*.stl)")
        sysman.ProgressStart()
        if file_name:  # 如果用户没有取消操作
            saveSTL.save_polydata_as_stl(sysman.tools[sysman.current_tool_index].getPolydata(), file_name)
            sysman.printInfo("The file was saved to "+ file_name +'.')
        else:
            sysman.printInfo("No path was selected.")
        sysman.ProgressEnd()
    
    def probeUnseen(self, sysman):
        pass
    
    def boneUnseen(self, sysman):
        pass
    
    def referenceUnseen(self, sysman):
        pass
    
    def setProgressbarValue(self, sysman):
        pass
    
    def adjust(self, sys_man):
        pass
    
    def addLight(self, sysman):
        pass
    
    def showTime(self, sysman):
        pass
    
    def setLight(self, item, sign=True):
        pass
    
    def addLight(self, sysman):
        pass  
    
    def deleteLight(sysman):
        pass
        
    def Render(self, renderWindows):
        renderWindows.render()     
    
    def renderDicoms(self, dicom, sysman, row, last=None):
        sysman.showProgress(1/len(config.VIEWORDER)*100)
        sysman.current_visual_dicom_index = row
        vtk_img = dicom.getImageData()
        extent = np.array(vtk_img.GetExtent())
        spacing = np.array(vtk_img.GetSpacing())
        origin = np.array(vtk_img.GetOrigin())
        #                       axial                     sagittal                 cornal
        extent_range = [int(extent[5] - extent[4]), 100, int(extent[1] - extent[0]), int(extent[3] - extent[2])]
        sysman.ui.volume_cbox.setChecked(True) 
        if last is not None:
            QCoreApplication.processEvents()
            sysman.renderers[1].RemoveVolume(sysman.dicoms[last].actors[1])
        for i in [0,2,3]:
            QCoreApplication.processEvents()
            sysman.renderers[i].RemoveAllViewProps()
        for i in config.VIEWORDER:
            QCoreApplication.processEvents()
            if i == 1:
                QCoreApplication.processEvents()
                sysman.renderers[i].AddVolume(dicom.actors[i])
                QCoreApplication.processEvents()
                # 获取并输出当前渲染器中未被隐藏的 actor 数量
                num_of_actors  = sysman.renderers[i].GetActors().GetNumberOfItems()
                if not num_of_actors:
                    sysman.resetCamera(sysman.renderers[i], 0, config.viewUp[i])
            else:
                QCoreApplication.processEvents()
                sysman.ui.ui_displays[i].slider.setMaximum(extent_range[i])
                QCoreApplication.processEvents()
                sysman.ui.ui_displays[i].slider.setValue(extent_range[i]/2)
                QCoreApplication.processEvents()
                sysman.renderers[i].AddActor(dicom.actors[i])
                QCoreApplication.processEvents()
                sysman.resetCamera(sysman.renderers[i], 1, config.viewUp[i])
                QCoreApplication.processEvents()
            with ThreadPoolExecutor() as executor:
                # 提交任务给线程池执行（带参数）
                executor.submit(self.Render, sysman.vtk_renderWindows[i])
        tmp_lineCenter = [0, 0, 0]
        tmp_lineCenter[2] = spacing[2] * (sysman.ui.ui_displays[0].slider.value()+extent[4]) + origin[2]
        tmp_lineCenter[0] = spacing[0] * (sysman.ui.ui_displays[2].slider.value()+extent[0]) + origin[0]
        tmp_lineCenter[1] = spacing[1] * (sysman.ui.ui_displays[3].slider.value()+extent[2]) + origin[1]
        diff = [tmp_lineCenter[0]-sysman.lineCenter[0], tmp_lineCenter[1]-sysman.lineCenter[1], tmp_lineCenter[2]-sysman.lineCenter[2]]
        for i in range(3):
            sysman.lineActors[i].AddPosition(diff[0], diff[1], diff[2])
        sysman.lineCenter = tmp_lineCenter
        sysman.reposition2DLineActors()
        for i in config.VIEWORDER:
            sysman.showProgress((i+1)/len(config.VIEWORDER)*100)
            sysman.vtk_renderWindows[i].Render()
            sysman.views[i].update()
            
    def renderMeshes(self, mesh, sysman):
        sysman.renderers[1].AddActor(mesh.actor)
        sysman.vtk_renderWindows[1].Render() 
        sysman.views[1].update()
        
    def renderLandmarks(self, landmark, sysman):
        sysman.renderers[1].AddActor(landmark.actor)
        sysman.vtk_renderWindows[1].Render() 
        sysman.views[1].update()
        
    def renderImplants(self, implant, sysman):
        sysman.renderers[1].AddActor(implant.tube_actor)
        sysman.renderers[1].AddActor(implant.dash_actor)
        sysman.vtk_renderWindows[1].Render() 
        sysman.views[1].update()
    
    def on_dicom_table_clicked(self, sysman, row, column):
        sysman.current_dicom_index = row
        pass
    
    def on_dicom_table_doubleClicked(self, sysman, item):
        sysman.current_dicom_index = item.row()
        if sysman.current_visual_dicom_index is not None and  sysman.current_visual_dicom_index == item.row():
            return
        sysman.ui.setEnabled(False)
        self.renderDicoms(sysman.dicoms[sysman.current_dicom_index], sysman, row=item.row(), last=sysman.current_visual_dicom_index)
        sysman.ui.setEnabled(True)
        pass
    
    def on_mesh_table_clicked(self, sysman, row, column):
        sysman.current_mesh_index = row
        for i in range(sysman.ui.mesh_tw.columnCount()):
            if 'Visible' in sysman.ui.mesh_tw.horizontalHeaderItem(i).text() and column == i:
                sysman.meshes[row].changeVisible()
                visible_widget = createVisibleWidget.createVisibleWidget(sysman.meshes[row].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
                sysman.ui.mesh_tw.setCellWidget(row, column, visible_widget)
                sysman.vtk_renderWindows[1].Render() 
            if 'Color' in sysman.ui.mesh_tw.horizontalHeaderItem(i).text() and column == i:
                # 设置初始颜色为RGB(255, 0, 0)
                initial_color = QColor(255, 0, 0)
                # 显示颜色选择对话框，并设置初始颜色
                color = QColorDialog.getColor(initial_color)
                color = [color.red(), color.green(), color.blue()]
                color_widget = createColorWidget.createColorWidget(color)
                sysman.ui.mesh_tw.setCellWidget(row, column, color_widget)
                sysman.meshes[row].setColor(np.array(color)/255)
        sysman.updateViews() 
    
    def on_mesh_table_right_clicked(self, sysman, pos):
        cell = sysman.mesh_tw.indexAt(pos)
        row = cell.row()
        column = cell.column()
        
        
        pass
    
    def on_implant_table_clicked(self, sysman, row, column):
        sysman.current_implant_index = row
        for i in range(sysman.ui.implant_tw.columnCount()):
            if 'Visible' in sysman.ui.implant_tw.horizontalHeaderItem(i).text() and column == i:
                sysman.implants[row].changeVisible()
                visible_widget = createVisibleWidget.createVisibleWidget(sysman.implants[row].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
                sysman.ui.implant_tw.setCellWidget(row, column, visible_widget)
                sysman.vtk_renderWindows[1].Render() 
            if 'Color' in sysman.ui.implant_tw.horizontalHeaderItem(i).text() and column == i:
                # 设置初始颜色为RGB(255, 0, 0)
                initial_color = QColor(255, 0, 0)
                # 显示颜色选择对话框，并设置初始颜色
                color = QColorDialog.getColor(initial_color)
                color = [color.red(), color.green(), color.blue()]
                color_widget = createColorWidget.createColorWidget(color)
                sysman.ui.implant_tw.setCellWidget(row, column, color_widget)
                sysman.implants[row].setColor(np.array(color)/255)
        sysman.updateViews() 
    
    def on_landmark_table_clicked(self, sysman, row, column):
        sysman.current_landmark_index = row
        for i in range(sysman.ui.landmark_tw.columnCount()):
            if 'Visible' in sysman.ui.landmark_tw.horizontalHeaderItem(i).text() and column == i:
                sysman.landmarks[row].changeVisible()
                visible_widget = createVisibleWidget.createVisibleWidget(sysman.landmarks[row].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
                sysman.ui.landmark_tw.setCellWidget(row, column, visible_widget)
                sysman.vtk_renderWindows[1].Render() 
            if 'Color' in sysman.ui.landmark_tw.horizontalHeaderItem(i).text() and column == i:
                # 设置初始颜色为RGB(255, 0, 0)
                initial_color = QColor(255, 0, 0)
                # 显示颜色选择对话框，并设置初始颜色
                color = QColorDialog.getColor(initial_color)
                color = [color.red(), color.green(), color.blue()]
                color_widget = createColorWidget.createColorWidget(color)
                sysman.ui.landmark_tw.setCellWidget(row, column, color_widget)
                sysman.landmarks[row].setColor(np.array(color)/255)
        sysman.updateViews() 
    
    def on_rom_table_clicked(self, sysman, row, column):
        sysman.current_rom_index = row
        pass
    
    def on_tool_table_clicked(self, sysman, row, column):
        sysman.current_tool_index = row
        for i in range(sysman.ui.tool_tw.columnCount()):
            if 'Visible' in sysman.ui.tool_tw.horizontalHeaderItem(i).text() and column == i:
                sysman.tools[row].changeVisible()
                visible_widget = createVisibleWidget.createVisibleWidget(sysman.tools[row].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
                sysman.ui.tool_tw.setCellWidget(row, column, visible_widget)
                sysman.vtk_renderWindows[1].Render() 
            if 'Color' in sysman.ui.tool_tw.horizontalHeaderItem(i).text() and column == i:
                # 设置初始颜色为RGB(255, 0, 0)
                initial_color = QColor(255, 0, 0)
                # 显示颜色选择对话框，并设置初始颜色
                color = QColorDialog.getColor(initial_color)
                color = [color.red(), color.green(), color.blue()]
                color_widget = createColorWidget.createColorWidget(color)
                sysman.ui.tool_tw.setCellWidget(row, column, color_widget)
                sysman.tools[row].setColor(np.array(color)/255)            
        sysman.updateViews() 
    
    def resetCamera0(self, sysman):
        sysman.resetCamera(sysman.renderers[0], 1, config.viewUp[0])
        sysman.vtk_renderWindows[0].Render() 
        sysman.views[0].update()
    
    def resetCamera1(self, sysman):
        sysman.resetCamera(sysman.renderers[1], 0, config.viewUp[1])
        sysman.vtk_renderWindows[1].Render() 
        sysman.views[1].update()
        
    def resetCamera2(self, sysman):
        sysman.resetCamera(sysman.renderers[2], 1, config.viewUp[2])
        sysman.vtk_renderWindows[2].Render() 
        sysman.views[2].update()
        
    def resetCamera3(self, sysman):
        sysman.resetCamera(sysman.renderers[3], 1, config.viewUp[3])
        sysman.vtk_renderWindows[3].Render() 
        sysman.views[3].update()
        
    def rotate_view0(self, sysman, angle = 90.0):
        sysman.renderers[0].GetActiveCamera().Roll(angle)
        sysman.vtk_renderWindows[0].Render() 
        sysman.views[0].update()
    
    def rotate_view1(self, sysman, angle = 90.0):
        sysman.renderers[1].GetActiveCamera().Roll(angle)
        sysman.vtk_renderWindows[1].Render() 
        sysman.views[1].update()
        
    def rotate_view2(self, sysman, angle = 90.0):
        sysman.renderers[2].GetActiveCamera().Roll(angle)
        sysman.vtk_renderWindows[2].Render() 
        sysman.views[2].update()
        
    def rotate_view3(self, sysman, angle = 90.0):
        sysman.renderers[3].GetActiveCamera().Roll(angle)
        sysman.vtk_renderWindows[3].Render() 
        sysman.views[3].update()
    
    def zoom_view0(self, sysman):
        if sysman.dlsplay_status == ALLWIN:
            sysman.dlsplay_status = AXIAL
            sysman.ui.view_box0.setParent(None)
            sysman.ui.view_box1.setParent(None)
            sysman.ui.view_box2.setParent(None)
            sysman.ui.view_box3.setParent(None)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box0)
            sysman.ui.ui_displays[0].zoom_btn.setStyleSheet("image: url(:/display/缩小.png);")

        elif sysman.dlsplay_status != ALLWIN:
            sysman.dlsplay_status = ALLWIN
            sysman.ui.view_box0.setParent(None)
            sysman.ui.view_box1.setParent(None)
            sysman.ui.view_box2.setParent(None)
            sysman.ui.view_box3.setParent(None)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box0, 0,0,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box1, 0,1,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box2, 1,0,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box3, 1,1,1,1)
            sysman.ui.ui_displays[0].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[1].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[2].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[3].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
        
    def zoom_view1(self, sysman):
        if sysman.dlsplay_status == ALLWIN:
            sysman.dlsplay_status = VIEW3D
            sysman.ui.view_box0.setParent(None)
            sysman.ui.view_box1.setParent(None)
            sysman.ui.view_box2.setParent(None)
            sysman.ui.view_box3.setParent(None)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box1)
            sysman.ui.ui_displays[1].zoom_btn.setStyleSheet("image: url(:/display/缩小.png);")
        elif sysman.dlsplay_status != ALLWIN:
            sysman.dlsplay_status = ALLWIN
            sysman.ui.view_box0.setParent(None)
            sysman.ui.view_box1.setParent(None)
            sysman.ui.view_box2.setParent(None)
            sysman.ui.view_box3.setParent(None)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box0, 0,0,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box1, 0,1,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box2, 1,0,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box3, 1,1,1,1)
            sysman.ui.ui_displays[0].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[1].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[2].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[3].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
             
    def zoom_view2(self, sysman):
        if sysman.dlsplay_status == ALLWIN:
            sysman.dlsplay_status = SAGITA
            sysman.ui.view_box0.setParent(None)
            sysman.ui.view_box1.setParent(None)
            sysman.ui.view_box2.setParent(None)
            sysman.ui.view_box3.setParent(None)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box2)
            sysman.ui.ui_displays[2].zoom_btn.setStyleSheet("image: url(:/display/缩小.png);")
        elif sysman.dlsplay_status != ALLWIN:
            sysman.dlsplay_status = ALLWIN
            sysman.ui.view_box0.setParent(None)
            sysman.ui.view_box1.setParent(None)
            sysman.ui.view_box2.setParent(None)
            sysman.ui.view_box3.setParent(None)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box0, 0,0,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box1, 0,1,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box2, 1,0,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box3, 1,1,1,1)
            sysman.ui.ui_displays[0].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[1].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[2].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[3].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
        
    def zoom_view3(self, sysman):
        if sysman.dlsplay_status == ALLWIN:
            sysman.dlsplay_status = CORNAL
            sysman.ui.view_box0.setParent(None)
            sysman.ui.view_box1.setParent(None)
            sysman.ui.view_box2.setParent(None)
            sysman.ui.view_box3.setParent(None)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box3)
            sysman.ui.ui_displays[3].zoom_btn.setStyleSheet("image: url(:/display/缩小.png);")
        elif sysman.dlsplay_status != ALLWIN:
            sysman.dlsplay_status = ALLWIN
            sysman.ui.view_box0.setParent(None)
            sysman.ui.view_box1.setParent(None)
            sysman.ui.view_box2.setParent(None)
            sysman.ui.view_box3.setParent(None)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box0, 0,0,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box1, 0,1,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box2, 1,0,1,1)
            sysman.ui.visual_layout.addWidget(sysman.ui.view_box3, 1,1,1,1)
            sysman.ui.ui_displays[0].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[1].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[2].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
            sysman.ui.ui_displays[3].zoom_btn.setStyleSheet("image: url(:/display/全屏.png);")
        
    # def rotate_view0(self, sysman, angle = 90):
    #     if sysman.current_visual_dicom_index is None:
    #         return
    #     transform = rotateImage.GetrotateImageMTX([0,0,1], angle)
    #     sysman.dicoms[sysman.current_visual_dicom_index].actors[0].SetUserTransform(transform)
    #     sysman.vtk_renderWindows[0].Render() 
    #     sysman.views[0].update()
    
    # def rotate_view1(self, sysman, angle = 90):
    #     sysman.renderers[1].GetActiveCamera().Roll(angle)
    #     sysman.vtk_renderWindows[1].Render() 
    #     sysman.views[1].update()
        
    # def rotate_view2(self, sysman, angle = 90):
    #     if sysman.current_visual_dicom_index is None:
    #         return
    #     transform = rotateImage.GetrotateImageMTX([1,0,0], angle)
    #     sysman.dicoms[sysman.current_visual_dicom_index].actors[2].SetUserTransform(transform)
    #     sysman.vtk_renderWindows[2].Render() 
    #     sysman.views[2].update()
        
    # def rotate_view3(self, sysman, angle = 90):
    #     if sysman.current_visual_dicom_index is None:
    #         return
    #     transform = rotateImage.GetrotateImageMTX([0,1,0], angle)
    #     sysman.dicoms[sysman.current_visual_dicom_index].actors[3].SetUserTransform(transform)
    #     sysman.vtk_renderWindows[3].Render() 
    #     sysman.views[3].update()
        
    def change_volume_visual_state(self, sysman, state):
        if state: # checked
            volumes = sysman.renderers[1].GetVolumes()  # 获取渲染器中的vtkVolume集合
            volumes.InitTraversal()
            volume = volumes.GetNextItem()
            while volume is not None:
                volume.VisibilityOn()  # 将vtkVolume设为不可见
                volume = volumes.GetNextItem()
                sysman.views[1].update()
        else:
            volumes = sysman.renderers[1].GetVolumes()  # 获取渲染器中的vtkVolume集合
            volumes.InitTraversal()
            volume = volumes.GetNextItem()
            while volume is not None:
                volume.VisibilityOff()  # 将vtkVolume设为不可见
                volume = volumes.GetNextItem()
                sysman.views[1].update()
        
    def change_mesh_visual_state(self, sysman, state):
        if state: # checked
            for mesh in sysman.meshes:
                mesh.refresh()
                self.renderMeshes(mesh, sysman)
                sysman.views[1].update()
            for landmark in sysman.landmarks:
                self.renderLandmarks(landmark, sysman)
                sysman.views[1].update()
            for implant in sysman.implants:
                self.renderImplants(implant, sysman)
                sysman.views[1].update()
            self.updateProject2D(sysman, 0)
            self.updateProject2D(sysman, 2)
            self.updateProject2D(sysman, 3)
        else:
            actors = sysman.renderers[1].GetActors()  # 获取渲染器中的vtkActor集合
            actors.InitTraversal()
            actor = actors.GetNextItem()
            while actor is not None:
                sysman.renderers[1].RemoveActor(actor)  # 直接抹去
                actor = actors.GetNextItem()
            if sysman.ui.location_btn.isChecked():
                sysman.renderers[1].AddActor(sysman.localization_actor)
            sysman.renderers[1].AddActor(sysman.lineActors[0])
            sysman.renderers[1].AddActor(sysman.lineActors[1])
            sysman.renderers[1].AddActor(sysman.lineActors[2])
            for i in [0, 2, 3]:
                sysman.contour_renderers[i].RemoveAllViewProps()
            sysman.add2DLineActors()
        for i in range(4):
            sysman.views[i].update()
        
    def set3DBackgroundTop(self, sysman):
        # 设置初始颜色为RGB(255, 0, 0)
        initial_color = QColor(255, 0, 0)
        # 显示颜色选择对话框，并设置初始颜色
        color = QColorDialog.getColor(initial_color)
        color = np.array([color.red(), color.green(), color.blue()])
        sysman.top_color = color/255
        sysman.box_color = color
        sysman.ui.color3D_btn_top.setStyleSheet(f"background-color: rgb({color[0]}, {color[1]}, {color[2]});")
        sysman.ui.ui_displays[1].box.setStyleSheet("border:None;\n"
                                                    f"background-color: rgb({sysman.box_color[0]}, {sysman.box_color[1]}, {sysman.box_color[2]});")
        sysman.renderers[1].SetBackground(sysman.bot_color)              # 设置页面底部颜色值
        sysman.renderers[1].SetBackground2(sysman.top_color)    # 设置页面顶部颜色值
        sysman.renderers[1].SetGradientBackground(1)   
        sysman.views[1].update()
        pass
    
    def set3DBackgroundBot(self, sysman):
        # 设置初始颜色为RGB(255, 0, 0)
        initial_color = QColor(255, 0, 0)
        # 显示颜色选择对话框，并设置初始颜色
        color = QColorDialog.getColor(initial_color)
        color = np.array([color.red(), color.green(), color.blue()])
        sysman.ui.color3D_btn_bot.setStyleSheet(f"background-color: rgb({color[0]}, {color[1]}, {color[2]});")
        sysman.bot_color = color/255
        sysman.renderers[1].SetBackground(sysman.bot_color)              # 设置页面底部颜色值
        sysman.renderers[1].SetBackground2(sysman.top_color)    # 设置页面顶部颜色值
        sysman.renderers[1].SetGradientBackground(1)   
        sysman.views[1].update()
        pass
                 
    def updateMeshOpacity(self, sysman):
        for i in range(len(sysman.mesh_opacity_sliders)):
            value = sysman.mesh_opacity_sliders[i].value()
            value = min(100, max(value, 0))/100
            if value > 0.98:
                value = 1
            if value < 0.02:
                value = 0
            sysman.meshes[i].setOpacity(value)   
            sysman.views[1].update()  
            
    def updateLandmarkOpacity(self, sysman):
        for i in range(len(sysman.landmark_opacity_sliders)):
            value = sysman.landmark_opacity_sliders[i].value()
            value = min(100, max(value, 0))/100
            if value > 0.98:
                value = 1
            if value < 0.02:
                value = 0
            sysman.landmarks[i].setOpacity(value) 
            sysman.views[1].update()  
            
    def updateToolOpacity(self, sysman):
        for i in range(len(sysman.tool_opacity_sliders)):
            value = sysman.tool_opacity_sliders[i].value()
            value = min(100, max(value, 0))/100
            if value > 0.98:
                value = 1
            if value < 0.02:
                value = 0
            sysman.tools[i].setOpacity(value)  
            sysman.views[1].update()  
                     
    def updateImplantOpacity(self, sysman):
        for i in range(len(sysman.implant_opacity_sliders)):
            value = sysman.implant_opacity_sliders[i].value()
            value = min(100, max(value, 0))/100
            if value > 0.98:
                value = 1
            if value < 0.02:
                value = 0
            sysman.implants[i].setOpacity(value) 
            sysman.views[1].update()  
            
    def lmtw_cell_data_update(self, sysman, Item=None):
        # 如果单元格对象为空
        if Item is None:
            return
        else:
            text = Item.text()  # 获取内容
            row = Item.row()  # 获取行数
            col = Item.column()  # 获取列数
            if 'Radius' in sysman.ui.landmark_tw.horizontalHeaderItem(col).text():
                if text == str(sysman.landmarks[row].getRadius()):
                    return
                if util.is_float(text):#.isnumeric():  
                    r = round(float(text), 3)  # 尝试转换为浮点数 
                    if r == sysman.landmarks[row].getRadius():
                        return
                    sysman.renderers[1].RemoveActor(sysman.landmarks[row].getActor())
                    sysman.landmarks[row].setRadius(r)
                    self.renderLandmarks(sysman.landmarks[row], sysman)
                    radiusItem = QTableWidgetItem(f"{r}")
                    radiusItem.setTextAlignment(0x0004|0x0080)
                    sysman.ui.landmark_tw.setItem(row, col, radiusItem) 
                else:  
                    radiusItem = QTableWidgetItem(f"{sysman.landmarks[row].getRadius()}")
                    radiusItem.setTextAlignment(0x0004 | 0x0080)
                    sysman.ui.landmark_tw.setItem(row, col, radiusItem)
            if 'Scalar' in sysman.ui.landmark_tw.horizontalHeaderItem(col).text():
                if text == f"{sysman.landmarks[row].scalar[0]}, {sysman.landmarks[row].scalar[1]}, {sysman.landmarks[row].scalar[2]}":
                    return
                text_scalar = text.replace(" ", "").split(",")
                scalars = []
                scalar_sign = True
                for scalar in text_scalar:
                    if util.is_float(scalar):#.isnumeric():
                        scalars.append(round(float(scalar), 3))
                    else:
                        scalar_sign = False
                if len(scalars) != 3:
                    scalar_sign = False
                if scalar_sign:
                    sysman.renderers[1].RemoveActor(sysman.landmarks[row].getActor())
                    sysman.landmarks[row].setScalar(scalars)
                    self.renderLandmarks(sysman.landmarks[row], sysman)
                    scalarItem = QTableWidgetItem(f"{scalars[0]}, {scalars[1]}, {scalars[2]}")
                    scalarItem.setTextAlignment(0x0004 | 0x0080)
                    sysman.ui.landmark_tw.setItem(row, col, scalarItem)
                else: 
                    scalarItem = QTableWidgetItem(f"{sysman.landmarks[row].scalar[0]}, {sysman.landmarks[row].scalar[1]}, {sysman.landmarks[row].scalar[2]}")
                    scalarItem.setTextAlignment(0x0004 | 0x0080)
                    sysman.ui.landmark_tw.setItem(row, col, scalarItem)
        return

    def iptw_cell_data_update(self, sysman, Item=None):
        # 如果单元格对象为空
        if Item is None:
            return
        else:
            text = Item.text()  # 获取内容
            row = Item.row()  # 获取行数
            col = Item.column()  # 获取列数
            if 'Start' in sysman.ui.implant_tw.horizontalHeaderItem(col).text():
                if text == f"{sysman.implants[row].start[0]}, {sysman.implants[row].start[1]}, {sysman.implants[row].start[2]}":
                    return
                text_scalar = text.replace(" ", "").split(",")
                scalars = []
                scalar_sign = True
                for scalar in text_scalar:
                    if util.is_float(scalar):#.isnumeric():
                        scalars.append(float(scalar))
                    else:
                        scalar_sign = False
                if len(scalars) != 3:
                    scalar_sign = False
                if scalar_sign:
                    sysman.renderers[1].RemoveActor(sysman.implants[row].getTubeActor())
                    sysman.renderers[1].RemoveActor(sysman.implants[row].getDashActor())
                    sysman.implants[row].setStart(scalars)
                    self.renderImplants(sysman.implants[row], sysman)
                    scalarItem = QTableWidgetItem(f"{scalars[0]}, {scalars[1]}, {scalars[2]}")
                    scalarItem.setTextAlignment(0x0004 | 0x0080)
                    sysman.ui.implant_tw.setItem(row, col, scalarItem)
                else: 
                    scalarItem = QTableWidgetItem( f"{sysman.implants[row].start[0]}, {sysman.implants[row].start[1]}, {sysman.implants[row].start[2]}")
                    scalarItem.setTextAlignment(0x0004 | 0x0080)
                    sysman.ui.implant_tw.setItem(row, col, scalarItem)
            if 'End' in sysman.ui.implant_tw.horizontalHeaderItem(col).text():
                if text == f"{sysman.implants[row].end[0]}, {sysman.implants[row].end[1]}, {sysman.implants[row].end[2]}":
                    return
                text_scalar = text.replace(" ", "").split(",")
                scalars = []
                scalar_sign = True
                for scalar in text_scalar:
                    if util.is_float(scalar):#.isnumeric():
                        scalars.append(float(scalar))
                    else:
                        scalar_sign = False
                if len(scalars) != 3:
                    scalar_sign = False
                if scalar_sign:
                    sysman.renderers[1].RemoveActor(sysman.implants[row].getTubeActor())
                    sysman.renderers[1].RemoveActor(sysman.implants[row].getDashActor())
                    sysman.implants[row].setEnd(scalars)
                    self.renderImplants(sysman.implants[row], sysman)
                    scalarItem = QTableWidgetItem(f"{scalars[0]}, {scalars[1]}, {scalars[2]}")
                    scalarItem.setTextAlignment(0x0004 | 0x0080)
                    sysman.ui.implant_tw.setItem(row, col, scalarItem)
                else: 
                    scalarItem = QTableWidgetItem( f"{sysman.implants[row].end[0]}, {sysman.implants[row].end[1]}, {sysman.implants[row].end[2]}")
                    scalarItem.setTextAlignment(0x0004 | 0x0080)
                    sysman.ui.implant_tw.setItem(row, col, scalarItem)
            if 'Radius' in sysman.ui.implant_tw.horizontalHeaderItem(col).text():
                if text == str(sysman.implants[row].getRadius()):
                    return
                if util.is_float(text):#.isnumeric():  
                    r = round(float(text), 3)  # 尝试转换为浮点数 
                    if r == sysman.implants[row].getRadius():
                        return
                    sysman.renderers[1].RemoveActor(sysman.implants[row].getTubeActor())
                    sysman.renderers[1].RemoveActor(sysman.implants[row].getDashActor())
                    sysman.implants[row].setRadius(r)
                    self.renderImplants(sysman.implants[row], sysman)
                    radiusItem = QTableWidgetItem(f"{r}")
                    radiusItem.setTextAlignment(0x0004|0x0080)
                    sysman.ui.implant_tw.setItem(row, col, radiusItem) 
                else:  
                    radiusItem = QTableWidgetItem(f"{sysman.implants[row].getRadius()}")
                    radiusItem.setTextAlignment(0x0004 | 0x0080)
                    sysman.ui.implant_tw.setItem(row, col, radiusItem)
        return

        
    
        
    
