# -*- coding: utf-8 -*-
import ast
import json
import random
import time
from io import BytesIO
import gzip
from threading import Thread

from seleniumwire.utils import decode
import requests
from flask import Flask, jsonify, request, render_template
from seleniumwire import webdriver
from weibo.more_sql_Run import dbUtil
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime

mobileName = ["BlackBerry Z30", "Blackberry PlayBook", "Galaxy Note 3", "Kindle Fire HDX", "LG Optimus L70",
              "Laptop with HiDPI screen", "Laptop with MDPI screen", "Laptop with touch", "Microsoft Lumia 550",
              "Microsoft Lumia 950", "Moto G4", "Nexus 10", "Nexus 4", "Nexus 5", "Nexus 5X", "Nexus 6", "Nexus 6P",
              "Nexus 7", "Nokia Lumia 520", "Nokia N9", "iPad Mini", "iPhone 4", "JioPhone 2", "Galaxy S5",
              "Pixel 2", "Pixel 2 XL", "iPhone 5/SE", "iPhone 6/7/8", "iPhone 6/7/8 Plus", "iPhone X", "iPad",
              "iPad Pro", "Surface Duo", "Galaxy Fold"]
app = Flask(__name__)
browser_dict = {}


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


def update_cookies_header(username, accountid):
    sql2 = """
                         select header,webcookie,account_id from `weibo`.`login_hold`  where account_id='{}'
                     """.format(accountid)
    data2 = dbUtil.run_sql(sql2)
    if data2:
        print(data2)
        print("update cookie start")
        for data in data2:
            header = data[0]
            headers = ast.literal_eval(header)
            cookie = data[1]
            cookies = eval(cookie)
            accountid = data[2]
            browser = get_webdriver(username)
            browser.get("https://m.weibo.cn/compose/")
            browser.delete_all_cookies()
            browser.headers = headers
            for cookie111 in cookies:
                browser.add_cookie(cookie111)
            browser.get("https://m.weibo.cn")
            cookies = {}
            for item in browser.get_cookies():
                cookies[item["name"]] = item["value"]
            head = {}
            for b_request in browser.requests:
                if b_request.response and '/m.weibo.cn/api/config' in b_request.url:
                    for key in b_request.headers:
                        if key == "sec-ch-ua":
                            head[key] = ''
                            sec_ch_ua = b_request.headers[key]
                            continue
                        if key == "sec-ch-ua-platform":
                            head[key] = 'Windows'
                            continue
                        head[key] = b_request.headers[key]

            webcookies = browser.get_cookies()
            head = json.dumps(head)
            cookies = json.dumps(cookies)
            webcookies = str(webcookies)
            sql2 = """
                                 update `weibo`.`login_hold` set `header`='{}',`cookie`='{}',`webcookie`="{}"  where account_id='{}'
                             """.format(head, cookies, webcookies, accountid)
            print(sql2)
            data2 = dbUtil.run_sql(sql2)
            if data2:
                print("update cookie success")
            close_webdriver(username)


