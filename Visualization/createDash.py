import vtkmodules.all as vtk

def get_dash_actor(center, direct, length, length_rate=20):
    dashed = vtk.vtkAppendPolyData()
    start = center - 0.5*length_rate*length*direct
    for i in range(2*length_rate):
        p1 = start
        p2 = start + 3/8*length*direct
        line = vtk.vtkLineSource()
        line.SetPoint1(p1)
        line.SetPoint2(p2)
        line.Update()
        dashed.AddInputConnection(line.GetOutputPort())
        start = start + 0.5*length*direct
    dashed.Update()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(dashed.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 0, 0)
    actor.GetProperty().SetLineWidth(0.2)
    return actor