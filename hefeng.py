#!/usr/bin/env python
# encoding: utf-8
"""
@Project ：pythonProject
@file: 和风天气api.py
@time: 2022/8/24 16:54
@Author: 寂情啊
@contact: 1758812645@qq.com
"""
import requests


class hfapi():
    def __init__(self, key, adm, location):
        self.key = key
        # 城市id
        self.location = location
        self.adm = adm
        self.location, self.city_lon, self.city_lat = self.city()
        # 经度, 纬度

    def city(self):
        # 城市信息查询 https://dev.qweather.com/docs/api/geo/city-lookup/
        url = "https://geoapi.qweather.com/v2/city/lookup"
        params = {
            "key": self.key,
            "location": self.location,
            # 需要查询地区的名称，支持文字、以英文逗号分隔的经度,纬度坐标（十进制，最多支持小数点后两位）、LocationID或Adcode（仅限中国城市）。例如 location=北京 或 location=116.41,39.92
            "adm": self.adm,
            # 城市的上级行政区划，默认不限定行政区划。 可设定只在某个行政区划范围内进行搜索，用于排除重名城市或对结果进行过滤。例如 adm=beijing
            # 如请求参数为location=chaoyang&adm=beijing时，返回的结果只包括北京市的朝阳区，而不包括辽宁省的朝阳市 如请求参数仅为location=chaoyang时，返回的结果包括北京市的朝阳区、辽宁省的朝阳市以及长春市的朝阳区
        }
        res = requests.get(url, params=params).json()
        # 地区/城市名称
        city_name = res["location"][0]["name"]
        # 地区/城市ID
        city_id = res["location"][0]["id"]
        #	地区/城市经度
        city_lon = res["location"][0]["lon"]
        # 地区/城市纬度
        city_lat = res["location"][0]["lat"]
        # 地区/城市的上级行政区划名称
        city_adm2 = res["location"][0]["adm2"]
        # 地区/城市所属一级行政区域
        city_adm1 = res["location"][0]["adm1"]
        # 地区/城市所属国家名称
        city_country = res["location"][0]["country"]
        #	地区评分
        city_rank = res["location"][0]["rank"]
        # 城市code 经度, 纬度
        return city_id, city_lon, city_lat

    def city_poi_range(self):
        # POI范围搜索 https://dev.qweather.com/docs/api/geo/poi-range/
        url = "https://geoapi.qweather.com/v2/poi/range"
        params = {
            "key": self.key,
            # 需要查询地区的以英文逗号分隔的经度,纬度坐标（十进制，最多支持小数点后两位）、LocationID或
            "location": "{},{}".format(self.city_lon, self.city_lat),
            # scenic 景点 CSTA 潮流站点  TSTA 潮汐站点
            "type": "scenic",
            # 搜索范围，可设置搜索半径，取值范围1-50，单位：公里。默认5公里
            "radius": "10",
            # 返回结果的数量，取值范围1-20，默认返回10个结果
            "number": "6"
        }
        res = requests.get(url, params=params).json()
        # 地区/城市名称
        for i in res["poi"]:
            # POI（兴趣点）名称
            print(i["name"])
            # POI（兴趣点）ID
            print(i["id"])
            # POI（兴趣点）经度
            print(i["lon"])
            # POI（兴趣点）纬度
            print(i["lat"])
            # POI（兴趣点）的上级行政区划名称
            print(i["adm2"])
            # POI（兴趣点）所属一级行政区域
            print(i["adm1"])
            #	POI（兴趣点）所属国家名称
            print(i["country"])
            # 地区评分
            print(i["rank"])

    def city_poi_info(self):
        # POI信息搜索 https://dev.qweather.com/docs/api/geo/poi-lookup/
        url = "https://geoapi.qweather.com/v2/poi/lookup"
        params = {
            "key": self.key,
            # 需要查询地区的名称，支持文字、以英文逗号分隔的经度,纬度坐标（十进制，最多支持小数点后两位）、LocationID或Adcode（仅限中国城市）。例如 location=北京 或 location=116.41,39.92
            "location": "广州",
            # scenic 景点 CSTA 潮流站点  TSTA 潮汐站点
            "type": "scenic",
            # 返回结果的数量，取值范围1-20，默认返回10个结果
            "number": "6"
        }
        res = requests.get(url, params=params).json()
        for i in res["poi"]:
            # POI（兴趣点）名称
            print(i["name"])
            # POI（兴趣点）ID
            print(i["id"])
            # POI（兴趣点）经度
            print(i["lon"])
            # POI（兴趣点）纬度
            print(i["lat"])
            # POI（兴趣点）的上级行政区划名称
            print(i["adm2"])
            # POI（兴趣点）所属一级行政区域
            print(i["adm1"])
            # POI（兴趣点）所属国家名称
            print(i["country"])
            #	地区评分
            print(i["rank"])

    def now_weather(self):
        """
        实时天气
        :return:
        """
        # 实时天气说明 https://dev.qweather.com/docs/api/weather/weather-now/
        url = "https://devapi.qweather.com/v7/weather/now"
        params = {
            "key": self.key,
            "location": self.location,  # https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv
        }
        res = requests.get(url, params=params).json()
        # 数据观测时间
        print(res["now"]["obsTime"])
        # 风向
        print(res["now"]["windDir"])
        # 风力等级
        print(res["now"]["windScale"])
        # 风速
        print(res["now"]["windSpeed"])
        # 实时温度
        real = res["now"]["temp"]
        real = real + "℃"
        # 体感温度
        print(res["now"]["feelsLike"])
        # 相对湿度
        print(res["now"]["humidity"])
        # 当前小时累计降水量，默认单位：毫米
        print(res["now"]["precip"])
        # 天气状况的文字描述
        print(res["now"]["text"])
        # 能见度，默认单位：公里
        print(res["now"]["vis"])
        # 云量，百分比数值。可能为空
        print(res["now"]["cloud"])
        return real

    def h_weather(self):
        # 逐小时天气预报 https://dev.qweather.com/docs/api/weather/weather-hourly-forecast/
        url = "https://devapi.qweather.com/v7/weather/24h"
        params = {
            "key": self.key,
            "location": self.location,  # https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv
        }
        res = requests.get(url, params=params).json()
        # 预报时间 0为下一个小时，当前为10：10，则0代表11：00  1为12：00依次类推
        print(res["hourly"][0]["fxTime"])
        #	温度，默认单位：摄氏度
        print(res["hourly"][0]["temp"])
        # 天气状况的文字描述，包括阴晴雨雪等天气状态的描述
        print(res["hourly"][0]["text"])
        # 风向
        print(res["hourly"][0]["windDir"])
        # 风力等级
        print(res["hourly"][0]["windScale"])
        # 风速，公里/小时
        print(res["hourly"][0]["windSpeed"])
        # 相对湿度，百分比数值
        print(res["hourly"][0]["humidity"])
        # 当前小时累计降水量，默认单位：毫米
        print(res["hourly"][0]["precip"])
        # 逐小时预报降水概率，百分比数值，可能为空
        pop = res["hourly"][0]["pop"]
        pop = pop + "%"
        # 云量，百分比数值。可能为空
        print(res["hourly"][0]["cloud"])
        return pop

    def today_weather(self):
        # 逐天天气说明 https://dev.qweather.com/docs/api/weather/weather-daily-forecast/
        # 最近三天的预报 支持 3 7
        url = "https://devapi.qweather.com/v7/weather/3d"
        params = {
            "key": self.key,
            "location": self.location,  # https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv
        }
        res = requests.get(url, params=params).json()
        # 预报日期
        print(res["daily"][0]["fxDate"])
        # 日出时间
        print(res["daily"][0]["sunrise"])
        # 日落时间
        print(res["daily"][0]["sunset"])
        # 月升时间
        print(res["daily"][0]["moonrise"])
        # 月落时间
        print(res["daily"][0]["moonset"])
        # 月相名称
        print(res["daily"][0]["moonPhase"])
        # 预报当天最高温度
        tempMax = res["daily"][0]["tempMax"]
        # 预报当天最低温度
        tempMin = res["daily"][0]["tempMin"]
        # 预报白天风向
        print(res["daily"][0]["windDirDay"])
        # 预报白天风力等级
        print(res["daily"][0]["windScaleDay"])
        # 预报白天风速，公里/小时
        print(res["daily"][0]["windSpeedDay"])
        # 预报夜间当天风向
        print(res["daily"][0]["windDirNight"])
        # 预报夜间风力等级
        print(res["daily"][0]["windScaleNight"])
        # 预报夜间风速，公里/小时
        print(res["daily"][0]["windSpeedNight"])
        # 预报当天总降水量，默认单位：毫米
        print(res["daily"][0]["precip"])
        # 紫外线强度指数
        print(res["daily"][0]["uvIndex"])
        # 相对湿度，百分比数值
        print(res["daily"][0]["humidity"])
        # 能见度，默认单位：公里
        print(res["daily"][0]["vis"])
        # 云量，百分比数值。可能为空
        print(res["daily"][0]["cloud"])
        # 预报白天天气状况文字描述 0为今天，1为明天，依次类推
        weather = res["daily"][0]["textDay"]
        # 预报晚间天气状况文字描述
        print(res["daily"][0]["textNight"])
        # 温度区间
        wendu = tempMin + "℃" + "~" + tempMax + "℃"
        # 天气 温度区间
        return weather, wendu

    def warining_weather(self):
        # 天气灾害预警 https://dev.qweather.com/docs/api/warning/weather-warning/
        url = "https://devapi.qweather.com/v7/warning/now"
        params = {
            "key": self.key,
            "location": self.location,  # https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv
        }
        res = requests.get(url, params=params).json()
        if not res["warning"]:
            print("无告警")
        else:
            # 本条预警的唯一标识，可判断本条预警是否已经存在
            print(res["warning"]["id"])
            # 预警发布单位，可能为空
            print(res["warning"]["sender"])
            # 预警发布时间
            print(res["warning"]["pubTime"])
            # 预警信息标题
            print(res["warning"]["title"])
            # 预警开始时间，可能为空
            print(res["warning"]["startTime"])
            #	预警结束时间，可能为空
            print(res["warning"]["endTime"])
            #	预警信息的发布状态
            print(res["warning"]["status"])
            # 预警严重等级
            print(res["warning"]["severity"])
            #	预警严重等级颜色，可能为空
            print(res["warning"]["severityColor"])
            #	预警类型ID
            print(res["warning"]["type"])
            # 预警类型名称
            print(res["warning"]["typeName"])
            #	预警信息的紧迫程度，可能为空
            print(res["warning"]["urgency"])
            #	预警信息的确定性，可能为空
            print(res["warning"]["certainty"])
            # 预警详细文字描述
            print(res["warning"]["text"])

    def sun_weather(self):
        # 日出日落 https://dev.qweather.com/docs/api/astronomy/sunrise-sunset/

        url = "https://devapi.qweather.com/v7/astronomy/sun"
        params = {
            "key": self.key,
            "location": self.location,  # https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv
            # 获取最近未来60天全球城市日出日落时间
            "date": "20220826",
        }
        res = requests.get(url, params=params).json()
        # 日出时间
        print(res["sunrise"])
        # 日落时间
        print(res["sunset"])

    def moon_weather(self):
        # 月升月落和月相 https://dev.qweather.com/docs/api/astronomy/moon-and-moon-phase/

        url = "https://devapi.qweather.com/v7/astronomy/moon"
        params = {
            "key": self.key,
            "location": self.location,  # https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv
            # 获取最近未来60天全球城市日出日落时间
            "date": "20220826",
        }
        res = requests.get(url, params=params).json()
        # 月升时间
        print(res["moonrise"])
        # 月落时间
        print(res["moonset"])
        # 月相逐小时预报时间
        print(res["moonPhase"][0]["fxTime"])
        #	月相数值
        print(res["moonPhase"][0]["value"])
        # 月相名字
        print(res["moonPhase"][0]["name"])
        # 月亮照明度，百分比数值
        print(res["moonPhase"][0]["illumination"])

    def life(self):
        # 天气生活指数 https://dev.qweather.com/docs/api/indices/

        url = "https://devapi.qweather.com/v7/indices/1d"
        params = {
            "key": self.key,
            "location": self.location,  # https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv
            # 生活指数的类型ID，包括洗车指数、穿衣指数、钓鱼指数等。可以一次性获取多个类型的生活指数，多个类型用英文,分割。例如type=3,5。具体生活指数的ID和等级参考天气指数信息。各项生活指数并非适用于所有城市
            # https://dev.qweather.com/docs/resource/indices-info/
            # 0代表全部指数
            "type": "0",
        }
        res = requests.get(url, params=params).json()
        # for i in res["daily"]:
        #     # 预报日期
        #     print(i["date"])
        #     # 生活指数类型ID
        #     print(i["type"])
        #     #	生活指数类型的名称
        #     print(i["name"])
        #     # 生活指数预报等级
        #     print(i["level"])
        #     # 生活指数预报级别名称
        #     print(i["category"])
        #     # 生活指数预报的详细描述，可能为空
        #     print(i["text"])
        # 交通指数
        tips = res["daily"][14]['text']
        return tips


if __name__ == '__main__':
    now = hfapi("fb4c2738a7974c2ab4028cd6fe299532", "广东", "天河")
    # now.now_weather()
    # now.h_weather()
    # now.today_weather()
    # now.warining_weather()
    # now.sun_weather()
    # now.moon_weather()
    now.life()
    # now.city()
    # now.city_poi_range()
    # now.city_poi_info()