@app.route('/sms_login', methods=['POST'])
def sms_login():
    username = request.json['username']
    sms_code = request.json['sms_code']
    browser = get_webdriver(username)
    browser.find_element(By.XPATH, '//*[@id="verifyCode"]//input').send_keys(sms_code)
    browser.find_element(By.XPATH, '//*[@id="verifyCode"]/div[1]/div/div/div[3]/a').click()
    time.sleep(3)
    cookies = {}
    webcookies = str(browser.get_cookies())
    print(browser.get_cookies())
    for item in browser.get_cookies():
        cookies[item["name"]] = item["value"]
    print("cookies:", cookies)
    headers = {}
    uid = ""
    xsrf_token = ""
    sec_ch_ua = ""
    for b_request in browser.requests:
        if b_request.response and '/m.weibo.cn/api/config' in b_request.url:
            for key in b_request.headers:
                if key == "sec-ch-ua":
                    headers[key] = ''
                    sec_ch_ua = b_request.headers[key]
                    continue
                if key == "sec-ch-ua-platform":
                    headers[key] = 'Windows'
                    continue
                headers[key] = b_request.headers[key]
            # 获取响应体的内容数据
            rp_body = b_request.response.body
            # 获取到的编码为byte数据，需要解码为utf-8，直接解码会报错
            # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte
            # print输出的字节码是以"b’\x1f\x8b\x08"开头的，说明它是gzip压缩过的数据，所以我们要对字节码进行一个解码操作
            buff = BytesIO(rp_body)
            f = gzip.GzipFile(fileobj=buff)
            body = f.read().decode('utf-8')
            print(body)
            uid = json.loads(body).get("data").get("uid")
            xsrf_token = json.loads(body).get("data").get('st')
            break
    print("headers:", headers)
    account_id = select_account_by_username(username)
    if uid:
        old_uid = select_login_hold_by_uid(uid)
        if old_uid:
            update_login_hold_by_uid(uid, json.dumps(headers), json.dumps(cookies), webcookies)
        else:
            add_login_hold(account_id, uid, json.dumps(headers), json.dumps(cookies), xsrf_token, webcookies)
        close_webdriver(username)
        sql3 = """
                UPDATE `weibo`.`account` SET `last_login_status`='success' where `id`='{}'
            """.format(account_id)
        dbUtil.run_sql(sql3)

        return "登录成功"
    else:
        return "登录失败"

    # url = "https://m.weibo.cn/api/statuses/update"
    # data = {
    #     "content": "1.坠入情网：把对方美化的十全十美\n2.付出：不计一切的疯狂付出，乞求得到爱。应该适当拒绝，及时赞美，得体批评，恰当争论，必要鼓励，温柔安慰，有效督促\n3.独立和尊重：尊重对方独立和成长\n真正的爱，永远都是促进对方心智成熟，是一种自我扩展，而非纯粹的自我牺牲，爱是自我完善的意愿",
    #     "st": "e1e7dc",
    #     "_spr": "screen:1536x864"
    # }
    # response = requests.post(url, headers=headers, cookies=cookies, data=data)
    #
    # print(response.text)
    # print(response)
    # return "登录成功"


def select_login_hold_by_uid(uid):
    """
    查询登录信息
    :param uid:
    :return:
    """
    sql = """
        SELECT * FROM `weibo`.`login_hold` WHERE `uid` = '{}' 
    """.format(uid)
    sql_data = dbUtil.run_sql(sql)
    return sql_data


def update_login_hold_by_uid(uid, header, cookie, webcookie):
    """
    更新登录信息
    :param uid:
    :param header:
    :param cookie:
    :return:
    """
    sql = """
        UPDATE `weibo`.`login_hold` SET `header` = '{}', `cookie` = '{}',`webcookie`="{}" WHERE `uid` = '{}'
    """.format(header, cookie, webcookie, uid)
    dbUtil.run_sql(sql)


def add_login_hold(account_id, uid, header, cookie, xsrf_token, webcookies):
    """
    保存登录信息
    :param account_id:
    :param uid:
    :param header:
    :param cookie:
    :param xsrf_token:
    :return:
    """
    sql = """
        INSERT INTO `weibo`.`login_hold`(`account_id`, `uid`, `header`, `cookie`, `xsrf_token` ,`webcookie`) VALUES ('{}', '{}', '{}', '{}','{}', "{}")
    """.format(account_id, uid, header, cookie, xsrf_token, webcookies)
    dbUtil.run_sql(sql)


@app.route('/sms_login_send', methods=['POST'])
def sms_login_send():
    try:
        username = request.json['username']
        password = request.json['password']
        browser = get_webdriver(username)
        # 打开微博登录页面
        browser.get('https://passport.weibo.cn/signin/login')
        # 输入账号密码
        username_input = browser.find_element(By.ID, 'loginName')
        password_input = browser.find_element(By.ID, 'loginPassword')
        username_input.send_keys(username)
        password_input.send_keys(password)
        # return "发送成功"
        # 点击登录按钮
        login_button = browser.find_element(By.ID, 'loginAction')
        login_button.click()
        time.sleep(3)
        browser.find_element(By.XPATH, '//*[@id="vdVerify"]/div[1]/div/div/div[3]/a').click()
        try:
            if "次数已超限" in browser.find_element(By.XPATH, '//*[@id="vdVerify"]/div[1]/div/div/div[3]/span').text:
                return "验证码获取次数已超限，请使用其他方式登录"
        except:
            pass
        return "发送验证码成功"
    except:
        close_webdriver(username)
        return "登录失败，检查账号密码是否正确"


