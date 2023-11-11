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

    def import_file(self, ui, file_type=None): 
        file_name = None
        if file_type:
            file_name, _ = QFileDialog.getOpenFileName(ui, f'select a {file_type} file', "C:/", f"{file_type}(*.{file_type});All Files(*)")
        else: 
            file_name, _ = QFileDialog.getOpenFileName(ui, f'select a file', "C:/", f"All Files(*)")
        pass
                                   
    def import_folder(self, ui):
        path = QFileDialog.getExistingDirectory(ui, 'select a folder', os.getcwd())
        pass
    
    def open_setting(self, ui):
        pass
    
    def open_help(self, ui):
        pass
    
    def adjust_seg(ui, sys_man):
        pass
    
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
        
    def conection2ndi(self):
        pass
    
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
        
    
