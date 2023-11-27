import numpy as np
import vtk
import config

class dicom():
    def __init__(self, data, Name=None, Age=None, filePath=None, resolution=None):
        self.data = data
        self.name = Name
        self.age = Age
        self.path = filePath
        self.resolution = resolution
        self.actor = None
        
    def setActor(self, actor):
        self.actor = actor
            
            
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
    
    def getName(self):
        return self.name
    
    def getPath(self):
        return self.path