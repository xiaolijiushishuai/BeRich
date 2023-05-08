import datetime

import requests


headers = {"sec-ch-ua": "", "x-xsrf-token": "bb5f2e", "sec-ch-ua-mobile": "?0", "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Mobile Safari/537.36", "accept": "application/json, text/plain, */*", "mweibo-pwa": "1", "x-requested-with": "XMLHttpRequest", "sec-ch-ua-platform": "Windows", "sec-fetch-site": "same-origin", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://m.weibo.cn/", "accept-encoding": "gzip, deflate, br", "accept-language": "zh-CN", "cookie": "SUB=_2A25JUjGODeRhGeNL61oY8yfFzzuIHXVqvV_GrDV6PUJbktAGLWLQkW1NSTlhSzMnHDb8rCJPfjv9Vdo803SIbKoS; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWef-c.oDMGP.TaUWJPnSJs5NHD95QfSK5R1Ke41KBNWs4DqcjwB-_Wi--Ni-2Xi-i8i--Xi-ihiKLWi--NiKy8iKyF; SSOLoginState=1683374558; _T_WM=22041737488; XSRF-TOKEN=bb5f2e; WEIBOCN_FROM=1110005030; mweibo_short_token=49d08dfca6; MLOGIN=1; M_WEIBOCN_PARAMS=uicode%3D20000174"}
cookies = {"MLOGIN": "1", "mweibo_short_token": "abaa7bb2a6", "WEIBOCN_FROM": "1110005030", "M_WEIBOCN_PARAMS": "uicode%3D20000174", "XSRF-TOKEN": "c048bd", "SSOLoginState": "1683380777", "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WWef-c.oDMGP.TaUWJPnSJs5NHD95QfSK5R1Ke41KBNWs4DqcjwB-_Wi--Ni-2Xi-i8i--Xi-ihiKLWi--NiKy8iKyF", "_T_WM": "23517507620", "SUB": "_2A25JUip5DeRhGeNL61oY8yfFzzuIHXVqvLYxrDV6PUJbktAGLXfmkW1NSTlhS3z0hMlKfdK9zqIy-g0o0aJOXQzw"}
url = "https://m.weibo.cn/api/statuses/update"


data = {
    "content": "666有一天那个孩子长大了，会想起童年的事，会想起那些晃动的树影儿，会想起他自己的妈妈。他会跑去看看那棵树。但他不会知道那棵树是谁种的，是怎么种的。",
    "st": "0f2399",
    "_spr": "screen:1536x864"
}
# response = requests.post(url, headers=headers, cookies=cookies, data=data)
#
# #url="https://m.weibo.cn"
#
# #response=requests.get(url)
# print(response.status_code==200)
# print(response.text)
# print(response.headers)
# print(response.cookies.get_dict())

cookies = [
    {'domain': '.weibo.cn', 'expiry': 1683384382, 'httpOnly': False, 'name': 'MLOGIN', 'path': '/', 'sameSite': 'Lax',
     'secure': False, 'value': '1'},
    {'domain': '.weibo.cn', 'expiry': 1683380795, 'httpOnly': True, 'name': 'mweibo_short_token', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': 'abaa7bb2a6'},
    {'domain': '.weibo.cn', 'httpOnly': True, 'name': 'WEIBOCN_FROM', 'path': '/', 'sameSite': 'Lax', 'secure': False,
     'value': '1110005030'},
    {'domain': '.weibo.cn', 'expiry': 1683381382, 'httpOnly': True, 'name': 'M_WEIBOCN_PARAMS', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': 'uicode%3D20000174'},
    {'domain': '.m.weibo.cn', 'expiry': 1683381982, 'httpOnly': False, 'name': 'XSRF-TOKEN', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': 'c048bd'},
    {'domain': '.weibo.cn', 'httpOnly': False, 'name': 'SSOLoginState', 'path': '/', 'sameSite': 'None', 'secure': True,
     'value': '1683380777'},
    {'domain': '.weibo.cn', 'expiry': 1714916780, 'httpOnly': False, 'name': 'SUBP', 'path': '/', 'sameSite': 'None',
     'secure': True,
     'value': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWef-c.oDMGP.TaUWJPnSJs5NHD95QfSK5R1Ke41KBNWs4DqcjwB-_Wi--Ni-2Xi-i8i--Xi-ihiKLWi--NiKy8iKyF'},
    {'domain': '.weibo.cn', 'expiry': 1683388802, 'httpOnly': False, 'name': '_T_WM', 'path': '/', 'sameSite': 'Lax',
     'secure': False, 'value': '23517507620'},
    {'domain': '.weibo.cn', 'expiry': 1714916780, 'httpOnly': True, 'name': 'SUB', 'path': '/', 'sameSite': 'None',
     'secure': True,
     'value': '_2A25JUip5DeRhGeNL61oY8yfFzzuIHXVqvLYxrDV6PUJbktAGLXfmkW1NSTlhS3z0hMlKfdK9zqIy-g0o0aJOXQzw'}]

print(str(cookies))

# def get_server_time_tomin():
#     """获取当前时间：%Y-%m-%d %H:%M"""
#     now = datetime.datetime.now()
#     formatted_time = datetime.datetime.strftime(now,"%Y-%m-%d %H:%M")
#     print("当前时间：", formatted_time)
#     return formatted_time
#
# get_server_time_tomin()
#
# print("2023-05-04 21:22:00"[0:len("2023-05-04 21:22:00")-3])