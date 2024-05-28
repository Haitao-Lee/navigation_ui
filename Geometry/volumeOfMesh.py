import vtk

def volumeOfMesh(polydata):
        massProperties = vtk.vtkMassProperties()
        massProperties.SetInputData(polydata)
        massProperties.Update()
        # 获取体积
        volume = massProperties.GetVolume()
        return volume