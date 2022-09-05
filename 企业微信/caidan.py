import requests


class Menu(object):
    """
    企业微信机器人的菜单
    """

    def __init__(self):
        # 企业id
        self.corpid = 'ww8107c9a87314cd63'
        # 机器人secret
        self.corpsecret = 'KqU37pYD1XtPC10KGce_ccCuhSBqInORXn0kJsxkZnc'
        # 机器人id
        self.agentid = '1000002'

    def access_token(self):
        response = requests.get(
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}".format(
                corpid=self.corpid, corpsecret=self.corpsecret)).json()
        access_token = response['access_token']
        return access_token

    def create_menu(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/menu/create"
        token = self.access_token()
        params = {
            "access_token": token,
            "agentid": self.agentid
        }
        data = {
            "button": [
                {
                    "type": "click",
                    "name": "资产查询",
                    "key": "8689"
                }]
        }
        data1 = {
            "button": [
                {
                    "type": "click",
                    "name": "资产查询",
                    "key": "查询"
                },
                {
                    "name": "菜单",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "搜索",
                            "url": "http://www.soso.com/"
                        },
                        {
                            "type": "click",
                            "name": "赞一下我们",
                            "key": "V1001_GOOD"
                        }
                    ]
                }
            ]
        }

        res = requests.post(url, params=params, json=data).json()
        if res["errcode"] == 0:
            print("菜单更新成功")
            print(res)
        else:
            print(res)


if __name__ == '__main__':
    Menu().create_menu()
