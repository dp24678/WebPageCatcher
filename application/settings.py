# -*- coding: utf-8 -*-
"""应用配置信息"""



# 代理服务器
import os

proxyHost = "http-pro.abuyun.com"
proxyPort = "9010"

# 代理隧道验证信息
proxyUser = "HZ436081551J93WP"
proxyPass = "DD62E4196E698C80"

proxyServer = "http://" + proxyHost + ":" + proxyPort


MAX_WSE = 2  # 启动几个浏览器

defult_expire_redis = 3600*2  # redis 插入數據的默認有效期


args_launch = [
    '--disable-dev-shm-usage',
    '--no-first-run',
    '--no-zygote',
    '--no-sandbox',  # 禁止沙箱模式
    '--no-default-browser-check',  # 不检查默认浏览器
    '--disable-extensions',
    '--hide-scrollbars',
    '--disable-bundled-ppapi-flash',
    '--mute-audio',
    '--disable-setuid-sandbox',
    '--disable-gpu',
    # "--window-size=500,450",
    '--start-maximized',  # 浏览器启动最大化
    "--disable-infobars"  # 禁止提示 浏览器被驱动的提示信息   # 关闭提示： Chrome 正受到自动测试软件的控制
]
JSON_AS_ASCII = False   # 解决 返回 json时中文乱码问题

# 本地临时存储 截图与pdf文件的目录
TEMPORARY_FILES_PATH = './temporary_files/'
if not os.path.exists(TEMPORARY_FILES_PATH):
    os.mkdir(TEMPORARY_FILES_PATH)


class BaseConfig:
    """
    配置基类,存放公用的配置
    """
    DEBUG = False
    # 加密过程中加盐
    SECRET_KEY = "-:5\xa0w\xfao\xccpJ\x17\xf17\x0f~>\xa9@\xbd\x9b\xd16\xab}"
    JSON_AS_ASCII = False   # 解决 返回 json时中文乱码问题


class ProductionConfig(BaseConfig):
    """
    生产环境配置
    """
    DEBUG = True
    USERNAME = 'root'
    PASSWORD = '12345'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'test'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME, PASSWORD, HOST, PORT,
                                                                                   DATABASE)


class DevelopmentConfig(BaseConfig):
    """
    开发配置
    """
    DEBUG = True
    USERNAME = 'root'
    PASSWORD = '12345'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'test'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME, PASSWORD, HOST, PORT,
                                                                                   DATABASE)


class TestingConfig(BaseConfig):
    """
    测试配置
    """
    USERNAME = 'root'
    PASSWORD = '12345'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'test'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME, PASSWORD, HOST, PORT,
                                                                                   DATABASE)
    WTF_CSRF_ENABLED = False


config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
