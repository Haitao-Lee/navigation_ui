import UI.ui_all as ui_all
import slot_functions
import config
from functools import partial

class system_manager():
    def __init__(self):
        super(system_manager, self).__init__()
        self.ui = ui_all.ui_all()
        self.slot_fs = slot_functions.slot_functions()
        #self.core = 
        self.setupConnections()       
        
    def setupConnections(self):
        self.ui.file_btn.clicked.connect(partial(self.slot_fs.import_file, self))
        self.ui.folder_btn.clicked.connect(partial(self.slot_fs.import_folder, self))
        self.ui.setting_btn.clicked.connect(partial(self.slot_fs.open_setting, self))
        self.ui.help_btn.clicked.connect(partial(self.slot_fs.open_help, self))
        # self.ui.adjust_btn.clicked.connect(partial(self.slot_fs.adjust, self))
        self.ui.connect_btn.clicked.connect(self.slot_fs.conect2ndi)
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
        
        