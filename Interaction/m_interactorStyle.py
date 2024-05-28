import vtk

class CustomInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self):
        self.left_button_down = False  # 记录鼠标左键状态
        self.AddObserver("LeftButtonPressEvent", self.on_left_button_down)
        self.AddObserver("LeftButtonReleaseEvent", self.on_left_button_up)
        self.AddObserver("MouseMoveEvent", self.on_mouse_move)

    def on_left_button_down(self, obj, event):
        self.left_button_down = True

    def on_left_button_up(self, obj, event):
        self.left_button_down = False

    def on_mouse_move(self, obj, event):
        # 禁止在按住鼠标左键时上下移动
        if self.left_button_down:
            return
        else:
            super().OnMouseMove()

# if __name__ == '__main__':
#     # 创建渲染器、图像数据等...
#     # ...

#     # 创建交互式窗口
#     renderWindowInteractor = vtk.vtkRenderWindowInteractor()

#     # 设置自定义的交互样式
#     style = CustomInteractorStyle()
#     renderWindowInteractor.SetInteractorStyle(style)

#     # 渲染窗口等操作...
#     # ...
#     renderWindowInteractor.Initialize()
#     renderWindowInteractor.Start()
