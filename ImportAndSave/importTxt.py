def importTxt(path):
    # 以只读模式打开文件
    with open(path, 'r', encoding='utf-8') as file:
        # 逐行读取文件的内容
        lines = file.readlines()
        return lines