from PyQt5.QtCore import *
import numpy as np

def importImplant(path):
    implant_file = QFile(path)
    implants = None
    if implant_file.open(QFile.ReadOnly):
        # 创建 QTextStream 对象，关联文件
        stream = QTextStream(implant_file)
       # 读取数字
        line = stream.readLine()
        numOfitem = int(line) if line.isdigit() else None  # 转换为整数
        implants = []
        for i in range(numOfitem):
            # 读取数据
            firstpt = []
            secondpt = []
            color = []
            for _ in range(3):
                line = (stream.readLine()).split()
                firstpt.append(line[0])
                secondpt.append(line[1])
                color.append(line[2])
            line = stream.readLine().split()
            radius = line[0]
            # length = float(line[1])
            implants.append([firstpt, secondpt, radius, color])
        
        # 在这里可以使用读取到的数据进行相应的处理或存储
        implant_file.close()
    return implants