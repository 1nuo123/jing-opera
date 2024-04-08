from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache
from flask_wtf import CSRFProtect

# 该文件的创建是为了避免其他文件跟app.py相互调用而产生的循环调用问题，并实例化一些必要的对象
db = SQLAlchemy()
mail = Mail()
cache = Cache()
csrf = CSRFProtect()