import os
import sys
# 获取当前文件所在目录的父目录绝对路径
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
# 将父目录添加到sys.path中
sys.path.append(parent_dir)
# 现在可以正常导入上一级
import util
def saveRom(rom, file_path):
    folder, fileName, file_extension = util.split_file_path(file_path)
    util.copy_and_rename(rom.getPath(), folder, fileName+file_extension)