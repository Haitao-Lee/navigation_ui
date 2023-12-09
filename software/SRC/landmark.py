import numpy as np
import vtk
import config

class landmark():
    def __init__(self, scalar, color=config.lm_color, visible=config.lm_visible, opacity = config.lm_opacity):
        self.scalar = scalar
        self.color = color
        self.visible = visible
        self.opacity = opacity
        self.polydata = self.createSpherePolydata(scalar)
        self.actor = self.createActor(self.polydata, self.color, self.opacity, self.visible)
        
    @staticmethod
    def createSpherePolydata(center, r=config.lm_radius):
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter(center[0], center[1], center[2])
        sphereSource.SetRadius(r)
        sphereSource.SetThetaResolution(30)  # 设置球体纬线分辨率
        sphereSource.SetPhiResolution(30)  # 设置球体经线分辨率
        return sphereSource.GetOutput()
    
    @staticmethod
    def createActor(polydata, color=(1, 0, 0), opacity=1, visible=1):   
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polydata)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOpacity(opacity)
        actor.SetVisibility(visible) 
        return actor
    
    @staticmethod
    def createShereActor(center, r=config.lm_radius, color=(1, 0, 0), opacity=1, visible=1):   
        # 创建一个球体
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(r)  # 设置球体半径
        sphere.SetCenter(center[0], center[1], center[2])  # 设置球体中心位置
        sphere.SetThetaResolution(30)  # 设置球体纬线分辨率
        sphere.SetPhiResolution(30)  # 设置球体经线分辨率

        # 创建球体的映射器和 actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOpacity(opacity)
        actor.SetVisibility(visible) 
        return actor
        
    def setActor(self, actor):
        self.actor = actor
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
            self.actor.GetProperty().SetOpacity(self.opacity)
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