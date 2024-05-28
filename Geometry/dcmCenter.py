import numpy as np
def getDCMCenter(vtk_img):
    dimensions = np.array(vtk_img.GetDimensions()) 
    spacing = np.array(vtk_img.GetSpacing())
    origin = np.array(vtk_img.GetOrigin())
    center_x = origin[0] + 0.5 * (dimensions[0]-1) * spacing[0]
    center_y = origin[1] + 0.5 * (dimensions[1]-1) * spacing[1]
    center_z = origin[2] + 0.5 * (dimensions[2]-1) * spacing[2]
    view_center = [center_x, center_y, center_z]
    return np.array(view_center)