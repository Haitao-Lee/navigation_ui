import numpy as np
import vtk
import config

class landmark():
    def __init__(self, scalar, color=config.lm_color, optical=config.lm_optical ):
        self.scalar = scalar
        self.color = color
        self.optical = optical
        self.polydata = self.createSpherePolydata(scalar)
        self.actor = None
        
    @staticmethod
    def createSpherePolydata(center, r=config.lm_radius):
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter(center)
        sphereSource.SetRadius(r)
        return sphereSource.GetOutput()
        
    def setActors(self, actor):
        self.actor = actor
        
    def changeActorOptical(self):
        if self.actor is not None:
            self.actor.GetProperty().SetOptical(1-self.optical)
            
    def setColor(self, color):
        self.color = color
        if self.actor is not None:
            self.actor.GetProperty().SetColor(color)