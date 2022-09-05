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


def write_jd_cookies(ptkey, username):
    jd_cookie = read_jd_cookies()
    jd_cookie[ptkey] = username
    w_cookie(jd_cookie)
    return jd_cookie


if __name__ == '__main__':
    # 写入到文件
    res = write_jd_cookies("pt_jflajfklb;", "jqf")
    print(res)
    # 从文件读
    res = read_jd_cookies()
    print(res)
