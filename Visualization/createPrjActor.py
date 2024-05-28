import vtk
import os
import sys
# 获取当前文件所在目录的父目录绝对路径
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
# 将父目录添加到sys.path中
sys.path.append(parent_dir)
# 现在可以正常导入上一级目录中的模块了
import config

def createPrjActor(mesh, cutter_center, view_center, normal, offset = config.lineActorZOffset):
    polyData = mesh.getPolydata()
    plane = vtk.vtkPlane()
    plane.SetOrigin(cutter_center)
    plane.SetNormal(normal)
    cutter = vtk.vtkCutter()
    cutter.SetCutFunction(plane)
    cutter.SetInputData(polyData)
    vtk_tf = vtk.vtkTransform()
    vtk_tf.PostMultiply()
    if normal[0]:
        vtk_tf.Translate(-cutter_center[0], -cutter_center[1], -cutter_center[2])
        vtk_tf.RotateY(90)
        vtk_tf.RotateZ(-90)
        vtk_tf.Scale(1, -1, 1)
        vtk_tf.Translate(cutter_center[1] - view_center[1], cutter_center[2] - view_center[2], offset)
    elif normal[1]:
        vtk_tf.Translate(-cutter_center[0], -cutter_center[1], -cutter_center[2])
        vtk_tf.RotateX(90)
        vtk_tf.Scale(1, -1, 1)
        vtk_tf.Translate(cutter_center[0] - view_center[0], cutter_center[2] - view_center[2], offset)
    else:
        vtk_tf.Translate(-cutter_center[0], -cutter_center[1], -cutter_center[2])
        vtk_tf.Scale(-1, 1, 1)
        vtk_tf.Translate(view_center[0] - cutter_center[0], cutter_center[1] - view_center[1], offset)
    vtk_tf_filtter = vtk.vtkTransformPolyDataFilter()
    vtk_tf_filtter.SetInputConnection(cutter.GetOutputPort())
    vtk_tf_filtter.SetTransform(vtk_tf)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(vtk_tf_filtter.GetOutputPort())
    actor = vtk.vtkActor()
    actor.GetProperty().SetLineWidth(4)
    actor.SetMapper(mapper)
    actor.Modified()
    return actor


def createPrjActors(mesh, cutter_center, view_center):
    normals = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # consistent with the order of views
    prj_actors = []
    for i in range(3):
        prj_actor = createPrjActor(mesh, cutter_center, view_center, normals[i])
        prj_actors.append(prj_actor)
    return prj_actors