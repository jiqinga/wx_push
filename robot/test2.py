#!/usr/bin/env python
# encoding: utf-8
"""
@Project ：pythonProject
@file: test2.py
@time: 2022/8/26 16:03
@Author: 寂情啊
@contact: 1758812645@qq.com
"""
import os

from werobot import WeRoBot

robot = WeRoBot(token='jinitaimei')
robot.config["APP_ID"] = "wx484d8f04d8eaa2ca"
robot.config["APP_SECRET"] = "14cf384b8621bf0ffb48115a98bc613e"

client = robot.client

# 微信测试号可用
client.create_menu({
    "button": [
        {
            "type": "click",
            "name": "天气",
            "key": "tianqi"
        },
        {
            "type": "click",
            "name": "歌手简介",
            "key": "V1001_TODAY_SINGER"
        },
        {
            "name": "菜单",
            "sub_button": [
                {
                    "type": "view",
                    "name": "搜索",
                    "url": "http://www.soso.com/"
                },
                {
                    "type": "view",
                    "name": "视频",
                    "url": "http://v.qq.com/"
                },
                {
                    "type": "view",
                    "name": "博客",
                    "url": "https://www.jiqinga.top/"
                }
            ]
        }
    ]})


@robot.key_click("V1001_TODAY_SINGER")
def music(message):
    return '你点击了“歌手简介”按钮'


@robot.key_click("tianqi")
def music(message):
    os.system("cd /root/wx/zaoan && /usr/bin/python3 /root/wx/zaoan/wx.py")
    return '推送完成'


@robot.text
def first(message, session):
    print(message.source)
    if 'first' in session:
        return message.content
    session['first'] = True
    return message.content


# print(client.match_custom_menu("o41va6SoDiOcOQKt5P2KmIhqF4SQ"))
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 8095
robot.run(server='tornado')
