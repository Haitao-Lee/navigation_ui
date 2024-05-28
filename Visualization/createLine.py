import vtk


def get_line_polydata(start, end):
    line_source = vtk.vtkLineSource()
    line_source.SetPoint1(start[0], start[1], start[2])  # 设置直线起点坐标
    line_source.SetPoint2(end[0], end[1], end[2])  # 设置直线终点坐标 
    line_source.Update() 
    return line_source.GetOutput()

def get_line_actor(start, end, color=[1,0,0], linewidth=2):
    # 创建直线的 mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(get_line_polydata(start, end))
    # 创建直线的 actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # 设置直线的属性
    line_property = actor.GetProperty()
    line_property.SetLineWidth(linewidth) 
    line_property.SetColor(color)
    return actor 