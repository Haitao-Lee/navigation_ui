import numpy as np
import vtk
import config
from vtk.util import numpy_support
from PyQt5.QtCore import *
import copy
from functools import partial
from concurrent.futures import ThreadPoolExecutor


class dicom(QThread):
    def __init__(self, arrayData,  imageData, Name=None, Age=None, filePath=None, resolution=None):
        self.arrayData = arrayData
        self.imageData = imageData
        self.name = Name
        self.age = Age
        self.path = filePath
        self.resolution = resolution
        self.actors = None
        self.imageReslices = None
        self.cut_planes = []
        self.resliceMappers = []
        self.reslices = [] 
        self.imageSliceProperty = []
    
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
    
    def createActorsInThreads(self, LUT2D, CTF3D, PWF3D):
        # 创建图像 actor, 分别为axial、体绘制、sagittal和0cornal 的actor/volume
        # 2D
        # 创建三个切片器，分别用于三个方向的切片
        axisMtx = [config.axialMtx, config.sagittalMtx, config.cornalMtx]
        origin = np.array(self.imageData.GetOrigin())
        spacing = np.array(self.imageData.GetSpacing())
        extent = np.array(self.imageData.GetExtent())
        scale = np.array([extent[0] + extent[1], extent[2] + extent[3], extent[4] + extent[5]])
        center = origin + 0.5*spacing*scale
        resliceAxes = []
        self.reslices = []
        self.colormaps = []
        self.actors = []
        for i in range(3):
            resliceAxes.append(vtk.vtkMatrix4x4())
            resliceAxes[i].DeepCopy(axisMtx[i])
            resliceAxes[i].SetElement(0, 3, center[0])
            resliceAxes[i].SetElement(1, 3, center[1])
            resliceAxes[i].SetElement(2, 3, center[2])
            self.reslices.append(vtk.vtkImageReslice())
            self.reslices[i].SetInputData(self.imageData)
            self.reslices[i].SetOutputDimensionality(2)
            self.reslices[i].SetResliceAxes(resliceAxes[i])
            self.reslices[i].SetInterpolationModeToCubic()
            self.colormaps.append(vtk.vtkImageMapToColors())
            self.colormaps[i].SetLookupTable(LUT2D)
            self.colormaps[i].SetInputConnection(self.reslices[i].GetOutputPort())
            self.colormaps[i].Update()
            self.actors.append(vtk.vtkImageActor())
            self.actors[i].GetMapper().SetInputConnection(self.colormaps[i].GetOutputPort())
        # # 3D
        # # 创建VTKVolumeMapper
        volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper() # vtkGPUVolumeRayCastMapper() # vtkSmartVolumeMapper() #  vtkFixedPointVolumeRayCastMapper() #
        volume_mapper.SetInputData(self.imageData)
        volume_mapper.SetSampleDistance(volume_mapper.GetSampleDistance()/2);
        # volume_mapper.SetCropping(1)	
        # volume_mapper.SetCroppingRegionPlanes(self.imageData.GetBounds())
        # volume_mapper.SetCroppingRegionFlags(0x0002000)
        # 创建VTKVolumeProperty
        self.volume_property = vtk.vtkVolumeProperty()
        self.volume_property.SetInterpolationTypeToLinear() # 设置线性插值
        self.volume_property.ShadeOn() # 开启阴影功能
        self.volume_property.SetAmbient(0.4) # 设置环境温度系数
        self.volume_property.SetDiffuse(0.6) # 设置漫反射系数
        self.volume_property.SetSpecular(0.2) # 设置镜面反射系数
        self.volume_property.SetColor(CTF3D)
        self.volume_property.SetScalarOpacity(PWF3D)
        # 创建VTKVolume
        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(self.volume_property)
        self.actors.insert(1, volume)
    
    def createActors(self, LUT2D, CTF3D, PWF3D):
        with ThreadPoolExecutor() as executor:
            # 提交任务给线程池执行（带参数）
            executor.submit(self.createActorsInThreads, LUT2D, CTF3D, PWF3D)
        
        
    def adjustActors(self, current_center):
        # 创建图像 actor, 分别为axial、体绘制、sagittal和0cornal 的actor/volume
        # 2D
        # 创建三个切片器，分别用于三个方向的切片
        # origin = np.array(self.imageData.GetOrigin())
        # spacing = np.array(self.imageData.GetSpacing())
        # extent = np.array(self.imageData.GetExtent())
        # scale = np.array([extent[0] + extent[1], extent[2] + extent[3], extent[4] + extent[5]])
        # center = origin + 0.5*spacing*scale
        # tmp_center = [[center[0], center[1], current_center[0]], [current_center[1], center[1], center[2]],[center[0], current_center[2], center[2]]]
        for i in range(3):
            # 获取切片平面的原点
            obtained_origin = np.array(self.reslices[i].GetResliceAxesOrigin())
            new_origin = copy.deepcopy(obtained_origin) 
            new_origin[(i+2)%3] = current_center[i]
            self.reslices[i].SetResliceAxesOrigin(new_origin)
            
            
    # def createActors(self, LUT2D, CTF3D, PWF3D):
    #     # 创建图像 actor, 分别为axial、体绘制、sagittal和0cornal 的actor/volume
    #     # 2D
    #     # 创建三个切片器，分别用于三个方向的切片
    #     color_min, color_max = LUT2D.GetRange()
    #     origin = np.array(self.imageData.GetOrigin())
    #     spacing = np.array(self.imageData.GetSpacing())
    #     extent = np.array(self.imageData.GetExtent())
    #     scale = np.array([extent[0] + extent[1], extent[2] + extent[3], extent[4] + extent[5]])
    #     center = origin + 0.5*spacing*scale
    #     self.actors = []  # 清空
    #     self.cut_planes = []
    #     self.resliceMappers = []
    #     self.reslices = [] 
    #     self.imageSliceProperty = []
    #     colormaps = []
    #     for i in range(3):
    #         self.imageSliceProperty.append(vtk.vtkImageProperty())
    #         self.imageSliceProperty[i].SetColorLevel((color_min + color_max)/2)
    #         self.imageSliceProperty[i].SetColorWindow(color_max - color_min)
    #         self.imageSliceProperty[i].SetInterpolationTypeToLinear()
    #         self.cut_planes.append(vtk.vtkPlane())
    #         self.cut_planes[i].SetOrigin(center[0], center[1], center[2])
    #         self.cut_planes[i].SetNormal(config.sliceNormal[i][0], config.sliceNormal[i][1], config.sliceNormal[i][2])
    #         self.resliceMappers.append(vtk.vtkImageResliceMapper())
    #         self.resliceMappers[i].SetInputData(self.imageData)
    #         self.resliceMappers[i].SetSlicePlane(self.cut_planes[i])
    #         self.reslices.append(vtk.vtkImageSlice())
    #         self.reslices[i].SetMapper(self.resliceMappers[i])
    #         self.reslices[i].SetProperty(self.imageSliceProperty[i])
    #         self.reslices[i].SetInterpolationModeToLinear()
    #         colormaps[i].SetLookupTable(LUT2D)
    #         colormaps[i].SetInputConnection(self.reslices[i].GetOutputPort())
    #         colormaps[i].Update()
    #         self.actors.append(vtk.vtkImageActor())
    #         self.actors[i].GetMapper().SetInputConnection(colormaps[i].GetOutputPort())
    #     # # 3D
    #     # # 创建VTKVolumeMapper
    #     volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()
    #     volume_mapper.SetInputData(self.imageData)
    #     volume_property = vtk.vtkVolumeProperty()
    #     volume_property.SetInterpolationTypeToLinear() # 设置线性插值
    #     volume_property.ShadeOn() # 开启阴影功能
    #     volume_property.SetAmbient(0.4) # 设置环境温度系数
    #     volume_property.SetDiffuse(0.6) # 设置漫反射系数
    #     volume_property.SetSpecular(0.2) # 设置镜面反射系数
    #     volume_property.SetColor(CTF3D)
    #     volume_property.SetScalarOpacity(PWF3D)
    #     # 创建VTKVolume
    #     volume = vtk.vtkVolume()
    #     volume.SetMapper(volume_mapper)
    #     volume.SetProperty(volume_property)
    #     self.actors.insert(1, volume)
        
    # def createActors(self, LUT2D, CTF3D, PWF3D):
    #     # 创建图像 actor, 分别为axial、体绘制、sagittal和0cornal 的actor/volume
    #     # 2D
    #     # 创建三个切片器，分别用于三个方向的切片
    #     color_min, color_max = LUT2D.GetRange()
    #     origin = np.array(self.imageData.GetOrigin())
    #     spacing = np.array(self.imageData.GetSpacing())
    #     extent = np.array(self.imageData.GetExtent())
    #     scale = np.array([extent[0] + extent[1], extent[2] + extent[3], extent[4] + extent[5]])
    #     center = origin + 0.5*spacing*scale
    #     self.actors = []  # 清空
    #     self.cut_planes = []
    #     self.resliceMappers = []
    #     self.reslices = [] 
    #     self.imageSliceProperty = []
    #     colormaps = []
    #     for i in range(3):
    #         self.imageSliceProperty.append(vtk.vtkImageProperty())
    #         self.imageSliceProperty[i].SetColorLevel((color_min + color_max)/2)
    #         self.imageSliceProperty[i].SetColorWindow(color_max - color_min)
    #         self.imageSliceProperty[i].SetInterpolationTypeToLinear()
    #         self.cut_planes.append(vtk.vtkPlane())
    #         self.cut_planes[i].SetOrigin(center[0], center[1], center[2])
    #         self.cut_planes[i].SetNormal(config.sliceNormal[i][0], config.sliceNormal[i][1], config.sliceNormal[i][2])
    #         self.resliceMappers.append(vtk.vtkImageResliceMapper())
    #         self.resliceMappers[i].SetInputData(self.imageData)
    #         self.resliceMappers[i].SetSlicePlane(self.cut_planes[i])
    #         self.reslices.append(vtk.vtkImageReslice())
    #         self.reslices[i].SetMapper(self.resliceMappers[i])
    #         self.reslices[i].SetProperty(self.imageSliceProperty[i])
    #         self.reslices[i].SetInterpolationModeToLinear()
    #         colormaps[i].SetLookupTable(LUT2D)
    #         colormaps[i].SetInputConnection(self.reslices[i].GetOutputPort())
    #         colormaps[i].Update()
    #         self.actors.append(vtk.vtkImageActor())
    #         self.actors[i].GetMapper().SetInputConnection(colormaps[i].GetOutputPort())
    #     # # 3D
    #     # # 创建VTKVolumeMapper
    #     volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()
    #     volume_mapper.SetInputData(self.imageData)
    #     volume_property = vtk.vtkVolumeProperty()
    #     volume_property.SetInterpolationTypeToLinear() # 设置线性插值
    #     volume_property.ShadeOn() # 开启阴影功能
    #     volume_property.SetAmbient(0.4) # 设置环境温度系数
    #     volume_property.SetDiffuse(0.6) # 设置漫反射系数
    #     volume_property.SetSpecular(0.2) # 设置镜面反射系数
    #     volume_property.SetColor(CTF3D)
    #     volume_property.SetScalarOpacity(PWF3D)
    #     # 创建VTKVolume
    #     volume = vtk.vtkVolume()
    #     volume.SetMapper(volume_mapper)
    #     volume.SetProperty(volume_property)
    #     self.actors.insert(1, volume)
        
    # def adjustActors(self, current_center):
    #     for i in range(3):
    #         self.cut_planes[i].SetOrigin(current_center[0], current_center[1], current_center[2])
    
    # def run(self):
    #     # 创建图像 actor, 分别为axial、体绘制、sagittal和0cornal 的actor/volume
    #     # 2D
    #     # 创建三个切片器，分别用于三个方向的切片
    #     axisMtx = [config.axialMtx, config.sagittalMtx, config.cornalMtx]
    #     origin = np.array(self.imageData.GetOrigin())
    #     spacing = np.array(self.imageData.GetSpacing())
    #     extent = np.array(self.imageData.GetExtent())
    #     scale = np.array([extent[0] + extent[1], extent[2] + extent[3], extent[4] + extent[5]])
    #     center = origin + 0.5*spacing*scale
    #     resliceAxes = []
    #     self.reslices = []
    #     self.colormaps = []
    #     self.actors = []
    #     for i in range(3):
    #         resliceAxes.append(vtk.vtkMatrix4x4())
    #         resliceAxes[i].DeepCopy(axisMtx[i])
    #         resliceAxes[i].SetElement(0, 3, center[0])
    #         resliceAxes[i].SetElement(1, 3, center[1])
    #         resliceAxes[i].SetElement(2, 3, center[2])
    #         self.reslices.append(vtk.vtkImageReslice())
    #         self.reslices[i].SetInputData(self.imageData)
    #         self.reslices[i].SetOutputDimensionality(2)
    #         self.reslices[i].SetResliceAxes(resliceAxes[i])
    #         self.reslices[i].SetInterpolationModeToCubic()
    #         self.colormaps.append(vtk.vtkImageMapToColors())
    #         self.colormaps[i].SetInputConnection(self.reslices[i].GetOutputPort())
    #         self.colormaps[i].Update()
    #         self.actors.append(vtk.vtkImageActor())
    #         self.actors[i].GetMapper().SetInputConnection(self.colormaps[i].GetOutputPort())
    #     # # 3D
    #     # # 创建VTKVolumeMapper
    #     volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper() # vtkSmartVolumeMapper() # vtkGPUVolumeRayCastMapper() # vtkFixedPointVolumeRayCastMapper() #
    #     volume_mapper.SetInputData(self.imageData)
    #     volume_mapper.SetCropping(1)	
    #     volume_mapper.SetCroppingRegionPlanes(self.imageData.GetBounds())
    #     volume_mapper.SetCroppingRegionFlags(0x0002000)
    #     # 创建VTKVolumeProperty
    #     self.volume_property = vtk.vtkVolumeProperty()
    #     self.volume_property.SetInterpolationTypeToLinear() # 设置线性插值
    #     self.volume_property.ShadeOn() # 开启阴影功能
    #     self.volume_property.SetAmbient(0.4) # 设置环境温度系数
    #     self.volume_property.SetDiffuse(0.6) # 设置漫反射系数
    #     self.volume_property.SetSpecular(0.2) # 设置镜面反射系数
    #     # 创建VTKVolume
    #     volume = vtk.vtkVolume()
    #     volume.SetMapper(volume_mapper)
    #     volume.SetProperty(self.volume_property)
    #     self.actors.insert(1, volume)
        
    # def complete_setting(self, LUT2D, CTF3D, PWF3D):
    #     for i in range(3):
    #         self.colormaps[i].SetLookupTable(LUT2D)
    #     self.volume_property.SetColor(CTF3D)
    #     self.volume_property.SetScalarOpacity(PWF3D)
        
    # def createActors(self, LUT2D, CTF3D, PWF3D):
    #     self.finished.connect(partial(self.complete_setting, LUT2D, CTF3D, PWF3D))