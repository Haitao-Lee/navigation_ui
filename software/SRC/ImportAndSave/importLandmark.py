import vtk

def importLandmark(path):
    reader = vtk.vtkOBJReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()