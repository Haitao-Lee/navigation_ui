import numpy as np
import vtk
import config

class mesh():
    def __init__(self, polydata, Name=None, filePath=None, visible=config.mesh_visible, opacity=config.mesh_opacity, color=config.mesh_colors[0]):
        self.polydata = polydata
        self.color = np.array(color)
        self.visible = visible
        self.opacity = opacity
        self.name = Name
        self.path = filePath
        self.actor = self.createActor(self.polydata, self.color, self.opacity, self.visible)
        self.projectActors = []
        
    @staticmethod
    def createActor(polydata, color=(1, 1, 1), opacity=1, visible=1):   
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polydata)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOpacity(opacity)
        actor.GetProperty().ShadingOn()
        actor.SetVisibility(visible) 
        return actor
        
    def setActor(self, actor):
        self.actor = actor
        self.actor.GetProperty().SetColor(self.color)
        self.actor.GetProperty().SetOpacity(self.opacity)
        self.actor.SetVisibility(self.visible)
        
    def setPrjActors(self, actors):
        for actor in actors:
            actor.GetProperty().SetColor(self.color)
            actor.GetProperty().SetOpacity(self.opacity)
            actor.SetVisibility(self.visible)
            self.projectActors.append(actor)
        
    def setPrjActor(self, actor, num):
        actor.GetProperty().SetColor(self.color)
        actor.GetProperty().SetOpacity(self.opacity)
        actor.SetVisibility(self.visible)
        if num >=0 and num < len(self.projectActors):
            self.projectActors[num] = actor

    def changeVisible(self):
        self.visible = 1 - self.visible
        if self.actor is not None:
            self.actor.SetVisibility(self.visible)
        for i in range(len(self.projectActors)):
            self.projectActors[i].SetVisibility(self.visible)
    
    def setVisible(self, visible):
        assert visible==0 or visible == 1
        self.visible = visible
        if self.actor is not None:
            self.actor.SetVisibility(self.visible) 
        for i in range(len(self.projectActors)):
            self.projectActors[i].SetVisibility(self.visible)
            
    def setOpacity(self, opacity):
        if opacity > 1:
            opacity = 1
        if opacity < 0:
            opacity = 0
        self.opacity = opacity
        if self.actor:
            self.actor.GetProperty().SetOpacity(self.opacity)
            self.actor.SetVisibility(self.visible) 
        for i in range(len(self.projectActors)):
            self.projectActors[i].GetProperty().SetOpacity(self.opacity)
            self.projectActors[i].SetVisibility(self.visible)
             
    def setColor(self, color):
        self.color = color
        if self.actor is not None:
            self.actor.GetProperty().SetColor(color)
        for i in range(len(self.projectActors)):
            self.projectActors[i].GetProperty().SetColor(color)
            
    def setName(self, name):
        self.name = name
        
    def setFilePath(self, path):
        self.path = path
            
    def getPolydata(self):
        return self.polydata
    
    def getActor(self):
        return self.actor
    
    def getPrjActors(self):
        return self.projectActors
    
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
    
    def refresh(self):
        self.actor.GetProperty().SetColor(self.color)
        self.actor.GetProperty().SetOpacity(self.opacity)
        for i in range(len(self.projectActors)):
            self.projectActors[i].GetProperty().SetColor(self.color)
            self.projectActors[i].GetProperty().SetOpacity(self.opacity)