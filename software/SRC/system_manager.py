import UI.ui_all as ui_all
import slot_functions
import config
from functools import partial
import vtkmodules.all as vtk
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class system_manager():
    def __init__(self):
        super(system_manager, self).__init__()
        # ui
        self.ui = ui_all.ui_all()
        self.slot_fs = slot_functions.slot_functions()
        
        # timer
        self.socket_timer = QTimer()
        self.regis_timer = QTimer()
        
        # setting
        self.connections = None
        self.robotics = None
        
        # adjustment
        self.lookupTable = vtk.vtkLookupTable()
        self.lower2Dvalues
        self.upper2Dvalues
        self.lower3Dvalues
        self.upper3Dvalues
        
        # data
        self.dicoms = []
        self.meshs =[]
        self.implants =[]
        self.tools = []
        self.landmarks =[]
        
        # setup
        self.setupConnections()       
        
    def setupConnections(self):
        self.ui.file_btn.clicked.connect(partial(self.slot_fs.import_file, self))
        self.ui.folder_btn.clicked.connect(partial(self.slot_fs.import_folder, self))
        self.ui.save_all_btn.clicked.connect(partial(self.slot_fs.save_all, self))
        self.ui.setting_btn.clicked.connect(partial(self.slot_fs.open_setting, self))
        self.ui.help_btn.clicked.connect(partial(self.slot_fs.open_help, self))
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
        
        pass
        # self.QFile.triggered.connect(self.slot_fs.import_file_slot)
        # self.QFolder.triggered.connect(self.slot_fs.import_folder_slot)
        # self.QSave.triggered.connect(self.slot_fs.save_slot)
        # self.QQuit.triggered.connect(self.slot_fs.quit_slot)
        # self.predict.clicked.connect(self.slot_fs.predict_slot)
        # # self.update.clicked.connect(self.slot_fs.update_slot)
        # self.visual.clicked.connect(self.slot_fs.visual_slot)
        # self.isolate.clicked.connect(self.slot_fs.isolate_slot)
        # self.working_tree.doubleClicked.connect(self.slot_fs.get_file)
        # self.model_select.currentIndexChanged.connect((self.slot_fs.model_select_slot)) 
        
        