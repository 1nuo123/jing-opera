from datetime import timedelta

# 创建配置文件的基类
class BaseConfig:
    SECRET_KEY = "aaaaaaaa"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_CHECK_DEFAULT = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    UPLOAD_IMAGE_PATH = "E:/Python/中国大学生计算机设计大赛/Work/media"
    PER_PAGE_COUNT = 10

# 创建开发的配置环境类，并继承Baseconfig类
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/Beijing_opera?charset=utf8mb4"

# 创建测试的配置环境，并继承Baseconfig类
class TestingConfig(BaseConfig):
    # 数据库的配置变量
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'Beijing_opera'
    USERNAME = 'root'
    PASSWORD = '000000123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "920845341@qq.com"
    MAIL_PASSWORD = "sketsqztvdlsbbgh"
    MAIL_DEFAULT_SENDER = "920845341@qq.com"

    # 缓存配置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_POST = 6379

    # Celery配置
    CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"











