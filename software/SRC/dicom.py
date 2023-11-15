import numpy as np
import vtk
import config

class dicom():
    def __init__(self, data, Name=None, Age=None, filePath=None, SerialNum=None):
        self.data = data
        self.name = Name
        self.age = Age
        self.path = filePath
        self.SerialNum = SerialNum
        self.actor = None
        
    def setActor(self, actor):
        self.actor = actor
            
    def setActorOpacity(self, opacity):
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