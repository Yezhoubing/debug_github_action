# -*- coding:utf-8 -*-
# @author:Ye Zhoubing
# @datetime:2024/8/27 10:00
# @software: PyCharm
import os
print(os.path.abspath('.'))
cmd = "ls"
print(os.popen(cmd).read())
