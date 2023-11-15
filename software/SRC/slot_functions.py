from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import numpy as np
from config import ALLWIN, TRANSS, SAGITA, VIEW3D

class slot_functions():
    def __init__(self):
        super(slot_functions, self).__init__()

    @staticmethod
    def import_file(sysman, file_type=None): 
        file_name = None
        if file_type:
            file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a {file_type} file', "C:/", f"{file_type}(*.{file_type});All Files(*)")
        else: 
            file_name, _ = QFileDialog.getOpenFileName(sysman.ui, f'select a file', "C:/", f"All Files(*)")
        pass
           
    @staticmethod                        
    def import_folder(sysman):
        path = QFileDialog.getExistingDirectory(sysman.ui, 'select a folder', os.getcwd())
        pass
    
    def save_all(sysman):
        pass
    
    @staticmethod
    def open_setting(sysman):
        pass
    
    @staticmethod
    def open_help(sysman):
        pass
    
    @staticmethod
    def conect2ndi(sysman):
        pass
    
    @staticmethod
    def registration(sysman):
        pass
    
    @staticmethod
    def calibration(sysman):
        pass
    
    @staticmethod
    def conect2robo(sysman):
        pass
    
    @staticmethod
    def localization(sysman):
        pass
         
        
    def adjust(self, sys_man):
        sys_man.ui.adjustment_ui.show()
    
    @staticmethod
    def print_info(item, messages):
        print("print_info")
        item.appendPlainText(messages + '\n')
        pass
    
    @staticmethod
    def save(self, data, dir, name, fileType):
        print("save slot")
        
    def quit(self):
        app = QApplication.instance()
        app.quit()
    
    @staticmethod
    def setColor(self):
        pass
    
    def setSTLColor(stl):
        pass
    
    def delete(self):
        pass
        
    def visual_slot(self):
        pass
    
    @staticmethod
    def changeLight(item, sign=True):
        pass
        
        
    @staticmethod    
    def get_files(self, dir, fileType=None):
        pass
        
    
