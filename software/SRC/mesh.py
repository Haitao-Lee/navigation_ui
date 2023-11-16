import numpy as np
import vtk
import config

class mesh():
    def __init__(self, polydata, Name=None, filePath=None, visible=config.mesh_visible, opacity=config.mesh_opacity, color=config.mesh_colors[0]):
        self.polydata = polydata
        self.color = color
        self.visible = visible
        self.opacity = opacity
        self.name = Name
        self.path = filePath
        self.actor = self.createActor(self.polydata, self.color, self.opacity, self.visible)
        
    @staticmethod
    def createActor(polydata, color=(1, 1, 1), opacity=1, visible=1):   
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polydata)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOptical(opacity)
        actor.SetVisibility(visible) 
        return actor
        
    def setActor(self, actor):
        self.actor = actor
        self.actor.GetProperty().SetColor(self.color)
        self.actor.GetProperty().SetOpacity(self.opacity)
        self.actor.SetVisibility(self.visible)
        
    def changeVisible(self):
        self.visible = 1 - self.visible
        if self.actor is not None:
            self.actor.SetVisibility(self.visible)
    
    def setVisible(self, visible):
        assert visible==0 or visible == 1
        self.visible = visible
        if self.actor is not None:
            self.actor.SetVisibility(self.visible) 
            
    def setOpacity(self, opacity):
        if opacity > 1:
            opacity = 1
        if opacity < 0:
            opacity = 0
        self.opacity = opacity
        if self.actor:
            self.actor.GetProperty().SetOptical(self.opacity)
            self.actor.SetVisibility(self.visible) 
            
    def setColor(self, color):
        self.color = color
        if self.actor is not None:
            self.actor.GetProperty().SetColor(color)
            
    def setName(self, name):
        self.name = name
        
    def setFilePath(self, path):
        self.path = path
            
    def getPolydata(self):
        return self.polydata
    
    def getActor(self):
        return self.actor
    
    def getColor(self):
        return self.color
    
    def getOpacity(self):
        return self.opacity
    
    def getVisible(self):
        return self.visible
    
    def getName(self):
        return self.name
    
    def getPath(self):
        return self.path