def get_new_time():
    """获取当前时间：%Y-%m-%d %H:%M:%S"""
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("当前时间：", formatted_time)
    return formatted_time


def get_server_time_tomin():
    """获取当前时间：%Y-%m-%d %H:%M"""
    now = datetime.datetime.now()
    formatted_time = datetime.datetime.strftime(now, "%Y-%m-%d %H:%M")
    print("当前时间：", formatted_time)
    return formatted_time


@app.route('/data', methods=['POST'])
def get_data():
    # 处理数据并返回响应
    data = request.json
    processed_data = data
    return jsonify(processed_data)


@app.route('/')
def index():
    my_int = 18
    my_str = 'curry'
    my_list = [1, 5, 4, 3, 2]
    my_dict = {
        'name': 'durant',
        'age': 28
    }

    # render_template方法:渲染模板
    # 参数1: 模板名称  参数n: 传到模板里的数据
    return render_template('iframe_html.html',
                           my_int=my_int,
                           my_str=my_str,
                           my_list=my_list,
                           my_dict=my_dict)


@app.route('/add_account.html')
def add_account_html():
    sql = """
    SELECT type_name FROM `weibo`.`account_type`
    """
    data = dbUtil.run_sql(sql)
    if data:
        data = [type_name[0] for type_name in data]
    account_type_list = data or ["大v账号", "普通账号", "小账号"]
    return render_template('add_account.html', account_type_list=account_type_list)


@app.route('/addproxy', methods=['POST'])
def addproxy():
    ip = request.json['ip']
    port = request.json['port']
    account = request.json['account']
    new_time = get_new_time()
    sql = """
             insert into `weibo`.`proxy` (`ip`,`port`,`account`,`creater_time`,`update_time`) values ('{}','{}','{}','{}','{}')
         """.format(ip, port, account, new_time, new_time)
    dbUtil.run_sql(sql)

    sql2 = """
             select id from `weibo`.`proxy` where `account`='{}'
         """.format(account)
    data = dbUtil.run_sql(sql2)
    proxyid = data[0][0]

    sql3 = """
            UPDATE `weibo`.`account` SET `proxy_id`='{}' where `account`='{}'
        """.format(proxyid, account)
    dbUtil.run_sql(sql3)
    return "200"


@app.route('/add_account_message', methods=['POST'])
def add_account_message():
    print("添加账号开始")
    username = request.json['username']
    if select_account_by_username(username):
        return "账号已存在"
    password = request.json['password']
    account_type = request.json['account_type']
    login_type = request.json['login_type']
    proxyip = request.json['proxyip']
    port = request.json['proxyport']

    account_type_flag = select_account_type_by_name(account_type)
    if not account_type_flag:
        add_account_type(account_type)
    account_type_id = select_account_type_id_by_name(account_type)
    add_account(username, password, account_type_id, login_type, proxyip, port)
    return "添加账号成功"


@app.route('/update_account_message', methods=['POST'])
def update_acount():
    username = request.json['username']
    password = request.json['password']
    account_type = request.json['account_type']
    login_type = request.json['login_type']
    proxyip = request.json['proxyip']
    port = request.json['proxyport']

    account_type_flag = select_account_type_by_name(account_type)
    if not account_type_flag:
        add_account_type(account_type)
    account_type_id = select_account_type_id_by_name(account_type)
    new_time = get_new_time()
    sql = """
            UPDATE `weibo`.`account` SET `password`='{}' , `account_type_id`='{}' , `login_type`='{}' , `updated_at`='{}',`proxyip`='{}',`proxyport`='{}'
           where `account`='{}'
        """.format(password, account_type_id, login_type, new_time, proxyip, port, username)
    dbUtil.run_sql(sql)
    return "修改成功"


