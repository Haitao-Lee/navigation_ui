import vtkmodules.all as vtk
import math
import numpy as np

def get_cylinder_polydata(center, direct, radius=5, length=10, resolution = 6):
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetHeight(length)
    cylinder.SetRadius(radius)
    cylinder.SetResolution(resolution)
    cylinder.Update()
    # 定义变换参数
    direct = direct / np.linalg.norm(direct)
    rotate_axis = np.cross([0, 1, 0], direct)
    angle = math.acos(direct[1]) * 180 / math.pi
    # 创建变换
    transform = vtk.vtkTransform()
    transform.Translate(center + np.array([0,0,0]))  # 举例：平移操作
    transform.RotateWXYZ(angle, rotate_axis[0], rotate_axis[1], rotate_axis[2])
    # 创建 vtkTransformPolyDataFilter，并应用变换
    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetInputConnection(cylinder.GetOutputPort())
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    # 获取应用变换后的 PolyData
    transformed_polydata = transform_filter.GetOutput()
    return transformed_polydata
    
    
def get_cylinder_actor(center, direct, radius=5, length=10, resolution = 6, color=[1,0,0], opacity=1):
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetHeight(length)
    cylinder.SetRadius(radius)
    cylinder.SetResolution(resolution)
    cylinder.Update()
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cylinder.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color[0], color[1], color[2])
    actor.GetProperty().SetOpacity(opacity)
    direct = direct/np.linalg.norm(direct)
    rotate_axis = np.cross([0, 1, 0], direct)
    angle = math.acos(direct[1])*180/math.pi
    actor.RotateWXYZ(angle, rotate_axis[0], rotate_axis[1], rotate_axis[2])
    actor.AddPosition(center)
    return actor