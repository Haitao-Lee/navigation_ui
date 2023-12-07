from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import numpy as np
from vtk.util import numpy_support
from config import ALLWIN, TRANSS, SAGITA, VIEW3D
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


class slot_functions():
    def __init__(self):
        super(slot_functions, self).__init__()
        
    def addTableDicoms(self, sysman, new_dicom):
        current_row = len(sysman.dicoms)
        sysman.dicoms.append(new_dicom) # (data, Name=None, Age=None, filePath=None, resolution=None)
        sysman.ui.dicom_tw.insertRow(current_row)
        nameItem = QTableWidgetItem(sysman.dicoms[-1].name)
        nameItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.dicom_tw.setItem(current_row, 0, nameItem)
        ageItem = QTableWidgetItem(sysman.dicoms[-1].age)
        ageItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.dicom_tw.setItem(current_row, 1, ageItem)
        resolutionItem = QTableWidgetItem(str(sysman.dicoms[-1].resolution[0]) + "x" + str(sysman.dicoms[-1].resolution[1]) + "x" + str(sysman.dicoms[-1].resolution[2]))
        resolutionItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.dicom_tw.setItem(current_row, 2, resolutionItem)
        pathItem = QTableWidgetItem(sysman.dicoms[-1].path)
        pathItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.dicom_tw.setItem(current_row, 3, pathItem)
        # 设置列宽度以适应每列中各自字符串的长度
        for j in range(sysman.ui.dicom_tw.columnCount()):
            max_width = 0
            for i in range(sysman.ui.dicom_tw.rowCount()):
                item = sysman.ui.dicom_tw.item(i, j)
                if item:
                    text_width = sysman.ui.dicom_tw.fontMetrics().boundingRect(item.text()).width()
                    if text_width > max_width:
                        max_width = text_width*config.text_margin
            sysman.ui.dicom_tw.setColumnWidth(j, max(max_width, config.min_margin))
    
    def addTableSTL(self, sysman, newSTL):
        current_row = len(sysman.meshes)
        sysman.meshes.append(newSTL)
        sysman.ui.mesh_tw.insertRow(current_row)
        visible_widget = createVisibleWidget.createVisibleWidget(sysman.meshes[-1].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
        color_widget = createColorWidget.createColorWidget(sysman.meshes[-1].color)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
        nameItem = QTableWidgetItem(sysman.meshes[-1].name)
        nameItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.mesh_tw.setItem(current_row, 0, nameItem)
        sysman.ui.mesh_tw.setCellWidget(current_row, 1, visible_widget)
        sysman.ui.mesh_tw.setCellWidget(current_row, 2, color_widget)
        pathItem = QTableWidgetItem(sysman.meshes[-1].path)
        pathItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.mesh_tw.setItem(current_row, 3, pathItem)
        # 设置列宽度以适应每列中各自字符串的长度
        for j in range(sysman.ui.mesh_tw.columnCount()):
            max_width = 0
            for i in range(sysman.ui.mesh_tw.rowCount()):
                item = sysman.ui.mesh_tw.item(i, j)
                if item:
                    text_width = sysman.ui.mesh_tw.fontMetrics().boundingRect(item.text()).width()
                    if text_width > max_width:
                        max_width = text_width*config.text_margin
            sysman.ui.mesh_tw.setColumnWidth(j, max(max_width, config.min_margin))
        self.renderMeshes(sysman.meshes[-1], sysman)
            
    def addTableImplant(self, sysman, newImplant):
        try:
            current_row = len(sysman.implants)
            sysman.implants.append(newImplant)
            # 更新UI中的列表
            sysman.ui.implant_tw.insertRow(current_row)
            visible_widget = createVisibleWidget.createVisibleWidget(sysman.implants[-1].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
            color_widget = createColorWidget.createColorWidget(sysman.implants[-1].color)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
            startItem = QTableWidgetItem(f"{sysman.implants[-1].start[0]}, {sysman.implants[-1].start[1]}, {sysman.implants[-1].start[2]}")
            startItem.setTextAlignment(0x0004 | 0x0080)
            sysman.ui.implant_tw.setItem(current_row, 0, startItem)
            endItem = QTableWidgetItem(f"{sysman.implants[-1].end[0]}, {sysman.implants[-1].end[1]}, {sysman.implants[-1].end[2]}")
            endItem.setTextAlignment(0x0004 | 0x0080)
            sysman.ui.implant_tw.setItem(current_row, 1, endItem)
            radiusItem = QTableWidgetItem(f"{sysman.implants[-1].radius}")
            radiusItem.setTextAlignment(0x0004 | 0x0080)
            sysman.ui.implant_tw.setItem(current_row, 2, radiusItem)
            sysman.ui.implant_tw.setCellWidget(current_row, 3, color_widget)
            sysman.ui.implant_tw.setCellWidget(current_row, 4, visible_widget) 
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
        except ValueError:
            QMessageBox.warning(sysman.ui, 'Warning', 'Implant error!', QMessageBox.Ok)
            sysman.printInfo("Invalid string format for float conversion! Please check your implant file!")
            
    def addTableLandmark(self, sysman, newLandmark):
        current_row = len(sysman.landmarks)
        sysman.landmarks.append(newLandmark)
        tmp_point = []
        # 更新UI中的列表
        sysman.ui.landmark_tw.insertRow(current_row)
        visible_widget = createVisibleWidget.createVisibleWidget(sysman.landmarks[-1].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
        color_widget = createColorWidget.createColorWidget(sysman.landmarks[-1].color)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
        scalartItem = QTableWidgetItem(f"{sysman.landmarks[-1].scalar[0]}, {sysman.landmarks[-1].scalar[1]}, {sysman.landmarks[-1].scalar[2]}")
        scalartItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.landmark_tw.setItem(current_row, 0, scalartItem)
        sysman.ui.landmark_tw.setCellWidget(current_row, 1, color_widget)
        sysman.ui.landmark_tw.setCellWidget(current_row, 2, visible_widget) 
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
            
    def addTableTool(self, sysman, newTool):
        current_row = len(sysman.tools)
        sysman.tools.append(newTool)
        sysman.ui.tool_tw.insertRow(current_row)
        # 更新UI中的列表
        visible_widget = createVisibleWidget.createVisibleWidget(sysman.tools[-1].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
        color_widget = createColorWidget.createColorWidget(sysman.tools[-1].color)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
        nameItem = QTableWidgetItem(sysman.tools[-1].name)
        nameItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.tool_tw.setItem(current_row, 0, nameItem)
        sysman.ui.tool_tw.setCellWidget(current_row, 1, visible_widget)
        sysman.ui.tool_tw.setCellWidget(current_row, 2, color_widget)
        pathItem = QTableWidgetItem(sysman.tools[-1].path)
        pathItem.setTextAlignment(0x0004 | 0x0080)
        sysman.ui.tool_tw.setItem(current_row, 3, pathItem)
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
        sysman.ui.rom_tw.setItem(current_row, 0, nameItem)
        pathItem = QTableWidgetItem(sysman.roms[-1].path)
        pathItem.setTextAlignment(0x0004 | 0x0080)
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
        dicom_series, images = importDicom.importDicom(path)
        if images is None:
            sysman.printInfo("There is no dicom file in the folder:" + path)
            return
        patient_name = str(dicom_series[0].PatientName)
        patient_age = str(dicom_series[0].PatientAge)
        image_array = sitk.GetArrayFromImage(images)
        # 创建VTK图像数据
        vtk_image = vtk.vtkImageData()
        vtk_image.SetDimensions(images.GetSize()[0], images.GetSize()[1], images.GetDepth())  # 注意维度的顺序可能需要颠倒
        vtk_image.SetSpacing(images.GetSpacing())
        vtk_image.SetOrigin(images.GetOrigin())
        vtk_image.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)
        vtk_array = numpy_support.numpy_to_vtk(image_array.ravel(), deep=True)
        vtk_image.GetPointData().SetScalars(vtk_array) # 将NumPy数组数据复制到VTK图像数据中
        vtk_image.SetSpacing(images.GetSpacing())
        QCoreApplication.processEvents()
        # image_array = get_pixels_hu.get_pixels_hu(image_array, dicom_series)
        QCoreApplication.processEvents()
        new_dicom = m_dicom.dicom(arrayData=image_array, imageData=vtk_image, Name=patient_name, Age=patient_age, resolution=image_array.shape, filePath=path)
        new_dicom.createActors(sysman.LUT2D, sysman.CTF3D, sysman.PWF3D)
        self.addTableDicoms(sysman, new_dicom)   
        QCoreApplication.processEvents()     
        self.renderDicoms(new_dicom, sysman)
    
    def addSystemSTL(self, path, sysman):
        new_stl = importMesh.importSTL(path)
        path = path.replace("\\", "/")
        name = path.split("/")[-1].split('.')[0]
        newSTL = m_mesh.mesh(polydata=new_stl, Name=name, filePath=path)
        self.addTableSTL(sysman, newSTL)
    
    def addSystemOBJ(self, path, sysman):
        new_stl = importMesh.importOBJ(path)
        path = path.replace("\\", "/")
        name = path.split("/")[-1].split('.')[0]
        newSTL = m_mesh.mesh(polydata=new_stl, Name=name, filePath=path)
        self.addTableSTL(sysman, newSTL)
        
    def addSystemImplant(self, path, sysman):
        implants = importImplant.importImplant(path)
        for implant in implants:
            newImplant = m_implant.implants(start=np.array([float(element) for element in implant[0]]), end=np.array([float(element) for element in implant[1]]), radius=float(implant[2]), color=np.array([int(element) for element in implant[3]]))
            self.addTableImplant(sysman, newImplant)
                
    def addSystemLandmark(self, pointlist, sysman):
        tmp_point = []
        for i in range(len(pointlist)):
            tmp_point.append(float(pointlist[i]))
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
        sysman.landmarks = [] # 清空原来的定点
        sysman.TrackerHostName = None # 清空原来的设备名，用于判断是否读取成功
        self.addSystemLandmark(pointlist, sysman)
        sysman.TrackerHostName = settings.get('General', 'TrackerHostName')
        tmp_matrix = settings.get('General', 'probeDeviateMatrix').split(",")
        try:
            sysman.probeDeviateMatrix = np.array([float(element) for element in tmp_matrix]).reshape(4, 4)
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
                    sysman.printInfo("Add dicoms in:" + path)
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
        if file_extension == "stl":
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
        pass
    
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
        pass
    
    def undo(self, sysman):
        pass
    
    def reset(self, sysman):
        pass
    
    def measure(self, sysman):
        pass
        
    def volume_calculation(self, sysman):
        if sysman.current_mesh is None:
            sysman.printInfo("<b>Bold\033[91m Please select a mesh!\033[0m.</b>") # 加粗加红
            return 
        volume = volumeOfMesh.volumeOfMesh(sysman.current_mesh.getPolydata())
        sysman.printInfo(f"The volume of the selected mesh: \n            {volume} mm{config.cubic}") # 加粗加红
    
    def project2D(self, sysman):
        pass
    
    def addDicom(self, sysman):
        path = QFileDialog.getExistingDirectory(sysman.ui, 'select the dicom folder', os.getcwd())
        if not os.path.exists(path):
            sysman.printInfo("Path:\""+path+"\" does not work!")
            return
        sysman.ProgressStart()
        self.addSystemDicoms(path, sysman)
        sysman.ProgressMiddle()
        sysman.ProgressEnd()
        sysman.printInfo("Successfully import dicoms in:" + path)
        pass
        
    def deleteDicom(self, sysman):
        pass
          
    def addMesh(self, sysman):
        file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a mesh file', "C:/", f"STL(*.stl);OBJ(*.obj);All Files(*)")
        if file_name is None:
            return
        name = file_name.split("/")[-1]
        file_extension = name.split(".")[-1]
        if file_extension == "stl":
            self.addSystemSTL(file_name, sysman)
        elif file_extension == "obj":
            self.addSystemOBJ(file_name, sysman)
        pass
    
    def changeMeshColor(self, sysman):
        pass
    
    def deleteMesh(self, sysman):
        pass
        
    def addImplant(self, sysman):
        pass
    
    def changeImplantColor(self, sysman):
        pass
    
    def deleteImplant(self, sysman):
        pass
    
    def addLandmark(self, sysman):
        pass
    
    def changeLandmarkColor(self, sysman):
        pass
    
    def deleteLandmark(self, sysman):
        pass
    
    def addTool(self, sysman):
        pass
    
    def changeToolColor(self, sysman):
        pass
    
    def deleteTool(self, sysman):
        pass
    
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
        
    def renderDicoms(self, dicom, sysman):
        for i in range(4):
            sysman.renderers[i].RemoveAllViewProps()
            QCoreApplication.processEvents()
            if i == 1:
                sysman.renderers[i].AddVolume(dicom.actors[i])
            else:
                sysman.renderers[i].AddActor(dicom.actors[i])
                sysman.renderers[i].GetActiveCamera().SetParallelProjection(1)
                # sysman.renderers[i].GetActiveCamera().SetParallelScale(config.ParallelScale)
                # 
            sysman.renderers[i].ResetCamera()
            sysman.renderers[i].GetActiveCamera().Zoom(config.zoom)
            sysman.vtk_renderWindows[i].Render() 
            sysman.views[i].update()
            
    def renderMeshes(self, mesh, sysman):
        sysman.renderers[1].AddActor(mesh.actor)
        sysman.renderers[1].ResetCamera()
        sysman.vtk_renderWindows[1].Render() 
        sysman.views[1].update()
    
    def on_dicom_table_clicked(self, sysman, row, column ):
        sysman.current_dicom = sysman.dicoms[row]
        pass
    
    def on_mesh_table_clicked(self, sysman, row, column):
        sysman.current_mesh = sysman.meshes[row]
        if column == 1:
            sysman.meshes[row].changeVisible()
            # widget = sysman.ui.mesh_tw.cellWidget(row, column)
            visible_widget = createVisibleWidget.createVisibleWidget(sysman.meshes[row].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
            sysman.ui.mesh_tw.setCellWidget(row, column, visible_widget)
            sysman.renderers[1].ResetCamera()
            sysman.vtk_renderWindows[1].Render() 
            sysman.views[1].update()
        pass
    
    def on_implant_table_clicked(self, sysman, row, column):
        sysman.current_implant = sysman.implants[row]
        if column == 4:
            sysman.implants[row].changeVisible()
            visible_widget = createVisibleWidget.createVisibleWidget(sysman.implants[row].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
            sysman.ui.implant_tw.setCellWidget(row, column, visible_widget)
            sysman.renderers[1].ResetCamera()
            sysman.vtk_renderWindows[1].Render() 
            sysman.views[1].update()
        pass
    
    def on_landmark_table_clicked(self, sysman, row, column):
        sysman.current_landmark = sysman.landmarks[row]
        if column == 2:
            sysman.landmarks[row].changeVisible()
            visible_widget = createVisibleWidget.createVisibleWidget(sysman.landmarks[row].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
            sysman.ui.landmark_tw.setCellWidget(row, column, visible_widget)
            sysman.renderers[1].ResetCamera()
            sysman.vtk_renderWindows[1].Render() 
            sysman.views[1].update()
        pass
    
    def on_rom_table_clicked(self, sysman, row, column):
        sysman.current_rom = sysman.roms[row]
        pass
    
    def on_tool_table_clicked(self, sysman, row, column):
        sysman.current_tool = sysman.tools[row]
        if column == 1:
            sysman.tools[row].changeVisible()
            # widget = sysman.ui.mesh_tw.cellWidget(row, column)
            visible_widget = createVisibleWidget.createVisibleWidget(sysman.tools[row].visible)  # 创建一个新的小部件，设置布局并将其设置为单元格的部件
            sysman.ui.tool_tw.setCellWidget(row, column, visible_widget)
            sysman.renderers[1].ResetCamera()
            sysman.vtk_renderWindows[1].Render() 
            sysman.views[1].update()
        pass
    
        
    