@app.route('/update_essay_message', methods=['POST'])
def update_essay_message():
    essay_type = request.json['essay_type']
    title = request.json['title']
    content = request.json['content']

    essay_type_flag = select_article_type_by_name(essay_type)
    if not essay_type_flag:
        add_essay_type(essay_type)
    essayid = select_article_type_id_by_name(essay_type)
    new_time = get_new_time()
    sql = """
            UPDATE `weibo`.`article` SET `article_type_id`='{}' , `content`='{}' , `updated_at`='{}'
           where `article_title`='{}'
        """.format(essayid, content, new_time, title)
    dbUtil.run_sql(sql)
    return "修改成功"


@app.route('/searchByAccountType', methods=['POST'])
def searchByAccountType():
    account_type = request.json['account_type']
    account_type_id = select_account_type_id_by_name(account_type)
    sql = """
        SELECT
            t1.account,
            t1.password,
            t2.type_name,
            t1.login_type,
            if(t1.last_login_status = "success",'正常','需要登录'),
            t1.proxyip,
            t1.proxyport
        FROM
            `weibo`.`account` t1,
            `weibo`.`account_type` t2
        WHERE
            t1.account_type_id = t2.id and t1.`account_type_id`='{}'
    	""".format(account_type_id)

    account_list = dbUtil.run_sql(sql)
    print(account_list)
    list = []

    for da in account_list:
        dict = {}
        dict["accountName"] = da[0] + ""
        dict["password"] = da[1] + ""
        dict["accountType"] = da[2] + ""
        dict["loginType"] = da[3] + ""
        dict["logingStatue"] = da[4] + ""
        if da[5] == None:
            dict["proxyip"] = ""
        else:
            dict["proxyip"] = da[5] + ""

        if da[5] == None:
            dict["proxyport"] = ""
        else:
            dict["proxyport"] = da[6] + ""
        list.append(dict)
    print(json.dumps(list))
    return json.dumps(list)


@app.route('/searchByAccountName', methods=['POST'])
def searchByAccountName():
    account_name = request.json['account_Name']
    sql = """
        SELECT
            t1.account,
            t1.password,
            t2.type_name,
            t1.login_type,
            if(t1.last_login_status = "success",'正常','需要登录'),
            t1.proxyip,
            t1.proxyport
        FROM
            `weibo`.`account` t1,
            `weibo`.`account_type` t2
        WHERE
            t1.account_type_id = t2.id and t1.`account` like '%{}%'
    	""".format(account_name)

    account_list = dbUtil.run_sql(sql)
    print(account_list)
    list = []

    for da in account_list:
        dict = {}
        dict["accountName"] = da[0] + ""
        dict["password"] = da[1] + ""
        dict["accountType"] = da[2] + ""
        dict["loginType"] = da[3] + ""
        dict["logingStatue"] = da[4] + ""
        if da[5] == None:
            dict["proxyip"] = ""
        else:
            dict["proxyip"] = da[5] + ""

        if da[5] == None:
            dict["proxyport"] = ""
        else:
            dict["proxyport"] = da[6] + ""
        list.append(dict)
    print(json.dumps(list))
    return json.dumps(list)


@app.route('/delete_account_message', methods=['POST'])
def delete_acount():
    username = request.json['username']
    sql = """
            DELETE from `weibo`.`account` where `account`='{}'
        """.format(username)
    print(sql)
    dbUtil.run_sql(sql)
    return "删除成功"


@app.route('/delete_essay_message', methods=['POST'])
def delete_essay():
    article_title = request.json['article_title']
    sql = """
            DELETE from `weibo`.`article` where `article_title`='{}'
        """.format(article_title)
    print(sql)
    dbUtil.run_sql(sql)
    return "删除成功"


