import numpy as np
import vtk
import config
import Visualization.createSphere as createSphere

class landmark():
    def __init__(self, scalar, color=config.lm_color, visible=config.lm_visible, opacity = config.lm_opacity, r=config.lm_radius):
        self.scalar = scalar
        self.r=r
        self.color = color
        self.visible = visible
        self.opacity = opacity
        self.polydata = createSphere.get_sphere_polydata(self.scalar, self.r)
        self.actor = createSphere.get_sphere_actor(self.polydata, self.color, self.opacity, self.visible)
        self.projectActors = []

        
    # @staticmethod
    # def createSpherePolydata(center, r):
    #     sphereSource = vtk.vtkSphereSource()
    #     sphereSource.SetCenter(center[0], center[1], center[2])
    #     sphereSource.SetRadius(r)
    #     sphereSource.SetThetaResolution(30)  # 设置球体纬线分辨率
    #     sphereSource.SetPhiResolution(30)  # 设置球体经线分辨率
    #     return sphereSource.GetOutput()
    
    # @staticmethod
    # def createActor(polydata, color=(1, 0, 0), opacity=1, visible=1):   
    #     mapper = vtk.vtkPolyDataMapper()
    #     mapper.SetInputData(polydata)
    #     actor = vtk.vtkActor()
    #     actor.SetMapper(mapper)
    #     actor.GetProperty().SetColor(color)
    #     actor.GetProperty().SetOpacity(opacity)
    #     actor.SetVisibility(visible) 
    #     return actor
    
    # @staticmethod
    # def createShereActor(center, r=config.lm_radius, color=(1, 0, 0), opacity=1, visible=1):   
    #     # 创建一个球体
    #     sphere = vtk.vtkSphereSource()
    #     sphere.SetRadius(r)  # 设置球体半径
    #     sphere.SetCenter(center[0], center[1], center[2])  # 设置球体中心位置
    #     sphere.SetThetaResolution(30)  # 设置球体纬线分辨率
    #     sphere.SetPhiResolution(30)  # 设置球体经线分辨率

    #     # 创建球体的映射器和 actor
    #     mapper = vtk.vtkPolyDataMapper()
    #     mapper.SetInputConnection(sphere.GetOutputPort())
    #     actor = vtk.vtkActor()
    #     actor.SetMapper(mapper)
    #     actor.GetProperty().SetColor(color)
    #     actor.GetProperty().SetOpacity(opacity)
    #     actor.SetVisibility(visible) 
    #     return actor
    
    def setScalar(self, scalar):
        self.scalar = scalar
        self.polydata = createSphere.get_sphere_polydata(self.scalar, self.r)
        self.actor = createSphere.get_sphere_actor(self.polydata, self.color, self.opacity, self.visible)
        
    def setActor(self, actor):
        self.actor = actor
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
            
    def setRadius(self, r):
        self.r = r
        self.polydata = createSphere.get_sphere_polydata(self.scalar, self.r)
        self.actor = createSphere.get_sphere_actor(self.polydata, self.color, self.opacity, self.visible)
        
    def getScalar(self):
        return self.scalar
    
    def getRadius(self):
        return self.r
            
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
    
    def refresh(self):
        self.actor.GetProperty().SetColor(self.color)
        self.actor.GetProperty().SetOpacity(self.opacity)
        for i in range(len(self.projectActors)):
            self.projectActors[i].GetProperty().SetColor(self.color)
            self.projectActors[i].GetProperty().SetOpacity(self.opacity)