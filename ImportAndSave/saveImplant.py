import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

def save_content_to_txt(content, file_name):
    # 尝试写入文件
    try:
        with open(file_name, 'w') as file:
            file.writelines(content)
            return True
    except Exception as e:
        return False
