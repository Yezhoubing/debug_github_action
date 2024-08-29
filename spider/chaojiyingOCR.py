# -*- coding:utf-8 -*-
# @author:Ye Zhoubing
# @datetime:2023/11/2 16:10
# @software: PyCharm
"""
超级鹰识别验证码(本地图片)
"""

from hashlib import md5
import requests


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password.encode('utf8')).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


# if __name__ == '__main__':
#
#     # 超级鹰的图片识别区
#     chaojiying = Chaojiying_Client('qzq2001', 'dcrwgkqzq2001', '954241')  # 用户中心>>软件ID 生成一个替换 96001
#
#     # 取出本地的图片，并读取
#     im = open(r'C:\Users\Lenovo\Desktop\下载.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
#
#     # 1902是超级鹰的价格模型，针对不同类型的图片验证码的价格编号
#     pic_str = chaojiying.PostPic(im, 6001)['pic_str']
#     print(pic_str)

