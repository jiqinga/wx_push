# -*- encoding:utf-8 -*-
import _thread
import os
import re
import sys
import time
from xml.dom.minidom import parseString

from flask import Flask
from flask import request

import send_msg
from check_cookies import checkCookies
from updata_cookie import run, show_jd
from w_cookie import write_jd_cookies, read_jd_cookies

sys.path.append("weworkapi/callback")
from WXBizMsgCrypt3 import WXBizMsgCrypt  # 库地址 https://github.com/sbzhu/weworkapi_python

app = Flask(__name__)


def jd_key(message, username, f):
    try:
        # 判断是否为京东cookie
        ptkey = re.search('pt_pin=.*;', message).group()
        print(ptkey)
    except AttributeError:
        print("未匹配到京东cookie")
        ptkey = ""
    print(message)
    # 如果ptkey有值则代表用户发送的是京东cookie
    if ptkey:
        # 如果返回值为1则代表cookie有效
        if 1 == int(checkCookies([message])[0]):
            # 传入pt_key以及完整cookie
            status = run(ptkey, message, username)
            print(ptkey, message)
            if 0 == status:
                print("傻妞")
                write_jd_cookies(ptkey, username, message)
                f.write(time.strftime('[%Y-%m-%d %H:%M:%S]') + "[cookie更新] [%s:%s]\n" % (username, message))
                return "绑定成功"
            else:
                return "未知错误"

        else:
            return "cookie无效"
    if message.strip() == "查询" or "8689":
        # 查看用户是否绑定cookie
        try:
            cookies = read_jd_cookies()
            pt_pins = cookies[username]
        except KeyError:
            return "未绑定cookie，直接发送cookie完成绑定"
        # 遍历用户cookie查询资产
        zichan = ""
        for pt_pin in pt_pins:
            # 传入用户的cookie
            zichan = zichan + show_jd(pt_pins[pt_pin]) + "\n"
        return zichan
    return "不是京东cookie，格式为 pt_key=xxxx; pt_pin=xxxx;"


# 对应步骤4中接受消息回调模式中的URL，如域名是'www.example.com' 那么在步骤4中填入的url就为"http://www.example.com/hook_path"
@app.route('/hook_path', methods=['GET', 'POST'])
def douban():
    if request.method == 'GET':
        echo_str = signature(request, 0)
        return (echo_str)
    elif request.method == 'POST':
        echo_str = signature2(request, 0)
        return (echo_str)


qy_api = [
    WXBizMsgCrypt("jinitaimei", "at5OtLgrU8YFv9UFTG1HThmnW8byNlzT3jIOpAYPyXb", "ww8107c9a87314cd63"),
]  # 对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id


# 开启消息接受模式时验证接口连通性
def signature(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret, sEchoStr = qy_api[i].VerifyURL(msg_signature, timestamp, nonce, echo_str)
    if (ret != 0):
        print("ERR: VerifyURL ret: " + str(ret))
        return ("failed")
    else:
        return (sEchoStr)


# 实际接受消息
def signature2(request, i):
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    data = request.data.decode('utf-8')
    ret, sMsg = qy_api[i].DecryptMsg(data, msg_signature, timestamp, nonce)
    if (ret != 0):
        print("ERR: DecryptMsg ret: " + str(ret))
        return ("failed")
    else:
        with open("/var/log/qywx.log", 'a+') as f:  # 消息接收日志
            doc = parseString(sMsg)
            collection = doc.documentElement
            name_xml = collection.getElementsByTagName("FromUserName")
            msg_xml = collection.getElementsByTagName("Content")
            event_msg_xml = collection.getElementsByTagName("EventKey")
            type_xml = collection.getElementsByTagName("MsgType")
            pic_xml = collection.getElementsByTagName("PicUrl")
            msg = ""
            name = ""
            msg_type = type_xml[0].childNodes[0].data
            print(msg_type)
            if msg_type == "text":  # 文本消息
                name = name_xml[0].childNodes[0].data  # 发送者id
                msg = str(msg_xml[0].childNodes[0].data)  # 发送的消息内容
                f.write(time.strftime('[%Y-%m-%d %H:%M:%S]') + "[ch%d] %s:%s\n" % (i, name, msg))
                # 写入用户和cookie绑定信息
                msg = jd_key(msg, name, f)
                print(i, name, msg)
                qy = send_msg.qywx(0)
                # 发送文本消息
                qy.send_text(msg, [name])
            # 用户进入小k聊天界面触发
            elif msg_type == "event":
                name = name_xml[0].childNodes[0].data
                try:
                    msg = str(event_msg_xml[0].childNodes[0].data)
                    f.write(time.strftime('[%Y-%m-%d %H:%M:%S]') + "[ch%d] %s点击%s菜单\n" % (i, name, msg))
                    print(name, msg)
                    msg = jd_key(msg, name, f)
                    qy = send_msg.qywx(0)
                    # 发送文本消息
                    qy.send_text(msg, [name])  # 发送的消息内容
                except IndexError:
                    f.write(
                        time.strftime('[%Y-%m-%d %H:%M:%S]') + "[ch%d] %s进入小k聊天框\n" % (i, name))  # 发送的消息内容# 发送者id
            elif msg_type == "image":  # 图片消息
                name = name_xml[0].childNodes[0].data
                pic_url = pic_xml[0].childNodes[0].data
                f.write(time.strftime('[%Y-%m-%d %H:%M:%S]') + "[ch%d] %s:图片消息\n" % (i, name))
                _thread.start_new_thread(os.system, (
                    "python3 command.py '%s' '%s' '%d' '%d'" % (name, pic_url, i, 1),))  # 此处将消息进行外部业务处理

            f.close()

        return ("ok")


if __name__ == '__main__':
    app.run("0.0.0.0", 80)  # 本地监听端口,可自定义
