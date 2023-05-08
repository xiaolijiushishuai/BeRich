# 导包
import os
import threading

import pymysql


# 创建类
class dbUtil:
    __lock = threading.Lock()  # 创建锁
    # 创建conn私有属性
    __conn = None
    # 创建cursor私有属性
    __cursor = None
    # 是否有锁
    __flag = 0

    # 定义创建sql连接的私有方法
    @classmethod
    def __get_connect(cls, host="127.0.0.1",
                      port=3306,
                      user="root",
                      password="123456",
                      db="weibo",
                      ssl={'ca': 'apsaradb-ca-chain.pem', 'check_hostname': False}):
        """
        创建sql连接
        :param host: 地址
        :type host: str
        :param port: 端口
        :type port: int
        :param user: 账号
        :type user: str
        :param password:密码
        :type password: str
        :param db: 数据库名称
        :type db: str
        :return: Connection
        :rtype: Connection
        """
        # host = "39.101.136.192"
        # db = "huaxin_chuangx_n"
        # port = 3306
        # user = "huaxin_chuangx_n"
        # password = "hEKE3JRx5TJf7Rir"
        # 获取当前文件目录名
        path = os.path.dirname(__file__)
        if path not in ssl.get("ca"):
            # 拼接证书的存放地址
            ssl["ca"] = path + "\\" + ssl.get("ca")
        if cls.__conn is None:
            cls.__conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)
        return cls.__conn

    # 定义创建游标的私有方法
    @classmethod
    def __get_cursor(cls):
        if cls.__cursor is None:
            cls.__cursor = cls.__get_connect().cursor()
        else:
            try:
                cls.__conn.ping(reconnect=True)  # cping 校验连接是否异常
            except Exception as e:
                print(e, "----------------------------------pymysql.ping()--------------57----------------------")
                cls.__conn = None
                cls.__cursor = None
                cls.__cursor = cls.__get_connect().cursor()
        return cls.__cursor

    # 定义执行单条sql的方法
    @classmethod
    def run_sql(cls, sql):
        """
        执行sql语句
        :param sql: sql语句
        :type sql: str
        :return: 查询结果或者受影响的数据条数
        :rtype:
        """
        # 捕捉异常，防止脏数据
        try:
            cls.__lock.acquire()  # 申请锁也就是加锁
            cls.__flag += 1
            # 获取游标对象
            cursor = cls.__get_cursor()
            # 执行多条sql语句 execute执行一条
            cursor.execute(sql)
            # 判断是否为查询语句 lstrip():去除最左边的空格 split():按指定符号切割成数组 lower(): 字符串转小写
            if sql.split()[0].lower() == 'select':
                # print("查询语句")
                # 是查询语句，返回查询结果
                return cursor.fetchall()
            else:
                # 不是查询语句，需要提交事务
                cls.__conn.commit()
                # 返回受影响的数据条数
                return cursor.rowcount
        except Exception as e:
            # 执行sql出现异常，回滚数据
            print(e, "--------------------------run_sql----------------92---------------", sql)
            # cls.__conn.rollback()
            cls.__conn = None
            cls.__cursor = None
            cls.__lock.release()
            cls.__get_cursor()
            if cls.__flag < 4:
                cls.run_sql(sql)
            else:
                cls.__flag = 0
            return e
        finally:
            cls.__conn.commit()
            # 关闭光标
            cls.close_cursor()
            # 关闭连接
            # cls.close_conn()
            if cls.__flag:
                cls.__lock.release()  # 释放锁
                cls.__flag = 0

    # 定义执行多条sql的方法
    @classmethod
    def run_sql_execute(cls, sql, *arr):
        """
        一条sql运行多个数据
        :param sql: sql语句
        :type sql: str


        :param arr: 数据
        :type arr: tuple list
        :return:
        :rtype:
        """
        # 捕捉异常，防止脏数据
        try:
            cls.__lock.acquire()  # 申请锁也就是加锁
            # 获取游标对象
            cursor = cls.__get_cursor()
            # 执行多条sql语句 execute执行一条
            cursor.executemany(sql, *arr)
            print(sql)
            # 判断是否为查询语句 lstrip():去除最左边的空格 split():按指定符号切割成数组 lower(): 字符串转小写
            if sql.split()[0].lower() == 'select':
                print("查询语句")
                # 是查询语句，返回查询结果
                return cursor.fetchall()
            else:
                print("不是查询语句")
                # 不是查询语句，需要提交事务
                cls.__conn.commit()
                # 返回受影响的数据条数
                return cursor.rowcount
        except Exception as e:
            # 执行sql出现异常，回滚数据
            print(e)
            cls.__conn.rollback()
            return e
        finally:
            cls.__conn.commit()
            # 关闭光标
            cls.close_cursor()
            # 关闭连接
            # cls.close_conn()
            cls.__lock.release()  # 释放锁

    @classmethod
    def close_cursor(cls):
        if cls.__cursor is not None:
            cls.__cursor.close()
            cls.__cursor = None

    @classmethod
    def close_conn(cls):
        if cls.__conn is not None:
            cls.__conn.close()
            cls.__conn = None
