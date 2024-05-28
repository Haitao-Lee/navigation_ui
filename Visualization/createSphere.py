import vtkmodules.all as vtk

def get_sphere_polydata(center, radius=3):
    sphere = vtk.vtkSphereSource()
    sphere.SetCenter(center)
    sphere.SetRadius(radius)
    sphere.Update()
    return sphere.GetOutput()

def get_sphere_actor(polydata, color=(1, 0, 0), opacity=1, visible=1):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color[0], color[1], color[2])
    actor.GetProperty().SetOpacity(opacity)
    actor.SetVisibility(visible)
    return actor