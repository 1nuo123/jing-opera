from flask import Blueprint, render_template, request, redirect, url_for, flash,session,g
import random, string
from flask_mail import Message
from exts import mail, cache, db
from flask import current_app
from utils import restful
from forms.user import RegisterForm,LoginForm
from models.user import UserModel
from werkzeug.security import generate_password_hash

# 创建蓝图
bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    """
    注册视图函数
    先判断GET请求还是POST请求，GET请求则渲染注册页面
    POST请求则获取表单信息，若验证表单成功将数据保存到数据库，失败则返回错误并重定向到注册界面
    """
    if request.method == 'GET':
        return render_template("front/register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for("user.register"))


@bp.route("/email/captcha")
def email_captcha():
    """
    邮箱验证码视图函数
    该函数实现了用celery任务的方式发送邮箱验证码，使其高效运行
    """
    try:
        # 获取用户输入的email
        email = request.args.get("email")
        source = string.digits * 4
        captcha = random.sample(source, 4)
        captcha = "".join(captcha)
        subject = '注册验证码'
        body = f'您的注册验证码是:{captcha},为保证您的个人信息安全，请勿告诉其他人!'
        current_app.celery.send_task("send_email", (email, subject, body))
        cache.set(email, captcha, timeout=100)
        return restful.ok()
    except Exception as e:
        print(e)
        return restful.server_error()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录视图函数
    先判断GET请求还是POST请求，GET请求则渲染登录页面
    POST请求则获取表单信息，若验证表单成功将数据保存到数据库并存储到session中，失败则返回错误并重定向到登录界面
    """
    if request.method == 'GET':
        return render_template("front/login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = UserModel.query.filter_by(email=email).first()
            if user and user.check_password(password):
                if not user.is_active:
                    flash("该用户已被禁用！")
                    return redirect(url_for("user.login"))
                session['user_id'] = user.id
                if remember:
                    session.permanent = True
                return redirect("/")
            else:
                flash("邮箱或者密码错误！")
                return redirect(url_for("user.login"))
        else:
            for message in form.messages:
                flash(message)
            return render_template("front/login.html")


@bp.get("/profile/<string:user_id>")
def profile(user_id):
    user = UserModel.query.get(user_id)
    is_mine = False
    if hasattr(g, "user") and g.user.id == user_id:
        is_mine = True
    context = {
        "user" : user,
        "user_id" : user_id
    }
    return render_template("front/profile.html",user=user)


@bp.get("/logout")
def logout():
    session.clear()
    return redirect("/")