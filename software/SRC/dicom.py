import numpy as np
import vtk
import config

class dicom():
    def __init__(self, arrayData,  imageData, Name=None, Age=None, filePath=None, resolution=None):
        self.arrayData = arrayData
        self.imageData = imageData
        self.name = Name
        self.age = Age
        self.path = filePath
        self.resolution = resolution
        self.actors = None
    
    def getArrayData(self):
        return self.arrayData
    
    def getImageData(self):
        return self.imageData
    
    def getActors(self):
        return self.actors
    
    def getName(self):
        return self.name
    
    def getPath(self):
        return self.path
    
    def getAge(self):
        return self.age
    
    def getResolution(self):
        return self.resolution
    
    def createActors(self, LUT2D, CTF3D):
        # 创建图像 actor, 分别为axial、sagittal、cornal和体绘制actor
        self.actors = [] # 清空原有actors
        # 2D
        for _ in range(3): 
            self.actors.append(vtk.vtkImageActor())
            self.actors[-1].GetMapper().SetLookupTable(LUT2D)
        self.actors[0].SetInputData(self.arrayData[self.arrayData.shape[0] // 2, :, :])   
        self.actors[1].SetInputData(self.arrayData[:, self.arrayData.shape[0] // 2, :])  
        self.actors[2].SetInputData(self.arrayData[:, :, self.arrayData.shape[0] // 2]) 
        # 3D
        # 创建VTKVolumeMapper
        volume_mapper = vtk.vtkSmartVolumeMapper()
        volume_mapper.SetBlendModeToComposite()  # 使用复合模式混合
        volume_mapper.SetInputData(self.arrayData)
        # 创建VTKVolumeProperty
        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetColor(CTF3D)
        volume_property.ShadeOn()  # 启用阴影
        # 创建VTKVolume
        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)
        self.actors.append(volume)