from flask import Blueprint, request, render_template,redirect, jsonify, current_app, url_for, send_from_directory, g,flash
from flask_paginate import Pagination
from decorators import login_required
from forms.post import PublicPostForm,PublicCommentForm
from models.post import BoardModel, PostModel, CommentModel
from exts import db, csrf
from utils import restful
from werkzeug.utils import secure_filename
import os,re

# 创建蓝图
bp = Blueprint("front", __name__, url_prefix="")


@bp.route('/')
def index():
    """
    首页试图函数
    """
    return render_template("front/index.html")


@bp.route('/blog')
def blog():
    """
    博客试图函数
    """
    # 获取所有板块数据
    boards = BoardModel.query.all()

    # 获取页码参数
    page = request.args.get("page", type=int, default=1)

    # 获取板块参数
    board_id = request.args.get("board_id", type=int, default=0)

    # 当前page下的起始位置
    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
    # 当前page下的结束位置
    end = start + current_app.config.get("PER_PAGE_COUNT")

    # 查询对象
    query_obj = PostModel.query.order_by(PostModel.create_time.desc())

    # 过滤帖子
    if board_id:
        query_obj = query_obj.filter_by(board_id=board_id)

    # 总共有多少帖子
    total = query_obj.count()

    # 当前page下的帖子列表
    posts = query_obj.slice(start, end)

    # 分页对象
    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    # 创建context字典类型变量，用于传递关键字参数
    context = {
        "posts": posts,
        "boards": boards,
        "pagination": pagination,
        "current_board": board_id
    }
    return render_template("front/blog.html", **context)


@bp.route("/post/public", methods=['GET', 'POST'])
@login_required
def public_post():
    """
    发表帖子的视图函数
    先判断GET请求还是POST请求，GET请求则渲染发表帖子的页面
    POST请求则获取表单信息，若验证表单成功将数据保存到数据库，失败则返回错误
    """
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template("front/public_post.html", boards=boards)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            print(content)
            post = PostModel(title=title, content=content, board_id=board_id, author=g.user)
            db.session.add(post)
            db.session.commit()
            return restful.ok()
        else:
            message = form.messages[0]
            return restful.params_error(message=message)


@bp.route("/upload/image",methods=['GET','POST'])
@csrf.exempt
@login_required
def upload_image():
    if request.method == 'GET':
        return 'OK'

    else:
        f = request.files.get('image')
        extension = f.filename.split('.')[-1].lower()
        if extension not in ['jpg', 'gif', 'png', 'jpeg']:
            return jsonify({
                "errno": 400,
                "data": []
            })
        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"), filename))
        url = url_for('media.media_file', filename=filename)
        return jsonify({
            "errno": 0,
            "data": [{
                "url": url,
                "alt": "",
                "href": ""
            }]
        })


@bp.route("/post/detail/<int:post_id>")
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    post.read_count += 1
    db.session.commit()
    return render_template("front/post_detail.html",post=post)


@bp.post("/post/<int:post_id>/comment")
@login_required
def public_comment(post_id):
    form = PublicCommentForm(request.form)
    if form.validate():
        content = form.content.data
        comment = CommentModel(content=content,post_id=post_id,author=g.user)
        db.session.add(comment)
        db.session.commit()
    else:
        for message in form.messages:
            flash(message)
    return redirect(url_for("front.post_detail",post_id=post_id))


@bp.route("/lianpu")
def lianpu():
    return render_template("front/lianpu.html")


@bp.route("/sheng")
def sheng():
    return render_template("front/sheng.html")


@bp.route("/dan")
def dan():
    return render_template("front/dan.html")


@bp.route("/jing")
def jing():
    return render_template("front/jing.html")


@bp.route("/chou")
def chou():
    return render_template("front/chou.html")

@bp.route("/jumu")
def jumu():
    return render_template("front/jumu.html")