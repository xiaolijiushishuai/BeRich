import datetime
import json

import requests



account_id = '36'

headers = {"sec-ch-ua": "", "x-xsrf-token": "b72af5", "sec-ch-ua-mobile": "?0", "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.63 Mobile Safari/537.36", "accept": "application/json, text/plain, */*", "mweibo-pwa": "1", "x-requested-with": "XMLHttpRequest", "sec-ch-ua-platform": "Windows", "sec-fetch-site": "same-origin", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://m.weibo.cn/compose/", "accept-encoding": "gzip, deflate, br", "cookie": "XSRF-TOKEN=b72af5; _T_WM=73920313007; SUB=_2A25JWIHlDeRhGeNL61oY8yfFzzuIHXVqoi-trDV6PUJbktAGLROkkW1NSTlhS5yDtxHtQk5Xge8Nr0WJXH13fb4Q; WEIBOCN_FROM=1110006030; MLOGIN=1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWef-c.oDMGP.TaUWJPnSJs5NHD95QfSK5R1Ke41KBNWs4DqcjwB-_Wi--Ni-2Xi-i8i--Xi-ihiKLWi--NiKy8iKyF; SSOLoginState=1683812789; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174"}

cookies = {"SSOLoginState": "1683812789", "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WWef-c.oDMGP.TaUWJPnSJs5NHD95QfSK5R1Ke41KBNWs4DqcjwB-_Wi--Ni-2Xi-i8i--Xi-ihiKLWi--NiKy8iKyF", "MLOGIN": "1", "mweibo_short_token": "6fc8e504bd", "WEIBOCN_FROM": "1110006030", "SUB": "_2A25JWIHlDeRhGeNL61oY8yfFzzuIHXVqoi-trDV6PUJbktAGLROkkW1NSTlhS5yDtxHtQk5Xge8Nr0WJXH13fb4Q", "_T_WM": "73920313007", "M_WEIBOCN_PARAMS": "luicode%3D20000174", "XSRF-TOKEN": "b72af5"}

essay_data = {
    "content": "666有一天那个孩子长大了，会想起童年的事，会想起那些晃动的树影儿，会想起他自己的妈妈。他会跑去看看那棵树。但他不会知道那棵树是谁种的，是怎么种的。",
    "st": "0f2399",
    "_spr": "screen:1536x864"
}

url = "https://m.weibo.cn/api/statuses/update"
# response = requests.post(url, headers=headers, cookies=cookies, data=data)

##get mid
getuid_url="https://m.weibo.cn/feed/friends?"

req=requests.get(getuid_url,headers=headers,cookies=cookies)
req_data=req.text.strip()
stList=json.loads(req_data)["data"]["statuses"]
print(type(stList))

mid=""
for st in stList:
    mid=st["mid"]
    #break
    print(mid)
    user=st["user"]
    print(user["screen_name"])
    break

comment_date={
    "content":"jiushizhemeshuai",
    "mid":mid,
    "st": "0f2399",
    "_spr": "screen:1536x864"
}
##send common
send_coment_url="https://m.weibo.cn/api/comments/create"
req=requests.post(send_coment_url,headers=headers,cookies=cookies,data=comment_date)
print(req.status_code)

light_star_data={
    "id":mid,
    "attitude":"heart",
    "st": "0f2399",
    "_spr": "screen:1536x864"
}

##light star
light_star_url="https://m.weibo.cn/api/attitudes/create"
req=requests.post(send_coment_url,headers=headers,cookies=cookies,data=light_star_data)
print(req.status_code)

#
# #url="https://m.weibo.cn"
