# -*- codeing=utf-8 -*-
# @Time:2022/4/17 19:46
# @Author:Ye Zhoubing
# @File: WeChat_send.py
# @software:PyCharm
"""
    利用企业微信实现发送通知功能
"""
import requests
import json
import os



class SendWeixin:
    # 调用企业微信接口发送微信消息
    def __init__(self, subject, message):  # 消息主题和消息内容
        self.subject = subject
        self.message = message

    def get_token(self, corp_id, secret):  # 获取token
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(corp_id, secret)
        r = requests.get(url=url)
        token = r.json()['access_token']
        return token

    def send_message(self, userid, agent_id, token):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
        data = {
            "touser": userid,
            "msgtype": "news",
            "agentid": agent_id,
            "news": {
                "articles": [
                    {
                        "title": self.subject,
                        "description": self.message,
                        "url": "https://www.houdunren.com/login",
                        "picurl": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwallpaperm.cmcm.com%2Fa2fd5828c3872e333a2ce0e4461ca7f7.jpg&refer=http%3A%2F%2Fwallpaperm.cmcm.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1656226295&t=73ebe828c0b24710ee8c3f0fb9a5be4d",
                    }
                ]
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        r = requests.post(url=url, data=json.dumps(data), verify=False)

        print(r.json())

    def main(self,user_id):
        corp_id = "wwe5f31a2523bde178"  # 企业ID
        secret = os.environ['secret']  # 应用Secret
        userid = user_id # 接收消息的用户账号，支持发给多个用户
        agent_id = "1000002"  # 应用AgentId
        token = self.get_token(corp_id, secret)
        self.send_message(userid, agent_id, token)  # 发送文本消息




