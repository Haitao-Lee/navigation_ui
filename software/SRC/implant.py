import numpy as np
import vtk
import config
import math

class implants():
    def __init__(self, start, end, radius=config.ip_radius, color=config.ip_colors[0], visible=config.ip_visible, opacity = config.ip_opacity):
        self.start = start
        self.end = end
        direct = end - start
        self.length = np.linalg.norm(direct)
        self.direct = direct/self.length
        self.radius = radius
        self.color = color
        self.visible = visible
        self.opacity = opacity
        self.line_actor = self.createLineActor(self.start, self.direct, self.length)
        self.tube_polytdata = self.createTuberPolyData(self.start, self.end, self.radius)
        self.tube_actor = None
    
    @staticmethod
    def createLineActor(start, direct, length, dash_length=config.ip_dash_length, length_rate=config.ip_line_rate):
        dashed = vtk.vtkAppendPolyData()
        total_line_length = length_rate*length
        start = start - (total_line_length-length)*direct/2
        for i in range(total_line_length//dash_length):
            p1 = start
            p2 = start + 3*dash_length*direct/4
            line = vtk.vtkLineSource()
            line.SetPoint1(p1)
            line.SetPoint2(p2)
            line.Update()
            dashed.AddInputConnection(line.GetOutputPort())
            start = start + dash_length*direct/4
        dashed.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(dashed.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 0, 0)
        actor.GetProperty().SetLineWidth(0.5)
        return actor
    
    @staticmethod     
    def createTuberPolyData(start, end, radius, resolution=config.ip_cylinder_res):
        ls = vtk.ctkLineSource()
        ls.SetPoint1(start)
        ls.SetPoint2(end)
        ts = vtk.vtkTubeFilter()
        ts.SetInputConnection(ls.GetOutputPort())
        ts.SetRadius(radius)
        ts.SetNumberOfSides(resolution)
        ts.CappingOn()
        ts.Updata()
        return ts.GetOutput()
    
    @staticmethod  
    def createTuberActor(polydata, opacity=config.ip_opacity, visible=config.ip_visible, color=config.ip_colors[0]):
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(polydata.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOpacity(opacity)
        actor.GetProperty().SetVisibility(visible)
        return actor
            
    def setActor(self, actor):
        self.actor = actor
        
    def changeActorVisible(self):
        self.visible = 1 - self.visible
        if self.actor is not None:
            self.actor.SetVisibility(self.visible)  
            
    def setActorVisible(self, visible):
        assert visible==0 or visible == 1
        self.visible = visible
        if self.actor is not None:
            self.actor.SetVisibility(self.visible) 
            
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
            
    def getScalar(self):
        return self.scalar
            
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