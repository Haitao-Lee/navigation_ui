import numpy as np
import vtk
import config

class dicom():
    def __init__(self, arrayData, vtkImageData, Name=None, Age=None, filePath=None, resolution=None):
        self.arrayData = arrayData
        self.vtkImageData = vtkImageData
        self.name = Name
        self.age = Age
        self.path = filePath
        self.resolution = resolution
        self.actors = None
    
    def getArrayData(self):
        return self.arrayData
    
    def getImageData(self):
        return self.vtkImageData
    
    def getActors(self):
        return self.actors
    
    def getName(self):
        return self.name
    
    def getPath(self):
        return self.path
    
    def getAge(self):
        return self.age
    
    def getResolution(self):
        return self.resolution
    
    def createActors(self, LUT):
        pass
        