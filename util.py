from vtk import vtkActor, vtkRenderer, vtkRenderWindow


# 输入参数 str 需要判断的字符串
# 返回值   True：该字符串为浮点数；False：该字符串不是浮点数。
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def is_actor_in_renderer(actor, renderer):
    """
    检查给定的actor是否存在于renderer的actors列表中。
    
    参数:
    actor -- 要检查的vtkActor对象
    renderer -- vtkRenderer对象
    
    返回:
    如果actor在renderer中返回True, 否则返回False。
    """
    actors = renderer.GetActors()  # 获取渲染器中的vtkActor集合
    actors.InitTraversal()
    cur_actor = actors.GetNextItem()
    while cur_actor is not None:
        if cur_actor is actor:  # 检查当前actor是否是我们要查找的actor
            return True
        cur_actor = actors.GetNextItem()
    return False  # 如果遍历完所有actors都没找到，返回False

import shutil
import os

def copy_and_rename(src_file_path, dest_folder_path, new_file_name):
    """
    复制文件到指定文件夹并重命名。
    
    :param src_file_path: 源文件路径
    :param dest_folder_path: 目标文件夹路径
    :param new_file_name: 新的文件名（含扩展名）
    """
    try:
        # 确保目标文件夹存在
        if not os.path.exists(dest_folder_path):
            os.makedirs(dest_folder_path)
        
        # 构建目标文件的完整路径
        dest_file_path = os.path.join(dest_folder_path, new_file_name)
        
        # 使用shutil.copy()复制文件到目标文件夹并使用新名字
        shutil.copy(src_file_path, dest_file_path)
        
        # print(f"文件已成功复制并重命名为: {dest_file_path}")
    except IOError as e:
        print(f"复制文件时发生错误: {e.strerror}")
    except Exception as e:
        print(f"发生未知错误: {e}")

# # 示例使用
# source_file = 'path/to/source/file.txt'  # 源文件路径
# destination_folder = 'path/to/destination/folder'  # 目标文件夹路径
# new_name = 'new_file_name.txt'  # 新的文件名

# copy_and_rename(source_file, destination_folder, new_name)


import os

def split_file_path(file_path):
    # 分离路径的各个部分
    path_parts = os.path.split(file_path)
    
    # 获取目录路径
    directory = path_parts[0]
    
    # 获取文件名（带扩展名）
    file_name_with_extension = path_parts[1]
    
    # 分离文件名和扩展名
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    
    return directory, file_name, file_extension

# 示例
# file_path = "/home/user/documents/example.txt"
# directory, file_name, file_extension = split_file_path(file_path)

# print(f"目录: {directory}")
# print(f"文件名: {file_name}")
# print(f"文件类型: {file_extension}")



def copy_tree(src, dst):
    """
    复制源目录src到目标目录dst,包括所有子目录和文件。
    :param src: 源目录路径
    :param dst: 目标目录路径
    """
    try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
        # print(f"目录 '{src}' 已成功复制到 '{dst}'。")
    except FileNotFoundError:
        pass
        # print(f"源目录 '{src}' 未找到。")
    except PermissionError:
        pass
        # print(f"没有足够的权限复制到目录 '{dst}'。")
    except Exception as e:
        pass
        # print(f"复制过程中发生错误: {e}")

# # 使用示例
# source_dir = 'path/to/source_directory'  # 源目录路径
# destination_dir = 'path/to/destination_directory'  # 目标目录路径

# # 确保目标目录存在，如果不存在则创建
# if not os.path.exists(destination_dir):
#     os.makedirs(destination_dir)

# copy_tree(source_dir, destination_dir)