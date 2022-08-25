#!/usr/bin/env python
# encoding: utf-8
"""
@Project ：pythonProject
@file: wx.py
@time: 2022/8/23 10:13
@Author: 寂情啊
@contact: 1758812645@qq.com
"""
import random
from time import localtime
from requests import get, post
from datetime import datetime, date
import sys
import os
import http.client, urllib
import json
from zhdate import ZhDate
from hefeng import hfapi


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token


def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday


    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


# 天气
def get_weather(city):
    url = 'http://api.tianapi.com/tianqi/index'
    params = urllib.parse.urlencode({'key': 'e46dc5527dc901b24140a76854f70966', 'city': '天河区'})
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    res = post(url, headers=headers, params=params)
    data = json.loads(res.text)
    # 今日天气，明日天气索引唯1
    # print(data['newslist'][0])
    # 今天
    sunny = data['newslist'][0]
    # 明天
    sunny1 = data['newslist'][1]
    # 天气
    weather = sunny["weather"]
    # 实时温度
    real = sunny["real"]
    # 温度区间
    wendu = sunny["lowest"] + "~" + sunny["highest"]
    # 风向
    wind = sunny["wind"]
    # 风速，km/h
    windspeed = sunny["windspeed"]
    # 风力
    windsc = sunny["windsc"]
    # 日出时间
    sunrise = sunny["sunrise"]
    # 日落时间
    sunset = sunny["sunset"]
    # 月升时间
    moonrise = sunny["moonrise"]
    # 月落时间
    moondown = sunny["moondown"]
    # 降雨量
    pcpn = sunny["pcpn"]
    # 降雨概率
    pop = sunny["pop"] + "%"
    # 紫外线强度指数
    uv_index = sunny["uv_index"]
    # 能见度，单位：公里
    vis = sunny["vis"]
    # 相对湿度
    humidity = sunny["humidity"]
    # 生活指数提示
    tips = sunny["tips"]
    return weather, real, wendu, pop, tips


def get_hf_weather(hf_key, country, city):
    hf_weather = hfapi(hf_key, country, city)
    weather, wendu = hf_weather.today_weather()
    real = hf_weather.now_weather()
    pop = hf_weather.h_weather()
    tips = hf_weather.life()
    return weather, real, wendu, pop, tips


# 词霸每日一句
def get_ciba():
    if (Whether_Eng != "否"):
        url = "http://open.iciba.com/dsapi/"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        r = get(url, headers=headers)
        note_en = r.json()["content"]
        note_ch = r.json()["note"]
        return note_ch, note_en
    else:
        return "", ""


# 彩虹屁
def caihongpi():
    if (caihongpi_API != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
        params = urllib.parse.urlencode({'key': caihongpi_API})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/caihongpi/index', params, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = data["newslist"][0]["content"]
        if ("XXX" in data):
            data.replace("XXX", "蒋蒋")
        return data
    else:
        return ""


# 健康小提示API
def health():
    if (health_API != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
        params = urllib.parse.urlencode({'key': health_API})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/healthtip/index', params, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = data["newslist"][0]["content"]
        return data
    else:
        return ""


# 星座运势
def lucky():
    if (lucky_API != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
        params = urllib.parse.urlencode({'key': lucky_API, 'astro': astro})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/star/index', params, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = "爱情指数：" + str(data["newslist"][1]["content"]) + "\n速配星座：" + str(
            data["newslist"][7]["content"]) + "\n工作指数：" + str(data["newslist"][2]["content"]) + "\n今日概述：" + str(
            data["newslist"][8]["content"])
        # print(data)
        return data
    else:
        return ""


# 励志名言
def lizhi():
    if (lizhi_API != "替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
        params = urllib.parse.urlencode({'key': lizhi_API})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/lzmy/index', params, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        return data["newslist"][0]["saying"]
    else:
        return ""


# 推送信息
def send_message(to_user, access_token, city, weather, real, wendu, pipi, lizhi, pop, tips,
                 note_en, note_ch, health_tip, lucky_):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]

    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "city": {
                "value": city,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "wendu": {
                "value": wendu,
                "color": get_color()
            },
            "real": {
                "value": real,
                "color": get_color()
            },
            "love_day": {
                "value": love_days,
                "color": get_color()
            },
            "note_en": {
                "value": note_en,
                "color": get_color()
            },
            "note_ch": {
                "value": note_ch,
                "color": get_color()
            },

            "pipi": {
                "value": pipi,
                "color": get_color()
            },

            "lucky": {
                "value": lucky_,
                "color": get_color()
            },

            "lizhi": {
                "value": lizhi,
                "color": get_color()
            },

            "pop": {
                "value": pop,
                "color": get_color()
            },

            "health": {
                "value": health_tip,
                "color": get_color()
            },

            "tips": {
                "value": tips,
                "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value, year, today)
        # 将生日数据插入data
        data["data"][key] = {"value": birth_day, "color": get_color()}
        # print(data)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入省份和市获取天气信息
    city = config["city"]
    # 省份
    country = config["country"]
    # 和风API
    hefeng_API = config["hefeng_API"]
    # 是否启动和风天气api
    Whether_hefeng = config["Whether_hefeng"]
    if Whether_hefeng == "是":
        weather, real, wendu, pop, tips = get_hf_weather(hefeng_API, country, city)
    else:
        # 天行api 天气，实时温度,温度区间，降雨概率，小贴士
        weather, real, wendu, pop, tips = get_weather(city)
    # 获取彩虹屁API
    caihongpi_API = config["caihongpi_API"]
    # 获取励志古言API
    lizhi_API = config["lizhi_API"]
    # 获取天气预报API
    tianqi_API = config["tianqi_API"]
    # 是否启用词霸每日金句
    Whether_Eng = config["Whether_Eng"]
    # 获取健康小提示API
    health_API = config["health_API"]
    # 获取星座运势API
    lucky_API = config["lucky_API"]
    # 获取星座
    astro = config["astro"]
    # 获取词霸每日金句
    note_ch, note_en = get_ciba()
    # 彩虹屁
    pipi = caihongpi()
    # 健康小提示
    health_tip = health()
    # 励志名言
    lizhi = lizhi()
    # 星座运势
    lucky_ = lucky()
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, city, weather, real, wendu, pipi, lizhi, pop, tips,
                     note_en, note_ch, health_tip, lucky_)
