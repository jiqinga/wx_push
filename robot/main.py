# coding=UTF-8
import re
from xml.etree import ElementTree

import web

from wx_requests import wx_req

urls = (
    '/wx/', 'Handle',
)


class Handle():
    def GET(self):
        print("get")

    def POST(self):
        dicta = web.input()
        wx_data = web.data().decode('utf-8')
        tree = ElementTree.fromstring(wx_data)
        message = tree.find("Content").text
        try:
            ptkey = re.match("(^pt_key=.*;|查询|菜单|资产推送|账号管理)", message).group()
            print(ptkey)
        except AttributeError:
            print("未匹配到京东cookie")
            ptkey = ""
        print(message)
        if ptkey:
            url = "https://sn.jiqinga.top/wx/"
            print("傻妞")
        else:
            url = "http://0.0.0.0:8095/wx/"
        # 模拟微信发送请求收到的返回结果
        wx_push = wx_req(url, dicta.timestamp, dicta.signature, dicta.nonce, dicta.openid,
                         wx_data)
        return wx_push


if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.run()
