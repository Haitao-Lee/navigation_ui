import vtk

def createAxesActor(colors=[[0,1,0],[0,0,1],[1,0,0]], length=1.5):
    # 创建vtkAxesActor实例
    axes_actor = vtk.vtkAxesActor()
    # 获取X、Y、Z轴的属性对象
    x_axis_prop = axes_actor.GetXAxisCaptionActor2D().GetCaptionTextProperty()
    y_axis_prop = axes_actor.GetYAxisCaptionActor2D().GetCaptionTextProperty()
    z_axis_prop = axes_actor.GetZAxisCaptionActor2D().GetCaptionTextProperty()
    
    
    # 获取X、Y、Z轴的箭头属性
    x_axis_shaft_prop = axes_actor.GetXAxisShaftProperty()
    y_axis_shaft_prop = axes_actor.GetYAxisShaftProperty()
    z_axis_shaft_prop = axes_actor.GetZAxisShaftProperty()
    
    x_axis_tip_prop = axes_actor.GetXAxisTipProperty()
    y_axis_tip_prop = axes_actor.GetYAxisTipProperty()
    z_axis_tip_prop = axes_actor.GetZAxisTipProperty()
    
    # 设置箭头和轴的颜色，这里使用RGB值，范围从0到1
    x_axis_shaft_prop.SetColor(colors[0])  # X轴轴杆为红色
    x_axis_tip_prop.SetColor(colors[0])  # X轴箭头也为红色
    
    y_axis_shaft_prop.SetColor(colors[1])  # Y轴轴杆为绿色
    y_axis_tip_prop.SetColor(colors[1])  # Y轴箭头也为绿色
    
    z_axis_shaft_prop.SetColor(colors[2])  # Z轴轴杆为蓝色
    z_axis_tip_prop.SetColor(colors[2]) 
    
    # 设置颜色，这里使用RGB值，范围从0到1
    x_axis_prop.SetColor(colors[0])  
    y_axis_prop.SetColor(colors[1])  
    z_axis_prop.SetColor(colors[2]) 
    axes_actor.SetTotalLength(length, length, length) 
    return axes_actor