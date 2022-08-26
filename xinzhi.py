#!/usr/bin/env python
# encoding: utf-8
"""
@Project ：pythonProject
@file: xinzhi.py
@time: 2022/8/26 9:20
@Author: 寂情啊
@contact: 1758812645@qq.com
"""
import requests


class xinzhi():
    def __init__(self, key, city):
        self.key = key
        self.city = city

    @staticmethod
    def now_weather(key, city="广州"):
        url = "https://api.seniverse.com/v3/weather/now.json"
        params = {
            "key": key,
            "location": city,
            #	当参数为 c 时，温度 c、风速 km/h、能见度 km、气压 mb
            # 当参数为 f 时，温度 f、风速 mph、能见度 mile、气压 inch
            # https://docs.seniverse.com/api/start/common.html#%E5%8D%95%E4%BD%8D-unit
            "unit": "c"
        }
        res = requests.get(url, params=params).json()
        # 城市名
        print(res["results"][0]["location"]["name"])
        # 城市全名
        print(res["results"][0]["location"]["path"])
        # 天气描述
        print(res["results"][0]["now"]["text"])
        # 实时温度
        print(res["results"][0]["now"]["temperature"])

    def today_weather(self):
        url = "https://api.seniverse.com/v3/weather/daily.json"
        params = {
            "key": self.key,
            # 位置（格式是 纬度:经度，英文冒号分隔)
            "location": self.city,
            # 返回几天数据，免费版最多三天
            "days": "1"
        }
        res = requests.get(url, params=params).json()
        print(res)
        # 城市名
        print(res["results"][0]["location"]["name"])
        for i in res["results"][0]["daily"]:
            # 时间
            print(i["date"])
            # 白天天气现象文字
            print(i["text_day"])
            # 晚间天气现象文字
            print(i["text_night"])
            # 当天最高温度
            print(i["high"])
            # 当天最低温度
            print(i["low"])
            # 降水量，单位mm
            print(i["rainfall"])
            # 降水概率，范围0~100，单位百分比（目前仅支持国外城市）
            print(i["precip"])
            # 风向文字
            print(i["wind_direction"])
            # 风速，单位km/h（当unit=c时）、mph（当unit=f时）
            print(i["wind_speed"])
            # 风力等级
            print(i["wind_scale"])
            # 相对湿度，0~100，单位为百分比
            print(i["humidity"])


if __name__ == '__main__':
    xinzhi.now_weather("SI_IOGtHmtik2u5L5")
    xz = xinzhi("SI_IOGtHmtik2u5L5", "广州")
    xz.today_weather()
