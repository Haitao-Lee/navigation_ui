import SimpleITK as sitk
import itk
import pydicom
import os
from PyQt5.QtCore import *


# '''之所以用2个库来读取dicom。是因为simpleITK和pydicom在当前版本下和numpy、vtk等都有兼容问题,单个无法满足要求，只能妥协点读取时间了'''
# def importDicom(path):
#     # 获取文件夹中的所有文件名
#     if not os.path.isdir(path):
#         return None, None
#     files = os.listdir(path)
#     # 用于存储DICOM文件的列表
#     dicom_files = []
#     # 遍历文件夹中的文件
#     for file_name in files:
#         file_path = os.path.join(path, file_name).replace("\\","/")
#         # 检查文件是否是DICOM格式
#         if os.path.isfile(file_path) and file_name.lower().endswith('.dcm'):
#             dicom_files.append(file_path)
#             QCoreApplication.processEvents() # 防止卡顿
#     # 读取DICOM文件
#     if len(dicom_files) == 0:
#         return None, None
#     dicom_data = [pydicom.dcmread(file) for file in dicom_files]
#     reader = sitk.ImageSeriesReader()
#     QCoreApplication.processEvents()
#     reader.SetFileNames(dicom_files)
#     # reader.LoadPrivateTagsOn()
#     QCoreApplication.processEvents()
#     image = reader.Execute()
#     QCoreApplication.processEvents()
#     return dicom_data, image


def importDicom(path):
    # 定义DICOM文件名序列
    file_names = itk.GDCMSeriesFileNames.New()
    file_names.SetDirectory(path)

    # 创建ImageSeriesReader
    reader_type = itk.Image[itk.SS, 3]
    reader = itk.ImageSeriesReader[reader_type].New()
    reader.SetFileNames(file_names.GetInputFileNames())
    reader.Update()
    return reader


# # 获取DICOM序列中的一些信息
    # for tag in dicom_data[0].dir():
    #     print(tag)
    # for data in dicom_data:
    #     print(f"Patient Name: {data.PatientName}")
    #     print(f"Study Description: {data.StudyDescription}")
    #     print(f"Series Description: {data.SeriesDescription}")
    #     print(f"Image Shape: {data.Rows} x {data.Columns}")
    #     print("-----------------------------")

# def importDicom(path):
#     reader = sitk.ImageSeriesReader()
#     dicom_names = reader.GetGDCMSeriesFileNames(path)
#     reader.SetFileNames(dicom_names)
#     image = reader.Execute()
#     # patient_name = image.GetMetaData("0010|0010") 
#     # image_array = sitk.GetArrayFromImage(image) # z, y, x
#     # origin = image.GetOrigin() # x, y, z
#     # spacing = image.GetSpacing()
#     return image

'''
# DICOM序列所在的文件夹路径
dicom_dir = '/path/to/your/dicom/folder/'

# 读取DICOM序列
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(dicom_dir)
reader.SetFileNames(dicom_names)
image = reader.Execute()

# 获取DICOM序列的元数据信息
dicom_tags = image.GetMetaDataKeys()

# 获取病人信息
patient_name = image.GetMetaData("0010|0010")  # 患者姓名
patient_id = image.GetMetaData("0010|0020")    # 患者ID
study_description = image.GetMetaData("0008|1030")  # 检查描述
study_date = image.GetMetaData("0008|0020")    # 检查日期

# 打印病人信息
print("Patient Name:", patient_name)
print("Patient ID:", patient_id)
print("Study Description:", study_description)
print("Study Date:", study_date)
 
"0010|0010"：患者姓名
"0010|0020"：患者 ID
"0008|1030"：检查描述
"0010|0040"：患者性别
"0010|1010"：患者年龄
"0008|0020"：检查日期
"0008|103e"：系列描述
"0018|0088"：扫描时间
"0018|0015"：扫描体部位
"0018|0050"：切片厚度
"0018|0060"：扫描模式
"0020|0011"：序列编号
"0020|0013"：扫描编号
"0028|0101"：比特数
"0028|0100"：位深度
"0028|0010"：行像素
"0028|0011"：列像素
'''