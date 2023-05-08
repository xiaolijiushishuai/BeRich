import random
import time

import requests
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

browser_dict = {}
mobileName = ["BlackBerry Z30", "Blackberry PlayBook", "Galaxy Note 3", "Kindle Fire HDX", "LG Optimus L70",
              "Laptop with HiDPI screen", "Laptop with MDPI screen", "Laptop with touch", "Microsoft Lumia 550",
              "Microsoft Lumia 950", "Moto G4", "Nexus 10", "Nexus 4", "Nexus 5", "Nexus 5X", "Nexus 6", "Nexus 6P",
              "Nexus 7", "Nokia Lumia 520", "Nokia N9", "iPad Mini", "iPhone 4", "JioPhone 2", "Galaxy S5",
              "Pixel 2", "Pixel 2 XL", "iPhone 5/SE", "iPhone 6/7/8", "iPhone 6/7/8 Plus", "iPhone X", "iPad",
              "iPad Pro", "Surface Duo", "Galaxy Fold"]

def get_webdriver(account):
    global browser_dict
    if account not in browser_dict.keys():
        create_webdriver(account)
    return browser_dict[account]


def close_webdriver(account):
    browser = get_webdriver(account)
    browser.close()
    browser.quit()
    del browser_dict[account]

def create_webdriver(account):
    # 创建Chrome浏览器实例
    # chrome_options = Options()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 开发者模式
    chrome_options.add_argument('--ignore-certificate-errors')  # 开发者模式
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    # chrome_options.add_argument('--proxy-server={}'.format(ip))  # 添加代理
    chrome_options.add_argument('--headless')  # 无界面
    chrome_options.add_argument('--disable-infobars')  # 关闭操控提示
    chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在报错问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU硬件加速。如果软件渲染器没有就位，则GPU进程将不会启动。
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    chrome_options.add_experimental_option("prefs", prefs)  # 禁用css和图片
    device_name = mobileName[random.randint(0, len(mobileName) - 1)]
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": device_name})  # 模拟手机类型
    global browser_dict
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(5)
    browser_dict[account] = browser



if __name__ == '__main__':
    browser=create_webdriver("18146725110");
    browser=get_webdriver("18146725110")

    browser.get("https://m.weibo.cn/compose/")
    browser.delete_all_cookies()
    cookies = [{'domain': '.weibo.cn', 'expiry': 1683384382, 'httpOnly': False, 'name': 'MLOGIN', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1'}, {'domain': '.weibo.cn', 'expiry': 1683380795, 'httpOnly': True, 'name': 'mweibo_short_token', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'abaa7bb2a6'}, {'domain': '.weibo.cn', 'httpOnly': True, 'name': 'WEIBOCN_FROM', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1110005030'}, {'domain': '.weibo.cn', 'expiry': 1683381382, 'httpOnly': True, 'name': 'M_WEIBOCN_PARAMS', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'uicode%3D20000174'}, {'domain': '.m.weibo.cn', 'expiry': 1683381982, 'httpOnly': False, 'name': 'XSRF-TOKEN', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'c048bd'}, {'domain': '.weibo.cn', 'httpOnly': False, 'name': 'SSOLoginState', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1683380777'}, {'domain': '.weibo.cn', 'expiry': 1714916780, 'httpOnly': False, 'name': 'SUBP', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWef-c.oDMGP.TaUWJPnSJs5NHD95QfSK5R1Ke41KBNWs4DqcjwB-_Wi--Ni-2Xi-i8i--Xi-ihiKLWi--NiKy8iKyF'}, {'domain': '.weibo.cn', 'expiry': 1683388802, 'httpOnly': False, 'name': '_T_WM', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '23517507620'}, {'domain': '.weibo.cn', 'expiry': 1714916780, 'httpOnly': True, 'name': 'SUB', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '_2A25JUip5DeRhGeNL61oY8yfFzzuIHXVqvLYxrDV6PUJbktAGLXfmkW1NSTlhS3z0hMlKfdK9zqIy-g0o0aJOXQzw'}]

    # cookies={"MLOGIN": "1", "mweibo_short_token": "abaa7bb2a6", "WEIBOCN_FROM": "1110005030",
    #  "M_WEIBOCN_PARAMS": "uicode%3D20000174", "XSRF-TOKEN": "c048bd", "SSOLoginState": "1683380777",
    #  "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WWef-c.oDMGP.TaUWJPnSJs5NHD95QfSK5R1Ke41KBNWs4DqcjwB-_Wi--Ni-2Xi-i8i--Xi-ihiKLWi--NiKy8iKyF",
    #  "_T_WM": "23517507620",
    #  "SUB": "_2A25JUip5DeRhGeNL61oY8yfFzzuIHXVqvLYxrDV6PUJbktAGLXfmkW1NSTlhS3z0hMlKfdK9zqIy-g0o0aJOXQzw"}

    for cookie in cookies:
        # cookie_dict = {
        # 'domain': 'passport.weibo.cn',
        # 'name': cookie.get('name'),
        # 'value': cookie.get('value'),
        # "expires": cookie.get('value'),
        # 'path': '/',
        # 'httpOnly': False,
        # 'HostOnly': False,
        # 'Secure': False}
        browser.add_cookie(cookie)

    browser.headers={"sec-ch-ua": "", "x-xsrf-token": "bb5f2e", "sec-ch-ua-mobile": "?0", "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Mobile Safari/537.36", "accept": "application/json, text/plain, */*", "mweibo-pwa": "1", "x-requested-with": "XMLHttpRequest", "sec-ch-ua-platform": "Windows", "sec-fetch-site": "same-origin", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://m.weibo.cn/", "accept-encoding": "gzip, deflate, br", "accept-language": "zh-CN", "cookie": "SUB=_2A25JUjGODeRhGeNL61oY8yfFzzuIHXVqvV_GrDV6PUJbktAGLWLQkW1NSTlhSzMnHDb8rCJPfjv9Vdo803SIbKoS; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWef-c.oDMGP.TaUWJPnSJs5NHD95QfSK5R1Ke41KBNWs4DqcjwB-_Wi--Ni-2Xi-i8i--Xi-ihiKLWi--NiKy8iKyF; SSOLoginState=1683374558; _T_WM=22041737488; XSRF-TOKEN=bb5f2e; WEIBOCN_FROM=1110005030; mweibo_short_token=49d08dfca6; MLOGIN=1; M_WEIBOCN_PARAMS=uicode%3D20000174"}

    print(browser.get_cookies())
    print(browser.page_source)

   # browser.find_element(By.XPATH, "//*[@id='app']/div[1]/div/main/div[1]/div/span/textarea[1]").send_keys(
    #    "this is for test by pgm")

   # browser.find_element(By.XPATH, "//*[@id='app']/div[1]/div/header/div[3]/a").click()

    browser.get("https://m.weibo.cn/compose/")

    time.sleep(999)





















