# -*- encoding:utf-8 -*-
import json

import requests
from requests_toolbelt import MultipartEncoder


class qywx:
    corpid = 'ww8107c9a87314cd63'  # 步骤1-3中的企业id
    # 可配置多个机器人
    app_list = [
        (1000002, 'KqU37pYD1XtPC10KGce_ccCuhSBqInORXn0kJsxkZnc'),
        (10000002, 'KqU37pYD1XtPC10KGce_ccCuhSBqInORXn0kJsxkZnc')  # 此处将步骤1-2中的AgentId 和 Secret分别填入，多个应用逗号隔开
    ]

    def __init__(self, app_id):  # app_id 按app_list顺序编号
        self.agentid, self.corpsecret = qywx.app_list[app_id]

    # 上传临时文件素材接口，图片也可使用此接口，20M上限
    def post_file(self, filepath, filename):
        response = requests.get(
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}".format(
                corpid=qywx.corpid, corpsecret=self.corpsecret))
        data = json.loads(response.text)
        access_token = data['access_token']

        post_file_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file".format(
            access_token=access_token)

        m = MultipartEncoder(
            fields={'file': (filename, open(filepath + filename, 'rb'), 'multipart/form-data')},
        )

        r = requests.post(url=post_file_url, data=m, headers={'Content-Type': m.content_type})
        js = json.loads(r.text)
        print("upload " + js['errmsg'])
        if js['errmsg'] != 'ok':
            return None
        return js['media_id']

    # 向应用发送图片接口，_message为上传临时素材后返回的media_id
    def send_img(self, _message, useridlist=['name1|name2']):
        useridstr = "|".join(useridlist)
        response = requests.get(
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}".format(
                corpid=qywx.corpid, corpsecret=self.corpsecret))
        data = json.loads(response.text)
        access_token = data['access_token']

        json_dict = {
            "touser": useridstr,
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {
                "media_id": _message,
            },
            "safe": 0,
            "enable_id_trans": 1,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        json_str = json.dumps(json_dict)
        response_send = requests.post(
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}".format(
                access_token=access_token), data=json_str)
        print("send to " + useridstr + ' ' + json.loads(response_send.text)['errmsg'])
        return json.loads(response_send.text)['errmsg'] == 'ok'

    # 向应用发送文字消息接口，_message为字符串
    def send_text(self, _message, useridlist=['name1|name2']):
        useridstr = "|".join(useridlist)  # userid 在企业微信-通讯录-成员-账号
        response = requests.get(
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}".format(
                corpid=qywx.corpid, corpsecret=self.corpsecret))
        data = json.loads(response.text)
        access_token = data['access_token']
        json_dict = {
            "touser": useridstr,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": _message
            },
            "safe": 0,
            "enable_id_trans": 1,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        json_str = json.dumps(json_dict)
        response_send = requests.post(
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}".format(
                access_token=access_token), data=json_str)
        print("send to " + useridstr + ' ' + json.loads(response_send.text)['errmsg'])
        return json.loads(response_send.text)['errmsg'] == 'ok'


# 调用示例
if __name__ == '__main__':
    qy = qywx(0)

    # 发送文本消息
    qy.send_text('hello world', ['LiuMengLong'])

    # 发送图片消息, 需先上传至临时素材
    # media_id = qy.post_file('/root/', 'a.jpg')
    # qy.send_img(media_id, ['ZhangSan'])
