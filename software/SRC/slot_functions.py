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


class slot_functions():
    def __init__(self):
        super(slot_functions, self).__init__()

    def addSystemDicoms(self, path, sysman):
        sysman.ProgressStart()
        dicom_series, images = importDicom.importDicom(path)
        sysman.ProgressMiddle()
        if len(dicom_series) == 0:
            sysman.printInfo("--There is no dicom file in the folder:" + path)
            return
        patient_name = dicom_series[0].PatientName
        patient_age = dicom_series[0].PatientAge
        image_array = sitk.GetArrayFromImage(images)
        sysman.dicoms.append(m_dicom.dicom(data=image_array, Name=patient_name, Age=patient_age, resolution=image_array, filePath=path)) # (data, Name=None, Age=None, filePath=None, resolution=None)
        sysman.ProgressEnd()
    
    def addSystemSTL(self, path, sysman):
        new_stl = importMesh.importSTL(path)
        name = path.split("/")[-1]
        sysman.meshs.append(m_mesh.mesh(polydata=new_stl, Name=name, filePath=path))
        
    def addSystemOBJ(self, path, sysman):
        new_stl = importMesh.importOBJ(path)
        name = path.split("/")[-1]
        sysman.meshs.append(m_mesh.mesh(polydata=new_stl, Name=name, filePath=path))
        
    def addSystemImplant(self, path, sysman):
        implants = importImplant.importImplant(path)
        for implant in implants:
            sysman.implants.append(m_implant.implants(start=implant[0], end=implant[1], radius=implant[2], color=implant[3]))
            
    def addSystemLandmark(self, pointlist, sysman):
        tmp_point = []
        for i in range(len(pointlist)):
            tmp_point.append(float(pointlist[i]))
            if len(tmp_point) == 3:
                sysman.landmarks.append(m_landmark.landmark(scalar = copy.deepcopy(tmp_point)))
                tmp_point = []
                
    def buildSystemSetting(self, path, sysman):
        settings = importIni.importIni(path)
        pointlist= settings.get('General', 'FiducialPoints').split(',')
        sysman.landmarks = [] # 清空原来的定点
        self.addSystemLandmark(pointlist, sysman)
        sysman.TrackerHostName = settings.get('General', 'TrackerHostName')
        sysman.probeDeviateMatrix = np.array(settings.get('General', 'probeDeviateMatrix')).reshape(4, 4)    
        
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
            sysman.printInfo("--Path:\""+path+"\" does not work!")
            return 
        # NDI_path = path + 'NDIFiles'
        # if os.path.exists(NDI_path):
        #     self.buildSystemRom(NDI_path, sysman)
        files = os.listdir(path)
        num_files = len(files)
        for i in range(num_files):
            QCoreApplication.processEvents() # 防卡顿
            sysman.showProgress(int(100*i/num_files))
            f = files[i]
            file_path = os.path.join(path, f)
            if f.lower().endswith('.stl'):
                self.addSystemSTL(file_path, sysman)
                sysman.printInfo("--Add STL:\""+file_path+"\".")
            elif f.lower().endswith('.implant'):
                self.addSystemImplant(file_path, sysman)
                sysman.printInfo("--Add implants:\""+file_path+"\".")
            elif f.lower().endswith('.ini'):
                self.buildSystemSetting(file_path, sysman)
                sysman.printInfo("--Add settings:\""+file_path+"\".")
            elif 'NDIFiles' in f:
                self.buildSystemRom(file_path, sysman)
                sysman.printInfo("--Add ROM files.")
            else:
                self.addSystemDicoms(file_path, sysman)
                sysman.printInfo("--Add dicoms in:" + path)
        sysman.ProgressEnd()
                

    def import_file(self, sysman, file_type=None): 
        file_name = None
        if file_type:
            file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a {file_type} file', "C:/", f"{file_type}(*.{file_type});All Files(*)")
        else: 
            file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a file', "C:/", f"All Files(*)")
        if not os.path.exists(file_name):
            sysman.printInfo("--No document was selected!")
            return
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
        sysman.printInfo("--Import file:" + file_name)
        pass
           
    def import_folder(self, sysman):
        path = QFileDialog.getExistingDirectory(sysman.ui, 'Choose Source File Which Should Include Image, NDI File, Implant Files and so on', os.getcwd())
        if not os.path.exists(path):
            return
        self.buildAll(path, sysman)
        pass
    
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
            sysman.printInfo("--Path:\""+path+"\" does not work!")
            return
        self.addSystemDicoms(path, sysman)
        sysman.printInfo("--Successfully import dicoms in:" + path)
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
        
    
