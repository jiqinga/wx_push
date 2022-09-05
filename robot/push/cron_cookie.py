import re

import requests
from send_msg import qywx
from w_cookie import read_jd_cookies

# https://qinglong.ukenn.top/  青龙api
# 获取token
url = "https://ql.jiqinga.top/open/auth/token"
headers = {
    "accept": "application/json"
}
params = {
    "client_id": "751a9ErD_EbN",
    "client_secret": "mTJDRZlGOc-jdc9ITkr--i6U"
}
headers2 = {
    "accept": "application/json",
    'Authorization': 'Bearer 6d6f19e3-4a42-41b3-a966-f53780dc3692',
}
res = requests.get(url, headers=headers, params=params)
res = res.json()
print(res["data"]["token"])
# 获取环境变量
url = "https://ql.jiqinga.top/open/envs"
res2 = requests.get(url=url, headers=headers2)
env_list = res2.json()
for i in env_list["data"]:
    if int(i['status']) != 0:
        try:
            pt_pin = re.search('pt_pin=.*;', i["value"]).group()
        except AttributeError:
            print(i["remarks"], i["value"], "不是京东cookie")
            continue
        # print("cookie失效", i["remarks"], pt_pin)
        cookies = read_jd_cookies()
        try:
            username = cookies[pt_pin]
        except KeyError:
            print("%s,暂未找到绑定关系" % pt_pin)
            continue
        qy = qywx(0)
        # 发送文本消息
        qy.send_text('%s,cookie失效' % pt_pin, [username])
