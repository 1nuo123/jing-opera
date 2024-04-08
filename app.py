from flask import Flask
import commands
import config
import hooks
from exts import db, mail, cache,csrf
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from blueprints.media import bp as media_bp
from flask_migrate import Migrate
from work_celery import make_celery
from flask_wtf import CSRFProtect
from models import user

# 实例化Flask对象
app = Flask(__name__)

# 获取config配置文件
app.config.from_object(config.TestingConfig)

# 初始化变量
db.init_app(app)
mail.init_app(app)
cache.init_app(app)
csrf.init_app(app)

# 实例化Celery对象
celery = make_celery(app)

# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)
app.register_blueprint(media_bp)

# 实例化Migrate对象
migrate = Migrate(app, db)

# 添加命令
app.cli.command("create-premission")(commands.create_permission)
app.cli.command("create-role")(commands.create_role)
app.cli.command("create-test-user")(commands.create_test_user)
app.cli.command("create-admin")(commands.create_admin)
app.cli.command("create-board")(commands.create_board)

# CSRF保护
CSRFProtect(app)

# 钩子函数
app.before_request(hooks.bbs_before_request)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=444)
