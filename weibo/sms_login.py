# -*- coding: utf-8 -*-
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options
mobileName = ["BlackBerry Z30", "Blackberry PlayBook", "Galaxy Note 3", "Kindle Fire HDX", "LG Optimus L70",
              "Laptop with HiDPI screen", "Laptop with MDPI screen", "Laptop with touch", "Microsoft Lumia 550",
              "Microsoft Lumia 950", "Moto G4", "Nexus 10", "Nexus 4", "Nexus 5", "Nexus 5X", "Nexus 6", "Nexus 6P",
              "Nexus 7", "Nokia Lumia 520", "Nokia N9", "iPad Mini", "iPhone 4", "JioPhone 2", "Galaxy S5",
              "Pixel 2", "Pixel 2 XL", "iPhone 5/SE", "iPhone 6/7/8", "iPhone 6/7/8 Plus", "iPhone X", "iPad",
              "iPad Pro", "Surface Duo", "Galaxy Fold"]


# 模拟登录微博
def login_weibo(username, password):
    # 创建Chrome浏览器实例
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 开发者模式
    chrome_options.add_argument('--ignore-certificate-errors')  # 开发者模式
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    # chrome_options.add_argument('--proxy-server={}'.format(ip))  # 添加代理
    # chrome_options.add_argument('--headless')  # 无界面
    chrome_options.add_argument('--disable-infobars')  # 关闭操控提示
    chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在报错问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU硬件加速。如果软件渲染器没有就位，则GPU进程将不会启动。
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    chrome_options.add_experimental_option("prefs", prefs)  # 禁用css和图片
    device_name = mobileName[random.randint(0, len(mobileName) - 1)]
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": device_name})  # 模拟手机类型
    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    print(type(browser))
    return
    # 打开微博登录页面
    browser.get('https://passport.weibo.cn/signin/login')

    # 输入账号密码
    username_input = browser.find_element(By.ID, 'loginName')
    password_input = browser.find_element(By.ID, 'loginPassword')
    username_input.send_keys(username)
    password_input.send_keys(password)

    # 点击登录按钮
    login_button = browser.find_element(By.ID, 'loginAction')
    login_button.click()

    # 等待页面加载完成
    # time.sleep(5)
    browser.find_element(By.XPATH, '//*[@id="vdVerify"]/div[1]/div/div/div[3]/a').click()
    yzm = input("请输入验证码")
    browser.find_element(By.XPATH, '//*[@id="verifyCode"]//input').send_keys(yzm)
    browser.find_element(By.XPATH, '//*[@id="verifyCode"]/div[1]/div/div/div[3]/a').click()
    browser.get('https://m.weibo.cn/compose/')
    time.sleep(3)
    td = datetime.today()
    try:
        browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/main/div[1]/div/span/textarea[1]').send_keys("没事发个微博[吃瓜],看看现在什么时间"+str(td.date())+" "+str(td.time()))
    except:
        print("....")
    # 返回浏览器实例
    browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/header/div[3]/a').click()
    input("结束")
    return browser


# 调用登录函数
browser = login_weibo('15727583826', 'wb123456')

# 关闭浏览器
browser.quit()
