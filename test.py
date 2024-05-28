# from PyQt5.QtCore import QThread, pyqtSignal

# class Worker(QThread):
#     finished = pyqtSignal()

#     def run(self):
#         # 在这里编写需要在后台线程执行的任务
#         for i in range(5):
#             print(f"Working... {i}")
#             self.sleep(1)  # 模拟耗时任务
#         self.finished.emit()  # 发送任务完成的信号

# # 使用示例
# worker = Worker()
# worker.finished.connect(lambda: print("Task completed!"))  # 连接任务完成信号
# worker.start()  # 启动线程执行任务
import vtk

def create_axes_actor(axis_colors):
    """
    创建一个带有自定义颜色的坐标轴Actor。
    """
    axes = vtk.vtkAxesActor()
    
    # 分别设置X、Y、Z轴的颜色
    axes.GetXAxisShaftProperty().SetColor(axis_colors[0])
    axes.GetYAxisShaftProperty().SetColor(axis_colors[1])
    axes.GetZAxisShaftProperty().SetColor(axis_colors[2])
    
    # 设置轴箭头颜色（如果有需要的话，这通常与轴杆颜色相同）
    axes.GetXAxisTipProperty().SetColor(axis_colors[0])
    axes.GetYAxisTipProperty().SetColor(axis_colors[1])
    axes.GetZAxisTipProperty().SetColor(axis_colors[2])
    
    # 设置轴的长度
    axes.SetTotalLength(10, 10, 10)
    
    return axes

def main():
    # 创建渲染窗口、渲染器和交互器
    ren = vtk.vtkRenderer()
    ren_win = vtk.vtkRenderWindow()
    ren_win.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)
    
    # 创建一个简单的3D对象作为场景内容（例如，一个立方体）
    cube_source = vtk.vtkCubeSource()
    cube_mapper = vtk.vtkPolyDataMapper()
    cube_mapper.SetInputConnection(cube_source.GetOutputPort())
    cube_actor = vtk.vtkActor()
    cube_actor.SetMapper(cube_mapper)
    cube_actor.GetProperty().SetColor(0.8, 0.8, 0.8)  # 立方体颜色
    ren.AddActor(cube_actor)
    
    # 创建方向标记（坐标轴）
    axis_colors = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)  # RGB颜色：红绿蓝
    axes_actor = create_axes_actor(axis_colors)
    
    # 创建方向标记小部件并关联到交互器
    widget = vtk.vtkOrientationMarkerWidget()
    widget.SetOrientationMarker(axes_actor)
    widget.SetInteractor(iren)
    widget.SetEnabled(True)
    widget.InteractiveOff()  # 默认是InteractiveOn，如果希望静态显示，则设为InteractiveOff
    
    # 设置渲染窗口大小和背景颜色
    ren_win.SetSize(800, 600)
    ren.SetBackground(0.1, 0.2, 0.4)
    
    # 渲染并启动交互
    ren_win.Render()
    iren.Initialize()
    iren.Start()

if __name__ == "__main__":
    main()