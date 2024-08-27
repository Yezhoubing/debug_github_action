# -*- coding:utf-8 -*-
# @author:Ye Zhoubing
# @datetime:2023/11/30 14:30
# @software: PyCharm
"""
    该程序的功能为自动更新chromedriver驱动，将驱动下载至当前文件夹，并解压到当前文件夹。
    if _status == '200' and _url.endswith('chromedriver-win32.zip')在这里根据
你的系统选择驱动，如果是linux系统，选择chromedriver-linux64.zip，如果是win系统，选择
chromedriver_win64.zip或者chromedriver_win32.zip
"""
# todo:感觉是文件没有保存下来
import re
import shutil
import os
from zipfile import ZipFile
import requests
# region 自动更新chromedriver_win32驱动
print(os.getcwd())
def chromedriver_download(chrome_version):
    def download_114(_url, _headers, _chrome_ver_pre):
        try:
            res = requests.get(_url, headers=_headers)
        except requests.exceptions.RequestException as e:
            print(f'获取下载链接出错：', e)
            return None
        li_ver = re.findall("<CommonPrefixes><Prefix>(.*?)/</Prefix></CommonPrefixes>", res.text)[:-1]  # 获取所有版本号
        if li_ver:
            for www_drv_ver in reversed(li_ver):
                if _chrome_ver_pre in www_drv_ver:
                    new_zip_name = f'chromedriver_win32_{www_drv_ver}.zip'  # zip文件名
                    url_ = f'https://chromedriver.storage.googleapis.com/{www_drv_ver}/chromedriver_win32.zip'  # 构建下载地址
                    try:
                        content = requests.get(url_, headers=headers).content
                        with open(new_zip_name, 'wb') as f:
                            f.write(content)
                        print(f'驱动文件 {new_zip_name} 下载完成。')
                        return new_zip_name
                    except requests.exceptions.RequestException as e:
                        print(f'驱动文件 {new_zip_name} 下载出错：', e)
        else:
            print('获取下载链接失败。')
            return None

    def download_115(url, _headers, _chrome_ver_pre):
        try:
            res = requests.get(url, headers=_headers)
        except requests.exceptions.RequestException as e:
            print(f'获取下载链接出错：', e)
            return None
        li_url = re.findall('<code>(https://.*?)</code>', res.text)  # 获取所有url
        li_status = re.findall(r'<code>(\d{3})</code>', res.text)  # 获取所有状态码
        if li_url:
            for _url, _status in zip(reversed(li_url), reversed(li_status)):
                if _status == '200' and _url.endswith('chromedriver-linux64.zip'):  # chromedriver-linux64.zip，chromedriver-win32.zip，chromedriver-win64.zip；32位与64位都可以使用，不用纠结自己电脑是32位还是64位
                    www_drv_ver = _url.split('/')[-3]  # 版本号
                    old_zip_name = _url.split('/')[-1]  # zip文件名
                    new_zip_name = old_zip_name.replace('.zip', f'-{www_drv_ver}.zip')  # 修改后的zip文件名
                    if str(_chrome_ver_pre) in _url:  # 与浏览器版本号前1位相同，需要继续修改
                        try:
                            content = requests.get(_url, headers=_headers).content
                            with open(new_zip_name, 'wb') as f:
                                f.write(content)
                            print(f'驱动文件 {new_zip_name} 下载完成。')
                            return new_zip_name
                        except requests.exceptions.RequestException as e:
                            print(f'驱动文件 {new_zip_name} 下载出错：', e)
        else:
            print('获取下载链接失败。')
            return None

    def extract_zip(zip_n, ver_pre):  # 解压ZIP文件 zip文件名，大版本号
        if zip_n is not None:
            print(f'正在解压，请稍等……')
            if os.path.exists('chromedriver'):  # todo:这里反常的chromedriver不存在。
                os.remove('chromedriver')  # 驱动文件存在时，先删除
                print('原驱动文件 chromedriver删除完成。')
            zip_ext_folder = "-".join(zip_n.split("-", 2)[:2])
            zip_ext_full_name = f'{zip_ext_folder}/chromedriver' if int(ver_pre) == 115 else 'chromedriver'
            # 114和115版压缩包中文件结构不相同
            with ZipFile(zip_n) as file:  # 解压驱动压缩包
                file.extract(zip_ext_full_name, path=os.getcwd())  # 解压
            print('解压完成。')
            os.remove(zip_n)  # 删除压缩文件
            if int(ver_pre) == 115:  # 114版本以下没有临时文件
                os.rename(f"{zip_ext_full_name}", "chromedriver")  # 驱动文件移动到当前文件夹
                shutil.rmtree(f'{zip_ext_folder}')  # 删除临时解压文件夹
                print('临时文件清除完成。')

    def find_zip_name(zip_name_pre):  # 查找驱动压缩包完整名称，不含路径 因版本号末尾的数字不确定
        for file in os.listdir(os.getcwd()):  # 遍历当前文件夹下的所有文件，排除文件夹
            if not os.path.isdir(file):
                if zip_name_pre in file:
                    return file

    # 下载驱动并解压 自动判断浏览器版本 114及以前的版本和114以上的版本下载地址不相同，压缩包结构也不相同。
    # url_115是114版本以上，url_114是114版本以下
    url_115 = 'https://googlechromelabs.github.io/chrome-for-testing/'  # 119.0.6045.105/win32/chromedriver-win32.zip
    url_114 = 'https://chromedriver.storage.googleapis.com/?delimiter=/&prefix='
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/86.0.4240.198 Safari/537.36'}
    chrome_ver_pre_1 = int(chrome_version.split('.')[0])  # 浏览器版本号 前1位(第一个小数点前的数字，例如：122)
    chrome_ver_pre_3 = chrome_version.rsplit('.', 1)[0]  # 浏览器版本号 前3位（即3组数字，中间点分隔，例如：122.01.32）
    if os.path.exists('chromedriver'):  # 驱动文件存在，但是和浏览器版本不符
        loc_drv_ver = os.popen('google-chrome --version').read().strip().split(' ')[1]  # 获取本地驱动文件版本
        if str(chrome_ver_pre_1) not in loc_drv_ver:  # 浏览器版本号前1位和驱动文件版本前1位不相同
            print(f'当前google浏览器的版本号为：{chrome_version} ')
            zip_name = find_zip_name(chrome_ver_pre_3)
            if zip_name:  # 压缩包存在
                print(
                    f'驱动文件 chromedriver存在，版本号为：{loc_drv_ver} 与浏览器的版本号不符，但是找到文件 {zip_name}')
                if chrome_ver_pre_1 >= 115:
                    extract_zip(download_115(url_115, headers, chrome_ver_pre_3), 115)
                else:
                    extract_zip(download_114(url_114, headers, chrome_ver_pre_3), 114)
            else:  # 压缩包不存在
                print(f'驱动文件 chromedriver存在，版本号为：{loc_drv_ver} 与浏览器的版本号不符。\n正在下载，请稍等……')
                if chrome_ver_pre_1 >= 115:
                    extract_zip(download_115(url_115, headers, chrome_ver_pre_3), 115)
                else:
                    extract_zip(download_114(url_114, headers, chrome_ver_pre_3), 114)
    else:  # 驱动文件不存在
        zip_name = find_zip_name(chrome_ver_pre_3)
        if zip_name:  # 驱动压缩包存在
            print(f'当前google浏览器的版本号为：{chrome_version} ')
            print(f'驱动文件 chromedriver不存在，但是找到文件 {zip_name}。')
            if chrome_ver_pre_1 >= 115:
                extract_zip(download_115(url_115, headers, chrome_ver_pre_1), 115)
            else:
                extract_zip(download_114(url_114, headers, chrome_ver_pre_1), 114)
        else:  # 什么也没有
            print(f'当前google浏览器的版本号为：{chrome_version} ')
            print('驱动文件 chromedriver不存在。\n正在下载，请稍等……')
            if chrome_ver_pre_1 >= 115:  # 只要找前1位相同的版本号就行，比如：'122.0.6253.3'只要下载是122就开头的驱动即可
                extract_zip(download_115(url_115, headers, chrome_ver_pre_1), 115)
            else:
                extract_zip(download_114(url_114, headers, chrome_ver_pre_1), 114)





# 调用示例
cmd = "google-chrome --version"  # 获取chrome版本
chrome_version = os.popen(cmd).read().strip().split(" ")[-1]
chromedriver_download(chrome_version)  # 更新浏览器驱动