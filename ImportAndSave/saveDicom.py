import vtk
import numpy as np
import pydicom
from pydicom.dataset import FileDataset
import util

def vtk_image_data_to_numpy(vtk_image_data):
    """将vtkImageData转换为NumPy数组"""
    dims = list(vtk_image_data.GetDimensions())
    np_array = np.zeros(dims, dtype=np.uint8)
    vtk_array = vtk.numpy_support.vtk_to_numpy(vtk_image_data.GetPointData().GetScalars())
    np_array.flat = vtk_array
    return np_array

def save_vtk_image_data_as_dicom(vtk_image_data, output_path):
    """将vtkImageData保存为DICOM文件,使用其自身的spacing"""
    # 将vtkImageData转换为numpy数组
    image_data = vtk_image_data_to_numpy(vtk_image_data)
    
    # 获取spacing
    spacing = vtk_image_data.GetSpacing()
    
    # 使用pydicom创建DICOM文件
    save_as_dicom(image_data, output_path, pixel_spacing=spacing)

def save_as_dicom(image_data, output_path, pixel_spacing=(1.0, 1.0, 1.0)):
    """辅助函数,保存图像数据为DICOM"""
    # 构建DICOM文件结构,此处以CT为例
    ds = FileDataset(output_path, {}, file_meta={})
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # CT图像存储 SOP 类别标识符
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.FrameOfReferenceUID = pydicom.uid.generate_uid()
    ds.SeriesNumber = 1
    ds.InstanceNumber = 1
    ds.Rows, ds.Columns, _ = image_data.shape
    ds.PixelSpacing = pixel_spacing[:2]  # DICOM通常处理2D图像,所以只保留前两个值
    ds.SliceThickness = pixel_spacing[2] if len(pixel_spacing) > 2 else 1.0
    ds.PhotometricInterpretation = 'MONOCHROME2'
    ds.SamplesPerPixel = 1
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    
    # 将图像数据转换为二进制并赋值给PixelData
    image_data = image_data.astype(np.uint8)
    ds.PixelData = image_data.tobytes()
    
    # 保存DICOM文件
    ds.save_as(output_path)

# 示例使用
# 假设你已经有了一个vtkImageData实例,比如叫image_data_vtk
# save_vtk_image_data_as_dicom(image_data_vtk, 'output.dcm')


def saveDicom(dicom, file_path):
    # 获取DICOM文件的基本信息
    source = dicom.getPath()
    util.copy_tree(source, file_path)
