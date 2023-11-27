from PyQt5.QtCore import *
import configparser

def importIni(path):
    # 创建 ConfigParser 对象
    settings = configparser.ConfigParser()
    # 读取 INI 文件
    settings.read(path)
    return settings