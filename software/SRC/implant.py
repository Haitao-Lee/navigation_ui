import numpy as np
import vtk
import config

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
        self.cylinder_actor = None
    
    @staticmethod
    def createLineActor(start, direct, length, dash_length=config.ip_dash_length, length_rate=config.ip_line_rate):
        dashed = vtk.vtkAppendPolyData()
        total_line_length = length_rate*length
        start = start - (total_line_length-length)*direct/2
        for i in range(total_line_length//dash_length):
            p1 = start
            p2 = start + 3/8*dash_length*direct
            line = vtk.vtkLineSource()
            line.SetPoint1(p1)
            line.SetPoint2(p2)
            line.Update()
            dashed.AddInputConnection(line.GetOutputPort())
            start = start + 0.5*dash_length*direct
        dashed.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(dashed.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 0, 0)
        actor.GetProperty().SetLineWidth(0.5)
        return actor
        
    @staticmethod  
    def createCylinderActor(center, direct, radius, length, color=[1, 1, 1]):
        cylinder = vtk.vtkCylinderSource()
        length = length1 + length2
        cylinder.SetHeight(length)
        cylinder.SetRadius(0.7*radius)
        cylinder.SetResolution(6)
        cylinder.Update()
        
        head_cylinder = vtk.vtkCylinderSource()
        head_cylinder.SetHeight(4)
        head_cylinder.SetRadius(1.5*radius)
        head_cylinder.SetResolution(6)
        head_cylinder.Update()
        
        tf = vtk.vtkTransform()
        tf.Translate(0, length/2-2, 0)
        tf.Update()
        
        tf_pf = vtk.vtkTransformPolyDataFilter()
        tf_pf.SetInputData(head_cylinder.GetOutput())
        tf_pf.SetTransform(tf)
        tf_pf.Update()
        
        screw = vtk.vtkAppendPolyData()
        screw.AddInputData(cylinder.GetOutput())
        screw.AddInputData(tf_pf.GetOutput())
        
        for i in range(round(length)):
            thread_cylinder = vtk.vtkCylinderSource()
            thread_cylinder.SetHeight(0.5)
            thread_cylinder.SetRadius(radius)
            thread_cylinder.SetResolution(6)
            thread_cylinder.Update()
            thread_tf = vtk.vtkTransform()
            thread_tf.Translate(0, -length/2 + i, 0)
            thread_tf.Update()
            
            thread_tf_pf = vtk.vtkTransformPolyDataFilter()
            thread_tf_pf.SetInputData(thread_cylinder.GetOutput())
            thread_tf_pf.SetTransform(thread_tf)
            thread_tf_pf.Update()
            
            screw.AddInputData(thread_tf_pf.GetOutput())
            
        screw.Update()
        direct = direct/np.linalg.norm(direct)
        rotate_axis = np.cross([0, -1, 0], direct)
        angle = math.acos(-direct[1])*180/math.pi
        
        tf = vtk.vtkTransform()
        tf.PostMultiply()
        tf.RotateWXYZ(angle, rotate_axis[0], rotate_axis[1], rotate_axis[2])
        tf.Translate((length1 - length/2)*direct + center)
        tf.Update()
        
        tf_polydata = vtk.vtkTransformPolyDataFilter()
        tf_polydata.SetTransform(tf)
        tf_polydata.SetInputConnection(screw.GetOutputPort())
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(tf_polydata.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.4, 0.4, 0.4)
        return actor, tf_polydata
            
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