import SimpleITK as sitk

def importDicom(path):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(path)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    # image_array = sitk.GetArrayFromImage(image) # z, y, x
    # origin = image.GetOrigin() # x, y, z
    # spacing = image.GetSpacing()
    return image

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