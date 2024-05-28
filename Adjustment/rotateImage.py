import vtk

def GetrotateImageMTX(axis, value=90):
    rotationTransform = vtk.vtkTransform()
    rotationTransform.PreMultiply()
    rotationTransform.Identity()
    rotationTransform.RotateWXYZ(value, axis[0], axis[1], axis[2])
    return rotationTransform

