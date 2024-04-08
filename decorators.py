from functools import wraps
from flask import redirect, url_for, g, abort, flash

# 创建login_required修饰器
def login_required(func):
    """
    login_required接受一个函数作为参数，通过全局变量g有无user属性，判断用户是否登录
    若登录就重定向到登陆页面，否则就按照正常流程执行被装饰的函数
    """
    @wraps(func)
    def inner(*args, **kwargs):
        if not hasattr(g, "user"):
            return redirect(url_for("user.login"))
        elif not g.user.is_active:
            flash("该用户已被禁用！")
            return redirect(url_for("user.login"))
        else:
            return func(*args, **kwargs)
    return inner


def permission_required(permission):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if hasattr(g, "user") and g.user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return abort(403)
        return inner
    return outer