@app.route('/add_essay_message', methods=['POST'])
def add_essay_message():
    print("添加文章开始")
    essay_title = request.json['essay_title']
    if select_essay_by_article_title(essay_title):
        return "文章标题已存在"
    essay = request.json['essay']
    essay_type = request.json['essay_type']
    essay_type_flag = select_article_type_by_name(essay_type)
    if not essay_type_flag:
        add_essay_type(essay_type)
    article_type_id = select_article_type_id_by_name(essay_type)
    add_article(article_type_id, essay, essay_title)
    return "添加文章成功"


def select_essay_by_article_title(article_title):
    sql = """
        SELECT id FROM `weibo`.`article` WHERE `article_title` = '{}'
    """.format(article_title)
    article_id = dbUtil.run_sql(sql)
    if article_id:
        return article_id[0][0]
    return article_id


def select_account_by_username(username):
    sql = """
        SELECT id FROM `weibo`.`account` where account='{}'
    """.format(username)
    print(sql)
    account_id = dbUtil.run_sql(sql)
    if account_id:
        return account_id[0][0]
    return account_id


def select_article_type_id_by_name(article_type):
    sql = """
            SELECT id FROM `weibo`.`article_type` where type_name='{}'
        """.format(article_type)
    print(sql)
    type_name = dbUtil.run_sql(sql)
    if type_name:
        return type_name[0][0]
    return type_name


def select_account_type_id_by_name(account_type):
    sql = """
            SELECT id FROM `weibo`.`account_type` where type_name='{}'
        """.format(account_type)
    print(sql)
    type_name = dbUtil.run_sql(sql)
    if type_name:
        return type_name[0][0]
    return type_name


def select_account_type_by_name(account_type):
    sql = """
            SELECT type_name FROM `weibo`.`account_type` where type_name='{}'
        """.format(account_type)
    print(sql)
    type_name = dbUtil.run_sql(sql)
    if type_name:
        return type_name[0][0]
    return type_name


def select_article_type_by_name(article_type):
    sql = """
            SELECT type_name FROM `weibo`.`article_type` where type_name='{}'
        """.format(article_type)
    type_name = dbUtil.run_sql(sql)
    if type_name:
        return type_name[0][0]
    return type_name


def add_account_type(account_type):
    # 获取当前时间
    new_time = get_new_time()
    sql = """
            INSERT INTO `weibo`.`account_type`(`type_name`, `creater_time`, `update_time`) VALUES ('{}', '{}', '{}')
        """.format(account_type, new_time, new_time)
    print(sql)
    dbUtil.run_sql(sql)


def add_essay_type(essay_type):
    # 获取当前时间
    new_time = get_new_time()
    sql = """
            INSERT INTO `weibo`.`article_type`(`type_name`, `created_at`, `updated_at`) VALUES ('{}', '{}', '{}')
        """.format(essay_type, new_time, new_time)
    print(sql)
    dbUtil.run_sql(sql)


def add_article(article_type_id, essay, essay_title):
    sql = """
        INSERT INTO `weibo`.`article`(`article_type_id`, `content`, `article_title`) VALUES ('{}', '{}', '{}')
    """.format(article_type_id, essay, essay_title)
    print(sql)
    dbUtil.run_sql(sql)


def add_account(username, password, account_type_id, login_type, proxyip, proxyport):
    sql = """
        INSERT INTO `weibo`.`account`(`account`, `password`, `account_type_id`, `login_type`,`proxyip`,`proxyport`) VALUES ('{}', '{}', '{}', '{}','{}','{}')
    """.format(username, password, account_type_id, login_type, proxyip, proxyport)
    print(sql)
    dbUtil.run_sql(sql)


