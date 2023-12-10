import vtk

# 创建一个 vtkRenderer
renderer = vtk.vtkRenderer()

# 创建一个 vtkRenderWindow 和 vtkRenderWindowInteractor
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# 创建一个 vtkAxesActor
axes_actor = vtk.vtkAxesActor()

# 设置 vtkOrientationMarkerWidget
widget = vtk.vtkOrientationMarkerWidget()
widget.SetOrientationMarker(axes_actor)
widget.SetInteractor(interactor)
widget.SetViewport(0.0, 0.0, 0.2, 0.2)
widget.SetEnabled(1)
widget.InteractiveOn()

# 渲染和交互开始
render_window.Render()
interactor.Start()