# -*- coding:utf-8 -*-
# @author:Ye Zhoubing
# @datetime:2024/6/15 16:37
# @software: PyCharm

import os


def get_all_files(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


# 调用示例
path = 'E:\git\houdunren\chrome'
files = get_all_files(path)
print(files)