@app.route('/manage_account.html')
def manage_account():
    # 1.getaccountType
    sql = """
    SELECT type_name FROM `weibo`.`account_type`
    """
    data = dbUtil.run_sql(sql)
    if data:
        data = [type_name[0] for type_name in data]
    account_type_list = data or ["大v账号", "普通账号", "小账号"]

    # 2.getaccountList
    sql = """
    SELECT
        t1.account,
        t1.password,
        t2.type_name,
        t1.login_type,
        if(t1.last_login_status = "success",'正常','需要登录'),
        t3.ip,
        t3.port
    FROM
        `weibo`.`account` t1 LEFT JOIN `weibo`.`proxy` t3 ON t1.proxy_id = t3.id,
        `weibo`.`account_type` t2
    WHERE
        t1.account_type_id = t2.id
	"""
    sql = """
            SELECT
            t1.account,
            t1.password,
            t2.type_name,
            t1.login_type,
            if(t1.last_login_status = "success",'正常','需要登录'),
            t1.proxyip,
            t1.proxyport
        FROM
            `weibo`.`account` t1,
            `weibo`.`account_type` t2
        WHERE
            t1.account_type_id = t2.id
    """
    account_list = dbUtil.run_sql(sql)
    li1 = []
    for da in account_list:
        li = list(da)
        li3 = ["" if i is None else i for i in li]
        li1.append(li3)
    account_list = li1
    if not account_list:
        account_list = [["账号1", "密码1", "小账号", "无需登录"], ["账号2", "密码2", "大账号", "需要登录"], ["账号3", "密码3", "普通账号", "无需登录"]]
    return render_template('manage_account.html', account_list=account_list, account_type_list=account_type_list)


@app.route('/update_manage_account', methods=['POST'])
def update_manage_account():
    # 1.getaccountType
    sql = """
        SELECT type_name FROM `weibo`.`account_type`
        """
    data = dbUtil.run_sql(sql)
    if data:
        data = [type_name[0] for type_name in data]
    account_type_list = data or ["大v账号", "普通账号", "小账号"]

    # 2.getaccountList
    sql = """
        SELECT
            t1.account,
            t1.password,
            t2.type_name,
            t1.login_type,
            if(t1.last_login_status = "success",'正常','需要登录'),
            t1.proxyip,
            t1.proxyport
        FROM
            `weibo`.`account` t1,
            `weibo`.`account_type` t2
        WHERE
            t1.account_type_id = t2.id
    	"""
    account_list = dbUtil.run_sql(sql)
    li1 = []
    for da in account_list:
        li = list(da)
        li3 = ["" if i is None else i for i in li]
        li1.append(li3)
    account_list = li1
    if not account_list:
        account_list = [["账号1", "密码1", "小账号", "无需登录"], ["账号2", "密码2", "大账号", "需要登录"],
                        ["账号3", "密码3", "普通账号", "无需登录"]]
    return render_template('manage_account.html', account_list=account_list, account_type_list=account_type_list)


@app.route('/add_proxy.html')
def add_proxy():
    sql = """
    SELECT type_name FROM `weibo`.`account_type`
    """
    data = dbUtil.run_sql(sql)
    if data:
        data = [type_name[0] for type_name in data]
    account_type_list = data or ["大v账号", "普通账号", "小账号"]
    return render_template('add_proxy.html', account_type_list=account_type_list)

@app.route('/manage_proxy.html')
def manage_proxy():
    return render_template('manage_proxy.html', account_type_list=["大v账号", "普通账号", "小账号"])

@app.route('/add_essay.html')
def add_essay():
    sql = """
    SELECT type_name FROM `weibo`.`article_type`
    """
    data = dbUtil.run_sql(sql)
    if data:
        data = [type_name[0] for type_name in data]
    essay_type_list = data or ["大v账号", "普通账号", "小账号"]
    return render_template('add_essay.html', essay_type_list=essay_type_list)

@app.route('/manage_essay.html')
def manage_essay():
    sql = """
        SELECT type_name FROM `weibo`.`article_type`
        """
    data = dbUtil.run_sql(sql)
    if data:
        data = [type_name[0] for type_name in data]
    article_type_list = data or ["大v账号", "普通账号", "小账号"]

    # 2.getessayList
    sql = """
        SELECT
            t1.article_title,
            t1.content
        FROM
            `weibo`.`article` t1 
        WHERE status='unpublished'
    	"""
    account_essay_list = dbUtil.run_sql(sql)
    print(sql)
    print(account_essay_list)

    return render_template('manage_essay.html', account_essay_list=account_essay_list,
                           article_type_list=article_type_list)


