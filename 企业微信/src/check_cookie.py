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

res = requests.get(url, headers=headers, params=params)
res = res.json()
print(res["data"]["token"])
headers2 = {
	"accept": "application/json",
	'Authorization': f'Bearer {res["data"]["token"]}',
}
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
			for user in cookies:
				if pt_pin in cookies[user]:
					
					qy = qywx(0)
					# 发送文本消息
					qy.send_text('%s,cookie失效' % pt_pin, [user])
				else:
					print("没有要发送cookie失效的用户")
					continue
		except KeyError:
			print("%s,暂未找到绑定关系" % pt_pin)
			continue
