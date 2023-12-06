import numpy as np
import vtk
import config
from vtk.util import numpy_support

class dicom():
    def __init__(self, arrayData,  imageData, Name=None, Age=None, filePath=None, resolution=None):
        self.arrayData = arrayData
        self.imageData = imageData
        self.name = Name
        self.age = Age
        self.path = filePath
        self.resolution = resolution
        self.actors = None
        self.imageReslices = None
    
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
    
    def createActors(self, LUT2D, CTF3D, PWF3D):
        # 创建图像 actor, 分别为axial、体绘制、sagittal和0cornal 的actor/volume
        # 2D
        # 创建三个切片器，分别用于三个方向的切片
        axisMtx = [config.axialMtx, config.sagittalMtx, config.cornalMtx]
        origin = np.array(self.imageData.GetOrigin())
        spacing = np.array(self.imageData.GetSpacing())
        extent = np.array(self.imageData.GetExtent())
        scale = np.array([extent[0] + extent[1] ,extent[2] + extent[3] , extent[4] + extent[5]])
        center = origin + 0.5*spacing*scale
        resliceAxes = []
        reslices = []
        colormaps = []
        self.actors = []
        for i in range(3):
            resliceAxes.append(vtk.vtkMatrix4x4())
            resliceAxes[i].DeepCopy(axisMtx[i])
            resliceAxes[i].SetElement(0, 3, center[0])
            resliceAxes[i].SetElement(1, 3, center[1])
            resliceAxes[i].SetElement(2, 3, center[2])
            reslices.append(vtk.vtkImageReslice())
            reslices[i].SetInputData(self.imageData)
            reslices[i].SetOutputDimensionality(2)
            reslices[i].SetResliceAxes(resliceAxes[i])
            reslices[i].SetInterpolationModeToCubic()
            colormaps.append(vtk.vtkImageMapToColors())
            colormaps[i].SetLookupTable(LUT2D)
            colormaps[i].SetInputConnection(reslices[i].GetOutputPort())
            colormaps[i].Update()
            self.actors.append(vtk.vtkImageActor())
            self.actors[i].GetMapper().SetInputConnection(colormaps[i].GetOutputPort())
        # 3D
        # 创建VTKVolumeMapper
        volume_mapper = vtk.vtkSmartVolumeMapper()
        volume_mapper.SetBlendModeToComposite()  # 使用复合模式混合
        volume_mapper.SetInputData(self.imageData)
        # 创建VTKVolumeProperty
        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetInterpolationTypeToLinear() # 设置线性插值
        volume_property.ShadeOn() # 开启阴影功能
        volume_property.SetAmbient(0.4) # 设置环境温度系数
        volume_property.SetDiffuse(0.6) # 设置漫反射系数
        volume_property.SetSpecular(0.2) # 设置镜面反射系数
        volume_property.SetColor(CTF3D)
        volume_property.SetScalarOpacity(PWF3D)
        # 创建VTKVolume
        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)
        self.actors.insert(1, volume)
    
    # def createActors(self, LUT2D, CTF3D, PWF3D):
    #     # 创建图像 actor, 分别为axial、体绘制、sagittal和0cornal 的actor/volume
    #     self.actors = [] # 清空原有actors
    #     # 2D
    #     self.imageReslices = []
    #     for _ in range(3): 
    #         self.actors.append(vtk.vtkImageActor())
    #         self.actors[-1].GetMapper().SetLookupTable(LUT2D)
    #     self.actors[0].SetInputData(self.arrayData[self.arrayData.shape[0] // 2, :, :])   
    #     self.actors[1].SetInputData(self.arrayData[:, self.arrayData.shape[0] // 2, :])  
    #     self.actors[2].SetInputData(self.arrayData[:, :, self.arrayData.shape[0] // 2]) 
    #     # 3D
    #     # 创建VTKVolumeMapper
    #     volume_mapper = vtk.vtkSmartVolumeMapper()
    #     volume_mapper.SetBlendModeToComposite()  # 使用复合模式混合
    #     volume_mapper.SetInputData(self.arrayData)
    #     # 创建VTKVolumeProperty
    #     volume_property = vtk.vtkVolumeProperty()
    #     volume_property.SetColor(CTF3D)
    #     volume_property.SetScalarOpacity(PWF3D)
    #     volume_property.ShadeOn()  # 启用阴影
    #     # 创建VTKVolume
    #     volume = vtk.vtkVolume()
    #     volume.SetMapper(volume_mapper)
    #     volume.SetProperty(volume_property)
    #     self.actors.append(volume)