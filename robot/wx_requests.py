import requests


# 根据收到的请求模拟微信向机器人或者傻妞发送消息
def wx_req(url, timestamp, signature, nonce, openid, data):
    params = {
        "timestamp": timestamp,
        "signature": signature,
        "nonce": nonce,
        "openid": openid
    }
    res = requests.post(url, params=params, data=data.encode("utf-8"))
    return res.text
