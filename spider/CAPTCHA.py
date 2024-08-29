# -*- coding:utf-8 -*-
# @author:Ye Zhoubing
# @datetime:2024/7/1 19:16
# @software: PyCharm
# -*- coding: utf-8 -*-
# @Author: b01e
# @Time: 2023/8/9 17:19
# @File: dddd_ikun.py
# @Describe: from ddddocr 修改
# coding=utf-8
"""
注意一下使用版本的pillow
这个工程中使用的是pillow-9.5.0
针对的是：https://www.houdunren.com/login后盾人网站的登录验证码
todo：目前识别有些问题
"""
import ddddocr
import requests
import re


class RegularCalculation:
    __div = re.compile(r"(\d+\.?\d*/-\d+\.?\d*)|(\d+\.?\d*/\d+\.?\d*)")  # 查找除法运算

    __mul = re.compile(r"(\d+\.?\d*\*-\d+\.?\d*)|(\d+\.?\d*\*\d+\.?\d*)")  # 查找乘法运算

    __add = re.compile(r"(-?\d+\.?\d*\+-\d+\.?\d*)|(-?\d+\.?\d*\+\d+\.?\d*)")  # 查找加法运算

    __sub = re.compile(r"(-?\d+\.?\d*--\d+\.?\d*)|(-?\d+\.?\d*-\d+\.?\d*)")  # 查找减法运算

    def division(self, value):
        """计算除法"""
        exp = re.split(r'/', self.__div.search(value).group())  # 将除法表达式拆分成列表
        return value.replace(self.__div.search(value).group(), str(float(exp[0]) / float(exp[1])))  # 计算并用结果替换列表中表达式

    def multiplication(self, value):
        """计算乘法"""
        exp = re.split(r'\*', self.__mul.search(value).group())  # 将乘法表达式拆分成列表
        return value.replace(self.__mul.search(value).group(), str(float(exp[0]) * float(exp[1])))  # 计算并用结果替换列表中表达式

    def addition(self, value):
        """计算加法"""
        exp = re.split(r'\+', self.__add.search(value).group())  # 将加法表达式拆分成列表
        return value.replace(self.__add.search(value).group(), str(float(exp[0]) + float(exp[1])))  # 计算并用结果替换列表中表达式

    def subtraction(self, value):
        """计算减法"""
        exp = self.__sub.search(value).group()  # 去除减法表达式
        if exp.startswith('-'):  # 如果表达式形如：-2.2-1.2；需变换为：-（2.2+1.2）
            exp = exp.replace('-', '+')  # 将-号替换为+号；+2.2+1.2
            res = self.addition(exp).replace('+', '-')  # 调用Add运算，将返回值+3.4变为-3.4
        else:
            exp = re.split(r'-', exp)
            res = str(float(exp[0]) - float(exp[1]))
        return value.replace(self.__sub.search(value).group(), res)


class VerificationCode(object):

    def __init__(self,image):
        # 这里将验证码图片保存在本地test.png
        # head = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        # }
        #
        # res_img = requests.get('https://www.登录地址.com/', headers=head)
        # with open('test.png', 'wb') as f:
        #     f.write(res_img.content)
        self.image = image

    def verification_code(self):
        ocr = ddddocr.DdddOcr(show_ad=False)  # show_ad=False关闭广告
        res = ocr.classification(self.image)
        # print(res)
        try:
            if '+' in res:
                result = RegularCalculation().addition(res)
            elif '-' in res:
                result = RegularCalculation().subtraction(res)
            elif 'x' in res:  # 因为测试的验证码只有加号，识别出来的乘号是x其实也是＋
                # result = RegularCalculation().multiplication(res.replace('x', '*'))
                result = RegularCalculation().addition(res.replace('x', '+'))
            else:
                result = RegularCalculation().division(res)
        except Exception as e:
            result = '计算出错'
            print(e)
        print(result.split('.')[0])


