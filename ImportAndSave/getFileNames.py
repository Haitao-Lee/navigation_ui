import os

def get_file_names(path, filetype):  # 输入路径、文件类型例如'.csv'
    names = []
    for _, _, files in os.walk(path):
        print(files)
        for i in files:
            if os.path.splitext(i)[1] == filetype:
                names.append(path + '/' + i)
    return names  # 输出由有后缀的文件名组成的列表