import requests


def checkCookies(cookies):
    """

    :param cookies:  京东cookie列表
    :return: 返回列表 1有效 0 无效
    """
    cookie_status = list()
    for cookie in cookies:
        url = 'https://plogin.m.jd.com/cgi-bin/ml/islogin'
        headers = {
            "Cookie": cookie,
            "referer": "https://h5.m.jd.com/",
            "User-Agent": "jdapp;iPhone;10.1.2;15.0;network/wifi;Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML,like Gecko) Mobile/15E148;supportJDSHWK/1",
        }
        res = requests.get(url, headers=headers).json()
        cookie_status.append(res["islogin"])
    return cookie_status


if __name__ == '__main__':
    a = checkCookies(
        ["pt_key=AAJi_Y-HADBJGgqcaxAruSv4PrAuLlFsFLVm_Aee80p5OFyBncdwCNpyYKEYatvUqpNsz40mHUM;pt_pin=jd_JcOdblyhWOIT;",
         "pt_key=AAJjDFQJADBX8mC_wTYnGlSZ_v0c9TLqNQbRLRMHTKea712gSEDc5rbwbYREYHM3gQar2XWzh4c;pt_pin=qz%E6%9C%A8%E5%AD%90;",
         "pt_key=AAJjDFQJADBX8mC_wTYnfsfs"])
    print(a)
