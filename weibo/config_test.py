import requests


headers = {
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
    "X-XSRF-TOKEN": "41d118",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://m.weibo.cn/profile/5750086190",
    "MWeibo-Pwa": "1",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "SUB": "_2A25JRaOUDeRhGeNJ7lIR-CjNwjyIHXVqyc3crDV6PUJbktANLXTfkW1NS9bVFCbqoI-XLJ2ex0yrapKpdugxzAVE",
    "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9Whb61kfVUy-4lS5.BxO-vE.5NHD95QfS0-7ehnceK.7Ws4Dqc_xi--Ri-2NiKn4i--fi-i8iK.Ni--Ri-isiK.4i--Xi-zRi-8Wi--fiK.7iKy2i--fi-82iK.Ni--fi-2fi-i2i--ciK.7iKL8i--Ni-8hiK.p",
    "SSOLoginState": "1682035652",
    "WEIBOCN_FROM": "1110006030",
    "MLOGIN": "1",
    "_T_WM": "86954133862",
    "M_WEIBOCN_PARAMS": "luicode%3D10000011%26lfid%3D1076036395287027%26uicode%3D20000174",
    "XSRF-TOKEN": "41d118"
}
url = "https://m.weibo.cn/api/config"
response = requests.get(url, headers=headers, cookies=cookies)

print(response.text)
print(response)