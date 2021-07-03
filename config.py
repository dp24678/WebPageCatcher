# # _*_coding:utf-8 _*_
#
#
# # 开启调试
# # DEBUG=True
# # 数据库相关配置信息  MySQL
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from apscheduler.jobstores.redis import RedisJobStore
#
# MYSQL_HOST = '127.0.0.1'
# MYSQL_PORT = 3306
# MYSQL_USER_NAME = 'root'
# MYSQL_PASSWORD = '12345'
# MYSQL_DB_NAME = 'hengxing'
#
# MYSQL_GOODS_DATA_BASE_TBL_NAME = 'goods_data_id_'  # 商品数据表基名
# MYSQL_TBL_NAME_TBTM = 'goods_data_tb_tm'
# MYSQL_TBL_NAME_JD = 'goods_data_jd'
#
# # 格式： mysql://登录名:密码@ip:port/数据库名字
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:%s/%s"%(MYSQL_USER_NAME,MYSQL_PASSWORD,MYSQL_HOST, MYSQL_PORT,MYSQL_DB_NAME)
# # SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://%s:%s@%s:%s/%s"%(MYSQL_USER_NAME,MYSQL_PASSWORD,MYSQL_HOST, MYSQL_PORT,MYSQL_DB_NAME)
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# # SQLALCHEMY_TRACK_MODIFICATIONS 如果设置成True(默认情况)，Flask - SQLAlchemy
# # 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
# compare_type = True,  # 检查字段类型
# compare_server_default = True,  # 比较默认值
#
# SECRET_KEY = 'oiuYROUIHJBAFAJKBUWYEUI'
#
#
#
#
# redis 数据库配置
REDIS_HOST = "127.0.0.1"   # 主机名
REDIS_PORT = 6379          # 端口
REDIS_ENCODING = "utf8"   # 编码

REDIS_KEY_TASK_QUEUE = 'GNCookiePool'  # cookie存储地址
#
# # 定时任务相关配置
# SCAN_TASK_INTERVAL = 10   # 任务表扫描时间间隔 单位：秒
#
# # apscheduler 配置信息
# APS_SCHEDULER_CONFIG = {
#      'jobstores': {  # 作业存储相关配置
#          # 'default': {'type': 'redis', 'url': 'redis://127.0.0.1:6379/5'},
#          'redis': RedisJobStore(),
#      },
#      'executors': {
#         'default': ThreadPoolExecutor(10),#默认线程数
#         'processpool': ProcessPoolExecutor(3)#默认进程
#     },
#      'job_defaults': {
#          'coalesce': True,  # 积攒的任务只跑一次
#          'max_instances':1000,  # 支持1000个实例并发
#          'misfire_grace_time':600  # 600秒的任务超时容错
#      },
#      'timezone': 'Asia/Shanghai'  # 使用时区
#  }
#
#


MAX_WSE = 2  # 启动几个浏览器
WSE_DICT = {}  # 存储browserWSEndpoint
defult_expire_redis = 3600*2  # redis 插入數據的默認有效期

# 允许截图的图片格式 默认使用第一种 png
SCREENSHOT_FILE_TYPES = ['png', 'jpg', 'webp']

# 代理服务器
proxyHost = "http-pro.abuyun.com"
proxyPort = "9010"

# 代理隧道验证信息
proxyUser = "HZ436081551J93WP"
proxyPass = "DD62E4196E698C80"

proxyServer = "http://" + proxyHost + ":" + proxyPort
