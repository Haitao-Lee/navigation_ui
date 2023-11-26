from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import numpy as np
from config import ALLWIN, TRANSS, SAGITA, VIEW3D
import ImportAndSave.importDicom as importDicom
import ImportAndSave.importImplant as importImplant
import ImportAndSave.importLandmark as importLandmark
import ImportAndSave.importSTL as importSTL
import ImportAndSave.importTool as importTool
import ImportAndSave.importTxt as importTxt
import dicom as m_dicom
import mesh as m_mesh
import implant as m_implant
import SimpleITK as sitk


class slot_functions():
    def __init__(self):
        super(slot_functions, self).__init__()

    def buildSystemDicom(path, sysman):
        new_dicom = importDicom.importDicom(path)
        patient_name = new_dicom.GetMetaData("0010|0010")  
        patient_age = new_dicom.GetMetaData("0010|1010")
        image_array = sitk.GetArrayFromImage(new_dicom)
        sysman.dicoms.append(m_dicom(data=new_dicom, Name=patient_name, Age=patient_age, resolution=image_array, filePath=path)) # (data, Name=None, Age=None, filePath=None, resolution=None)
    
    def buildSystemSTL(path, sysman):
        new_stl = importSTL.importSTL(path)
        name = path.split("/")[-1]
        sysman.meshs.append(m_mesh(polydata=new_stl, Name=name, filePath=path))
        
    def buildSystemOBJ(path, sysman):
        new_stl = importSTL.importOBJ(path)
        name = path.split("/")[-1]
        sysman.meshs.append(m_mesh(polydata=new_stl, Name=name, filePath=path))
        
    def buildSystemImplant(path, sysman):
        implants = importImplant.importImplant(path)
        name = path.split("/")[-1]
        for implant in implants:
            sysman.implants.append(m_implant(start=implant[0], end=implant[1], radius=implant[2]/2, color=implant[3]))


    def import_file(self, sysman, file_type=None): 
        file_name = None
        if file_type:
            file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a {file_type} file', "C:/", f"{file_type}(*.{file_type});All Files(*)")
        else: 
            file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a file', "C:/", f"All Files(*)")
        if file_name is None:
            return
        name = file_name.split("/")[-1]
        file_extension = name.split(".")[-1]
        print(file_extension)
        if file_extension == "dcm":
            self.buildSystemDicoms(file_name, sysman)
            pass
        elif file_extension == "stl":
            pass
        elif file_extension == "obj":
            pass
        elif file_extension == "implant":
            pass
        elif file_extension == "txt":
            pass
        elif file_extension == "rom":
            pass
        elif file_extension == "ini":
            pass
        else:
            QMessageBox.warning(sysman.ui, 'Warning', 'The file is not appropriate!', QMessageBox.Ok)
        pass
           
    def import_folder(self, sysman):
        path = QFileDialog.getExistingDirectory(sysman.ui, 'Choose Source File Which Should Include Image, NDI File, Implant Files and so on', os.getcwd())
        
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
        self.buildSystemDicoms(path, sysman)
        pass
        
    def deleteDicom(self, sysman):
        pass
          
    def addMesh(self, sysman):
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
    
    @staticmethod
    def print_info(item, messages):
        item.appendPlainText(messages + '\n')
        pass
    
    def setLight(self, item, sign=True):
        pass
    
    def addLight(self, sysman):
        pass  
        
    @staticmethod    
    def get_files(dir, fileType=None):
        pass
        
    
