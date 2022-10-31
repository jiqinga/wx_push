import re

from send_msg import qywx
from updata_cookie import show_jd
from w_cookie import read_jd_cookies

cookie = read_jd_cookies()
for user in cookie:
	for i, v in cookie[user].items():
		res = show_jd(v)
		if "可以兑换了" in res:
			res = re.search('【东东农场】\S+\s\S+', res).group()
			qy = qywx(0)
			# 发送文本消息
			qy.send_text(res, [user])
