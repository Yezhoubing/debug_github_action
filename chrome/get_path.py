# -*- coding:utf-8 -*-
# @author:Ye Zhoubing
# @datetime:2024/8/27 10:00
# @software: PyCharm
import os
print(os.path.abspath('.'))
cmd = "ls"
print(os.popen(cmd).read())

# 测试一下写文件功能及保存路径
with open('data.txt', 'w') as f:
  f.write('hello world')  #文件的写操作
