import vtk

def save_polydata_as_stl(polydata, filename):
    """
    将vtkPolyData对象保存为STL文件。
    
    参数:
    polydata: vtkPolyData对象,要保存的几何数据。
    filename: str,输出STL文件的路径和名称。
    """
    # 创建一个STL writer
    writer = vtk.vtkSTLWriter()
    writer.SetInputData(polydata)  # 设置输入的PolyData
    writer.SetFileName(filename)   # 设置输出文件名    
    # 写入文件
    writer.Write()

# 示例：创建一个简单的立方体PolyData
# cubeSource = vtk.vtkCubeSource()
# cubeSource.Update()  # 更新源对象以生成输出数据

# 保存为STL文件
# save_polydata_as_stl(cubeSource.GetOutput(), "output.stl")