@app.route('/add_task_essay.html')
def add_task_essay():
    sql = """
        SELECT
            account
        FROM
            `weibo`.`account`
        WHERE 
            last_login_status='success'
    	"""
    account_list = dbUtil.run_sql(sql)

    sql = """
        SELECT
            article_title
        FROM
            `weibo`.`article`
        WHERE
            status = 'unpublished'
    	"""
    article_list = dbUtil.run_sql(sql)

    print(account_list)
    return render_template('add_task_essay.html', account_list=account_list, article_list=article_list)


def update_essay_status(article_title):
    """
    通过article_title更改文章状态
    :param article_title:
    :return:
    """
    sql = """
    UPDATE `weibo`.`article` SET `status` = 'scheduled' WHERE `article_title` = '{}'
    """.format(article_title)
    dbUtil.run_sql(sql)


@app.route('/addtaskessay', methods=['POST'])
def addtaskessay():
    task_name = request.json['task_name']   # 任务名称
    selected_values = request.json['selectedValues']    #
    selected_values_essay = request.json['selectedValues_essay']
    execute_begin_time = request.json['execute_begin_time']
    execute_end_time = request.json['execute_end_time']
    mession_type=request.json['mession_type']
    # 解析字符串为datetime对象
    d1 = datetime.datetime.strptime(execute_begin_time, '%Y-%m-%d %H:%M')
    d2 = datetime.datetime.strptime(execute_end_time, '%Y-%m-%d %H:%M')
    # 计算时间差,秒为单位
    seconds = (d2 - d1).total_seconds()
    sjs_sum = 0
    account_list = []
    # 根据时间范围和文章个数得出随机数
    for essay in selected_values_essay:
        if not account_list:
            account_list = selected_values.copy()
        account_index = 0 if len(account_list) == 1 else random.randint(0, len(account_list) - 1)
        sjs = random.randint(int(seconds/len(selected_values_essay)/10*8), int(seconds/len(selected_values_essay)))
        execute_time = str(d1 + datetime.timedelta(seconds=sjs+sjs_sum))[:-3]
        execute_account = account_list[account_index]
        new_time = get_new_time()
        if mession_type=="essay":
            sql = """
                    INSERT INTO `weibo`.`mession`(`account`, `article_title`, `created_at`,`excute_time`,`status`,`task_name`) VALUES ('{}', '{}', '{}','{}','{}','{}')
                """.format(execute_account, essay, new_time, execute_time, "P", task_name)
        elif mession_type=="common":
            print("common")
        else:
            print("star")
        print(sql)
        dbUtil.run_sql(sql)
        update_essay_status(essay)
        account_list.pop(account_index)
        sjs_sum += sjs




    # aclist = "".join(selected_values)
    # essaylist = "".join(selected_values_essay)
    # new_time = get_new_time()
    # format = '%Y-%m-%d %H:%M'
    # datetime_str = datetime.datetime.strptime(execute_begin_time, format)
    #
    # sql = """
    #     INSERT INTO `weibo`.`mession`(`account`, `article_title`, `created_at`,`excute_time`,`status`,`task_name`) VALUES ('{}', '{}', '{}','{}','{}','{}')
    # """.format(aclist, essaylist, new_time, datetime_str, "P", task_name)
    # print(sql)
    # dbUtil.run_sql(sql)
    return "添加成功"


@app.route('/fb_log.html')
def fb_log():
    sql = "SELECT account,DATE_FORMAT(excute_time, '%Y-%m-%d %H:%i'), article_title, `status`,task_name from `mession`"
    joblist = dbUtil.run_sql(sql)
    for job in joblist:
        print(job)
    print(joblist)
    return render_template('fb_log.html', joblist=joblist)


def batch():
    while True:
        sql = "SELECT id,account, article_title, excute_time,`status`,task_name,DATE_FORMAT(excute_time, '%Y-%m-%d %H:%i') from `mession` where `status`='P'"
        joblist = dbUtil.run_sql(sql)
        print(joblist)
        if joblist:
            for mesion in joblist:
                jobid = mesion[0]

                accountList = mesion[1]
                # accountList = accountList[0:len(accountList) - 1]
                # accList = accountList.split("}")
                accList = [accountList]

                essayList = mesion[2]
                # essayList = essayList[0:len(essayList) - 1]
                # essList = essayList.split("}")
                essList = [essayList]

                print("请执行job")
                batchJob(accList, essList, jobid, mesion[3])
        time.sleep(random.randint(41, 59))


