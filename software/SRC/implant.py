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
        self.visible = visible # 0:None, 1:tube, 2:tube and dash
        self.opacity = opacity
        self.tube_polytdata = self.createTuberPolyData(self.start, self.end, self.radius)
        self.tube_actor = self.createActor(self.tube_polytdata, self.opacity, self.visible, self.color)
        self.dash_polydata = self.createDashPolydata(self.start, self.direct, self.length)
        self.dash_actor = self.createDashActor(self.line_polydata)
    
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
    def createActor(polydata, opacity=config.ip_opacity, visible=config.ip_visible, color=config.ip_colors[0]):
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polydata)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOpacity(opacity)
        actor.SetVisibility(visible > 0)
        return actor
    
    @staticmethod
    def createDashPolydata(start, direct, length, dash_length=config.ip_dash_length, length_rate=config.ip_line_rate):
        dashed = vtk.vtkAppendPolyData()
        total_line_length = length_rate*length
        n_start = start - (total_line_length-length)*direct/2
        for _ in range(total_line_length//dash_length):
            p1 = n_start
            p2 = n_start + 3*dash_length*direct/4
            line = vtk.vtkLineSource()
            line.SetPoint1(p1)
            line.SetPoint2(p2)
            line.Update()
            dashed.AddInputConnection(line.GetOutputPort())
            n_start = n_start + dash_length*direct/4
        dashed.Update()
        return dashed.GetOutput()
    
    def createDashActor(self, polydata, color=[1,0,0], lineWidth=0.5):
        actor = self.createActor(polydata)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetLineWidth(lineWidth)
        actor.SetVisibility(self.visible == 2)
        return actor
         
    def setTubeActor(self, actor):
        self.tube_actor = actor
        self.tube_actor.GetProperty().SetColor(self.color)
        self.tube_actor.GetProperty().SetOpacity(self.opacity)
        self.tube_actor.SetVisibility(self.visible > 0)
        
    def setDashActor(self, actor):
        self.dash_actor = actor
        self.dash_actor.SetVisibility(self.visible == 2)
        
    def changeVisible(self):
        self.visible = (self.visible + 1)//3
        if self.tube_actor:
            self.tube_actor.SetVisibility(self.visible > 0)
        if self.dash_actor:
            self.dash_actor.SetVisibility(self.visible == 2)
            
    def setVisible(self, visible):
        assert visible==0 or visible == 1 or visible == 2
        self.visible = visible
        if self.tube_actor:
            self.tube_actor.SetVisibility(self.visible > 0)
        if self.dash_actor:
            self.dash_actor.SetVisibility(self.visible == 2)
            
    def setOpacity(self, opacity):
        if opacity > 1:
            opacity = 1
        if opacity < 0:
            opacity = 0
        self.opacity = opacity
        if self.tube_actor:
            self.tube_actor.GetProperty().SetOptical(self.opacity)
            self.tube_actor.SetVisibility(self.visible>0) 
            
    def setColor(self, color):
        self.color = color
        if self.tube_actor is not None:
            self.tube_actor.GetProperty().SetColor(color)
            
    def getStart(self):
        return self.start
    
    def getEnd(self):
        return self.end
    
    def getDirect(self):
        return self.direct
    
    def getLength(self):
        return self.length
            
    def getTubePolydata(self):
        return self.tube_polytdata
    
    def getDashPolydata(self):
        return self.dash_polydata
    
    def getTubeActor(self):
        return self.tube_actor
    
    def getDashActor(self):
        return self.dash_actor
    
    def getColor(self):
        return self.color
    
    def getOpacity(self):
        return self.opacity
    
    def getVisible(self):
        return self.visible