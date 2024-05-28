import configparser
import tempfile

# # 假定这是你提供的INI文件内容
# ini_content = """
# [General]
# FiducialPoints=144.22583690051266, 184.2465227519489, 11.767891003772498, 141.6009263052061, 182.15850376160165, -2.498702595109762, 156.07152977150812, 190.88830992415734, -20.64669604894047, 155.43448382479033, 199.55282704290178, -2.113520381121333
# probeDeviateMatrix=1, 0, 0, -0.7367, 0, 1, 0, -13.52, 0, 0, 1, -109.4, 0, 0, 0, 1
# TrackerHostName=P9-13960
# ErrorPoints=169.76871330013498, 198.04372329755094, 19.325445026035716
# """

# # 将字符串内容直接读取到configparser，无需写入临时文件
# config = configparser.ConfigParser()
# config.read_string(ini_content)

# # 打印或操作配置
# print("Fiducial Points:", config.get('General', 'FiducialPoints'))

# # 假设你想保存到的路径为
# target_file_path = 'path/to/your/desired/configfile.ini'

# # 将修改后的配置保存到指定路径
# with open(target_file_path, 'w') as configfile:
#     config.write(configfile)

# print(f"配置已保存至 '{target_file_path}'")

def saveSetting(content, file_name):
    # 将字符串内容直接读取到configparser，无需写入临时文件
    config = configparser.ConfigParser()
    config.read_string(content)
    # 将修改后的配置保存到指定路径
    with open(file_name, 'w') as configfile:
        config.write(configfile)

    