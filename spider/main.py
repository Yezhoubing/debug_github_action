# -*- codeing=utf-8 -*-
# @Time:2021/9/18 19:11
# @Author:Ye Zhoubing
# @File: main.py
# @software:PyCharm


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException #防止下面的NameError: name 'NoSuchElementException' is not defined
import time
from retrying import retry
import random
import os
# 当前绝对路径：/home/runner/work/health/health
import WeChat_send
import chaojiyingOCR
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import urllib3
urllib3.disable_warnings()  # 解决未启用证书报错的问题

from CAPTCHA import VerificationCode

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chromedriver = "/usr/bin/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver

# 获取环境中的设置的secret变量
# users = os.environ['user']
# passwords = os.environ['password']
# user_ids = os.environ['user_id']


user = '18714895919'
password = 'yzb20001123'
user_id = 'yezhoubing'

# 本地测试

url_login = 'https://www.houdunren.com/login'

# @retry(stop_max_attempt_number=3)
def Get_url(user,password,id):
    # driver = webdriver.Chrome() #原先的chrome_options已弃用
    driver = webdriver.Chrome(options=chrome_options, service=Service('E:\git\houdunren\chromedriver-win64\chromedriver-win64\chromedriver.exe')) #原先的chrome_options已弃用
    driver.get(url_login)
    time.sleep(3)
    # driver.maximize_window()  # 全屏，确保后续是一样的;对于无头浏览器无效

    driver.find_element(By.XPATH, '//*[@id="app"]/main/main/div/form/div/div[1]/div/div[1]/input[1]').send_keys(user)
    driver.find_element(By.XPATH, '//*[@id="app"]/main/main/div/form/div/div[1]/div/div[1]/input[2]').send_keys(password) #信息门户密码

    # # 输入验证码
    verify_img = driver.find_element(By.XPATH, '//*[@id="app"]/main/main/div/form/div/div[1]/div/div[1]/main/section/div/img')
    image = verify_img.screenshot_as_png
    verify_result = VerificationCode(image).verification_code()

    driver.find_element(By.XPATH,'//*[@id="app"]/main/main/div/form/div/div[1]/div/div[1]/main/section/input').send_keys(verify_result)

    # 先不用机器识别验证码
    time.sleep(20)
    # 点击登录
    driver.find_element(By.XPATH, '//*[@id="app"]/main/main/div/form/div/div[1]/div/button').click()
    time.sleep(5)

    # 先点更多功能，再点击签到打卡
    driver.find_element(By.XPATH, '/html/body/div[1]/main/main/main[1]/div/section[1]/main/div/a').click()  # todo：这里有时候也会找不到
    time.sleep(3)
    # 注意一下这里位置跟你窗口大小有关，会影响到xpath的位置
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[1]/div/ul/li[4]/a').click()  # todo：有问题的地方：到了点击签到打卡的地方就会出现问题
    time.sleep(3)

    # 输入签到内容及验证码,todo:2改为3
    driver.find_element(By.XPATH, '/html/body/div[1]/main/main/main[3]/main/div/div[1]/div/div[1]/div/input').send_keys('新的一天开始了')  # todo:这里有时候会找不到
    verify_img = driver.find_element(By.XPATH, '//*[@id="app"]/main/main/main[3]/main/div/div[1]/div/main/section/div/img')
    chaojiying = chaojiyingOCR.Chaojiying_Client('18355629027', '960902', '957768')
    verify_result = chaojiying.PostPic(verify_img.screenshot_as_png, 6001)['pic_str']
    driver.find_element(By.XPATH, '//*[@id="app"]/main/main/main[3]/main/div/div[1]/div/main/section/input').send_keys(verify_result)

    # 选择心情
    driver.find_element(By.XPATH, '//*[@id="app"]/main/main/main[3]/main/div/div[1]/div/div[3]/div[1]/img').click()

    # 点击开始签到
    driver.find_element(By.XPATH, '//*[@id="app"]/main/main/main[3]/main/div/div[2]/div/button').click() # 不知为何不能写绝对路径

    cont = "今日打卡成功"
    send_mail(cont, id)
    print(cont)
    driver.quit()
def main(user,password,id):
    try:
        Get_url(user,password,id)
    except Exception as e:
        print(e)
        e = "今日打卡失败，请手动进行一次打卡"
        send_mail(e,id)
        print(e)




# 企业微信发送信息
def send_mail(cont,id):
    subject = "打卡通知"
    try:
        send_weixin = WeChat_send.SendWeixin(subject, cont)
        send_weixin.main(id)
        print("信息发送成功")
    except Exception as e:
        print("信息发送失败")


if __name__ == '__main__':
    main(user, password, user_id)