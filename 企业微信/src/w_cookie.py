import json
import os

cookies_filename = "./jd_cookies.json"


def jd_cookies():
    jd_cookie = {}
    # jd_cookie["pt_pin=15816170703_p;"] = "LiuMengLong"
    # jd_cookie["pt_pin=15816170703_pddd;"] = "LiuMengLong"
    w_cookie(jd_cookie)


def w_cookie(jd_cookie):
    with open(cookies_filename, "w") as f:
        json.dump(jd_cookie, f)


def file_exits():
    if os.path.exists(cookies_filename):
        pass
    else:
        jd_cookies()


def read_jd_cookies():
    file_exits()
    with open(cookies_filename, 'r') as load_f:
        jd_cookie = json.load(load_f)
        return jd_cookie


def write_jd_cookies(ptkey, username, cookie):
    """

    :param ptkey:  cookie中的pt_key，相当于京东用户名
    :param username:  微信的userid
    :param cookie:    京东cookie 格式为 pt_key;pt_pin;
    :return:    json字典 ｛'微信的userid':{'pt_key':'cookie'}｝
    """
    jd_cookie = read_jd_cookies()
    # jd_cookie[username] = jd_cookie[username]
    try:
        jd_cookie[username]
    except KeyError:
        jd_cookie[username] = {}
    jd_cookie[username][ptkey] = cookie
    w_cookie(jd_cookie)
    return jd_cookie


if __name__ == '__main__':
    # 写入到文件
    # res = write_jd_cookies("pt_3;", "jqf2", "pt_key=djalfjl;pt_pin=fafja;")
    # print(res)

    # 从文件读
    res = read_jd_cookies()
    for pt_pin in res["jqf"]:
        print(res["jqf"][pt_pin])