def batchJob(accList, essList, jobid, excuteTime):
    try:
        doTxtime = datetime.datetime.strftime(excuteTime, "%Y-%m-%d %H:%M")
        print(doTxtime)
        serverTime = get_server_time_tomin()
        print(serverTime)
        if doTxtime == serverTime:
            for ac in accList:
                sql2 = """
                         select id from `weibo`.`account` where `account`='{}'
                     """.format(ac)
                data = dbUtil.run_sql(sql2)
                accid = data[0][0]
                sql2 = """
                                     select header,cookie from `weibo`.`login_hold` where `account_id`='{}'
                                 """.format(accid)
                data2 = dbUtil.run_sql(sql2)
                header = data2[0][0]
                cookie = data2[0][1]
                if data2:
                    for ess in essList:
                        sql3 = """
                                 select content from `weibo`.`article` where `article_title`='{}'
                             """.format(ess)
                        data = dbUtil.run_sql(sql3)
                        content = data[0][0]
                        try:
                            code = trancation(header, cookie, content)
                            print(code)
                            if code != 200:
                                sql3 = """
                                         update `mession` set `status`='{}' where `id`='{}'
                                     """.format("F", jobid)
                                data = dbUtil.run_sql(sql3)
                                break
                            print("do transacion")
                        except Exception as e:

                            print(e)
                else:
                    continue
            # change the job status
            sql3 = """
                     update `mession` set `status`='{}' where `id`='{}'
                 """.format("S", jobid)
            data = dbUtil.run_sql(sql3)

    except Exception as e:
        print(e)


def trancation(headers, cookies, content):
    try:
        url = "https://m.weibo.cn/api/statuses/update"
        data = {
            "content": content,
            "st": "0f2399",
            "_spr": "screen:1536x864"
        }
        print(headers)
        print(cookies)
        print(content)
        response = requests.post(url, headers=eval(headers), cookies=eval(cookies), data=data)
        print("fa bu wenz hang le 11111111111111111111111")
        print(response.text)
        print(response.status_code)
        return response.status_code
    except Exception as e:
        print("发布失败")
        print(e)


def keepAccountActive():
    while True:
        sql2 = """
                             select account_id from `weibo`.`login_hold`
                         """
        data2 = dbUtil.run_sql(sql2)
        if data2:
            print("keepAccountActive start ")
            for data in data2:
                accountid = data[0]
                sql = """
                    SELECT account FROM `weibo`.`account` where id='{}'
                """.format(accountid)
                print(sql)
                account_id = dbUtil.run_sql(sql)
                account_name = account_id[0][0]
                print(account_name)
                update_cookies_header(account_name, accountid)
        time.sleep(180)

def init_loginholdAndaccountStatus():
    sql = "delete `weibo`.`login_hold`"
    dbUtil.run_sql(sql)
    sql2="update `weibo`.`account` set `last_login_status`='fail'"
    dbUtil.run_sql(sql2)

if __name__ == '__main__':
    init_loginholdAndaccountStatus()
    t = Thread(target=batch)
    t.start()
    t2 = Thread(target=keepAccountActive)
    t2.start()
    app.run(debug=True)
    """
    U:上左，U'上右，
    D:下右，D'下左，
    L:左下，L'左上，
    R:右上，R'右下，
    F:前右，F'前左，
    B:后右，B'后左，
    """
"""
代理和账号合并到一起了
账号管理页面添加了搜索功能
做任务的时候账号掉了 任务丢失
两套不一样的系统不好兼容
账号维持登录时间



任务日志
账号	处理时间	任务状态	            任务名称    任务类型                    详情（）
            待处理、处理完成                 发布文章、点赞、关注、评论     发布：文章名
                                                                    点赞：被点赞账号名称
                                                                    关注：被关注名称
                                                                    评论：评论内容（评论账号）
"""