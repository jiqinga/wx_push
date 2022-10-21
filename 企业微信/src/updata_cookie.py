import re

import requests

from check_cookies import checkCookies


# https://qinglong.ukenn.top/  青龙api
# 获取青龙token
def get_ql_token():
	# 获取token
	"""

	:return:  返回青龙token
	"""
	url = "https://ql.jiqinga.top/open/auth/token"
	headers = {
		"accept": "application/json"
	}
	params = {
		"client_id": "751a9ErD_EbN",
		"client_secret": "mTJDRZlGOc-jdc9ITkr--i6U"
	}
	# 根据client_id以及client_secret获取青龙cookie
	res = requests.get(url, headers=headers, params=params).json()
	ql_token = res["data"]["token"]
	return ql_token


def add_jd_cookie(token, cookie, username):
	"""
	此函数用于在青龙新增cookie
	:param token:  青龙token
	:param cookie:   完整cookie
	:param username:  发送消息的微信用户
	:return:    环境变量id，名字，备注
	"""
	url = "https://ql.jiqinga.top/open/envs"
	data = '[{ "value": "%s", "name": "JD_COOKIE","remarks": "%s"}]' % (cookie, username)
	res = requests.post(url, headers=ql_headers(token), data=data.encode("utf-8")).json()
	# 如果状态码等于200，则表示成功，否则新增失败
	if res["code"] == 200:
		return res["data"][0]["id"], res["data"][0]["name"], res["data"][0]["remarks"]
	else:
		return "xx", "xx", "xx"


def ql_headers(token):
	headers2 = {
		"accept": "application/json",
		'Authorization': 'Bearer {}'.format(token),
		'Content-Type': 'application/json'
	}
	return headers2


# 获取id
def ql_cookie_id(jd_pt_pin, token, cookie, username):
	"""

	:param jd_pt_pin:    pt_pin 不是完整cookie
	:param token:        青龙访问token
	:return:   envs["id"], envs["name"], envs["remarks"] 返回变量id，名字，备注
	"""
	url = "https://ql.jiqinga.top/open/envs"
	res2 = requests.get(url=url, headers=ql_headers(token))
	env_list = res2.json()
	# print(env_list)
	# 对所有变量进行循环
	for envs in env_list["data"]:
		try:
			pt_pin = re.search('pt_pin=.*;', envs["value"]).group()
		except AttributeError:
			print(envs["remarks"], envs["value"], "不是京东cookie")
			continue
		# print("cookie失效", i["remarks"], pt_pin)
		if pt_pin == jd_pt_pin:
			return envs["id"], envs["name"], envs["remarks"]
	# 如果上面没匹配到，则cookie不在青龙中，则代表新增cookie
	return add_jd_cookie(token, cookie, username)


def enable_env_cookie(id, token):
	"""

	:param id:  青龙环境变量id
	:param token:  青龙token
	:return:
	"""
	url = "https://ql.jiqinga.top/open/envs/enable"
	data = '[{}]'.format(id)
	
	res = requests.put(url, headers=ql_headers(token), data=data)
	return res.status_code


def update_env_cookie(id, cookie_name, cookie_remarks, token, cookie):
	# 获取环境变量
	url = "https://ql.jiqinga.top/open/envs"
	data = {
		"value": cookie,
		"name": cookie_name,
		"remarks": cookie_remarks,
		"id": id,
		
	}
	res = requests.put(url, headers=ql_headers(token), json=data)
	print(res.text)
	if res.status_code == 200:
		enable_status = enable_env_cookie(id, token)
		if 200 == enable_status:
			return 0
	return 1


def run(pt_pin, cookie, username):
	"""

	:param pt_pin:    pt_pin
	:param cookie:   完整cookie
	:return:  0为成功 1为失败
	"""
	token = get_ql_token()
	id, cookie_name, cookie_remarks = ql_cookie_id(pt_pin, token, cookie, username)
	status = update_env_cookie(id, cookie_name, cookie_remarks, token, cookie)
	print(status)
	return status


def show_jd(cookie):
	url = "http://192.168.0.4:3100/getChangePro"
	
	data = {
		"data": cookie,
	}
	check = 0
	if int(checkCookies(cookie)) != 1:
		return "%s,cookie已失效" % cookie
	while check < 3:
		res = requests.post(url, json=data)
		if "【账号】null" in res.text:
			print("查询失败")
			check += 1
		else:
			return res.text
	return "查询异常，已失败重试三次"


if __name__ == '__main__':
	# token = get_ql_token()
	# id, cookie_name, cookie_remarks = ql_cookie_id("pt_pin=jd_jqa;", token)
	# status = update_env_cookie(id, cookie_name, cookie_remarks, token, "pt_key=666667;pt_pin=jd_jqa;")
	# if status == 0:
	#     print("成功")
	# else:
	#     print("faild")
	# show_jd(
	# 'pt_key=AAJi_Y-HADBJGgqcaxAruSv4PrAuLlFsFLVm_Aee80p5OFyBncdwCNpyYKEYatvUqpNsz40mHUM;pt_pin=jd_JcOdblyhWOIT;')
	# run("pt_pin=jd_JcOdblyhWOIT;",
	#     "pt_key=AAJi_Y-HADBJGgqcaxAruSv4PrAuLlFsFLVm_Aee80p5OFyBncdwCNpyYKEYatvUqpNsz40mHUM;pt_pin=jd_JcOdblyhWOIT;")
	add_jd_cookie(get_ql_token(), "ptxxx", "liuml")
