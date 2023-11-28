from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import numpy as np
from config import ALLWIN, TRANSS, SAGITA, VIEW3D
import ImportAndSave.importDicom as importDicom
import ImportAndSave.importImplant as importImplant
import ImportAndSave.importIni as importIni
import ImportAndSave.importMesh as importMesh
import ImportAndSave.importTool as importTool
import ImportAndSave.importTxt as importTxt
import dicom as m_dicom
import mesh as m_mesh
import implant as m_implant
import landmark as m_landmark
import SimpleITK as sitk
import copy
import config


class slot_functions():
    def __init__(self):
        super(slot_functions, self).__init__()

    def addSystemDicoms(self, path, sysman):
        dicom_series, images = importDicom.importDicom(path)
        if len(dicom_series) == 0 or images is None:
            sysman.printInfo("There is no dicom file in the folder:" + path)
            return
        patient_name = str(dicom_series[0].PatientName)
        patient_age = str(dicom_series[0].PatientAge)
        image_array = np.array(sitk.GetArrayFromImage(images))
        current_row = len(sysman.dicoms)
        sysman.dicoms.append(m_dicom.dicom(data=image_array, Name=patient_name, Age=patient_age, resolution=image_array.shape, filePath=path)) # (data, Name=None, Age=None, filePath=None, resolution=None)
        sysman.ui.dicom_tw.insertRow(current_row)
        # 设置单元格的内容
        # print(sysman.dicoms[-1].resolution)
        sysman.ui.dicom_tw.setItem(current_row, 0, QTableWidgetItem(sysman.dicoms[-1].name))
        sysman.ui.dicom_tw.setItem(current_row, 1, QTableWidgetItem(sysman.dicoms[-1].age))
        sysman.ui.dicom_tw.setItem(current_row, 2, QTableWidgetItem(str(sysman.dicoms[-1].resolution[0]) + "x" + str(sysman.dicoms[-1].resolution[1]) + "x" + str(sysman.dicoms[-1].resolution[2])))
        sysman.ui.dicom_tw.setItem(current_row, 3, QTableWidgetItem(sysman.dicoms[-1].path))
    
    def addSystemSTL(self, path, sysman):
        new_stl = importMesh.importSTL(path)
        path = path.replace("\\", "/")
        name = path.split("/")[-1].split('.')[0]
        current_row = len(sysman.meshs)
        sysman.meshs.append(m_mesh.mesh(polydata=new_stl, Name=name, filePath=path))
        sysman.ui.mesh_tw.insertRow(current_row)
        # 设置单元格的内容
        # print(sysman.dicoms[-1].resolution)
        sysman.ui.mesh_tw.setItem(current_row, 0, QTableWidgetItem(sysman.meshs[-1].name))
        sysman.ui.mesh_tw.setItem(current_row, 1, QTableWidgetItem(' ').setIcon(sysman.unvisible_icon if sysman.meshs[-1].visible else sysman.visible_icon))
        sysman.ui.mesh_tw.setItem(current_row, 2, QTableWidgetItem(' ').setBackground(QColor(sysman.meshs[-1].color[0], sysman.meshs[-1].color[1], sysman.meshs[-1].color[2])))
        sysman.ui.mesh_tw.setItem(current_row, 3, QTableWidgetItem(sysman.meshs[-1].path))
    
    
    def addSystemOBJ(self, path, sysman):
        new_stl = importMesh.importOBJ(path)
        path = path.replace("\\", "/")
        name = path.split("/")[-1].split('.')[0]
        sysman.meshs.append(m_mesh.mesh(polydata=new_stl, Name=name, filePath=path))
        
    def addSystemImplant(self, path, sysman):
        implants = importImplant.importImplant(path)
        for implant in implants:
            try:
                sysman.implants.append(m_implant.implants(start=np.array([float(element) for element in implant[0]]), end=np.array([float(element) for element in implant[1]]), radius=float(implant[2]), color=np.array([int(element) for element in implant[3]])))
            except ValueError:
                QMessageBox.warning(sysman.ui, 'Warning', 'Implant error!', QMessageBox.Ok)
                sysman.printInfo("Invalid string format for float conversion! Please check your implant file!")
                
            
    def addSystemLandmark(self, pointlist, sysman):
        tmp_point = []
        for i in range(len(pointlist)):
            tmp_point.append(float(pointlist[i]))
            if len(tmp_point) == 3:
                sysman.landmarks.append(m_landmark.landmark(scalar = copy.deepcopy(tmp_point)))
                tmp_point = []
                
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
        SROM_filter = "*.rom"
        SROM_list = [file for file in os.listdir(path) if file.endswith(SROM_filter) and os.path.isfile(os.path.join(path, file))]
        for file in SROM_list:
            file_name = os.path.splitext(file)[0]
            SROM_path = os.path.join(path, file)
            sysman.SROM_path_map[file_name] = SROM_path
            sysman.SROM_name.append(file_name)
            
    def buildAll(self, path, sysman):
        if not os.path.exists(path):
            sysman.printInfo("Path:\""+path+"\" does not work!")
            return 
        files = os.listdir(path)
        num_files = len(files)
        for i in range(num_files):
            QCoreApplication.processEvents() # 防卡顿
            sysman.showProgress(int(100*i/num_files))
        for i in range(num_files):
            f = files[num_files-i-1]
            file_path = os.path.join(path, f)
            numOfSTLs = len(sysman.meshs)
            numOfImplants = len(sysman.implants)
            numOfDicomss = len(sysman.dicoms)
            numOfRoms = len(sysman.SROM_name)
            if f.lower().endswith('.stl'):
                self.addSystemSTL(file_path, sysman)
                if len(sysman.meshs) > numOfSTLs:
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
                if len(sysman.SROM_name) > numOfRoms:
                    sysman.printInfo("Add ROM files.")
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
        path = path.replace("\\", "/")
        name = file_name.split("/")[-1]
        file_extension = name.split(".")[-1]
        if file_extension == "dcm":
            self.addSystemDicoms(file_name, sysman)
            pass
        elif file_extension == "stl":
            self.addSystemSTL(file_name, sysman)
            pass
        elif file_extension == "obj":
            self.addSystemOBJ(file_name, sysman)
            pass
        elif file_extension == "implant":
            self.addSystemImplant(file_name, sysman)
            pass
        # elif file_extension == "txt":
        #     pass
        elif file_extension == "rom":
            pass
        elif file_extension == "ini":
            self.buildSystemSetting(file_name, sysman)
            pass
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
        pass
    
    def registration(self, sysman):
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
    
    def show3D(self, sysman):
        pass
    
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
        
    @staticmethod    
    def get_files(dir, fileType=None):
        pass
        
    
