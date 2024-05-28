import numpy as np
import vtk
import config

class tool():
    def __init__(self, polydata, Name=None, filePath=None, matrix = config.to_matrix, opacity=config.to_opcaity, visible=config.to_visible, color=config.to_color):
        self.matrix = matrix
        self.name = Name
        self.color = color
        self.path = filePath
        self.opacity = opacity
        self.visible = visible
        self.polydata = polydata
        self.actor = self.createActor(self.polydata, self.opacity, self.visible, self.color)
    
    @staticmethod  
    def createActor(polydata, opacity=config.ip_opacity, visible=config.ip_visible, color=config.ip_colors[0]):
        if polydata:
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(polydata)
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(color)
            actor.GetProperty().SetOpacity(opacity)
            actor.SetVisibility(visible)
            return actor
        return None
       
    def changeVisible(self):
        self.visible = 1 - self.visible
        if self.actor is not None:
            self.actor.SetVisibility(self.visible)
    
    def setActor(self, actor):
        self.actor = actor
        self.actor.GetProperty().SetOptical(self.opacity)
        self.actor.SetVisibility(self.visible) 
            
    def setOpacity(self, opacity):
        if opacity > 1:
            opacity = 1
        if opacity < 0:
            opacity = 0
        self.opacity = opacity
        if self.actor:
            self.actor.GetProperty().SetOpacity(self.opacity)
            self.actor.SetVisibility(self.visible) 
            
    def setColor(self, color):
        self.color = color
        if self.actor is not None:
            self.actor.GetProperty().SetColor(color)
            
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
    
    def getMatrix(self):
        return self.matrix