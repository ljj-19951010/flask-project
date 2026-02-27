"""
视图
url
"""
from flask import Blueprint, render_template, request, session, make_response, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
from App.exts import db
from App.forms import LoginForm, RegisterForm
from App.models import Article, Carousel, Friendlink, Category, User, Comment
from App.verifycode import vc

blog = Blueprint('blog', __name__)


@blog.route("/")
@login_required     # 用户如果没有登录不能访问首页
def index():
    # 获取文章列表，根据时间排序
    articles = Article.query.order_by(-Article.pub_date).all()[:8]
    # 获取录播图,根据pos排序
    imgs = Carousel.query.order_by(Carousel.pos).all()
    # 原创作品
    myself_articles = Article.query.filter(Article.iscreator==1).order_by(-Article.hits).all()[:5]
    # 获取推荐文章
    great_articles = Article.query.order_by(-Article.hits).all()[:5]
    # 友情链接
    friend_links = Friendlink.query.order_by(Friendlink.orderyno).all()
    # 获取用户
    user = User.query.order_by(User.id).all()[-1]
    return render_template('home.html', **locals())


@blog.route("/list/")
@login_required
def list_view():
    num = func.count(Article.tid)       # 根据文章tid，计算每个tid对应的文章总数量
    category_list = db.session.query(Article.cid, Category.name, num, Category.orderno).filter(Article.cid == Category.cid).group_by(Article.cid).order_by(Category.orderno).all()  # 根据文章的外键cid查询类别中分类的名称

    cid = category_list[0][0]
    order = int(request.values.get('order', 1))
    # 查询分类文章
    page = int(request.values.get('page', 1))
    if order == 1:
        pagination = Article.query.filter(Article.cid==cid).order_by(Article.pub_date).paginate(page=page, per_page=10)
    elif order == 2:
        pagination = Article.query.filter(Article.cid==cid).order_by(-Article.hits).paginate(page=page, per_page=10)
    else:
        pagination = Article.query.filter(Article.cid==cid).order_by(Article.replycount).paginate(page=page, per_page=10)

    return render_template('list.html', **locals())


@blog.route("/list/<int:cid>/")
@login_required
def group_articles(cid):
    num = func.count(Article.tid)  # 根据文章tid，计算每个tid对应的文章总数量
    category_list = db.session.query(Article.cid, Category.name, num, Category.orderno).filter(Article.cid == Category.cid).group_by(Article.cid).order_by(Category.orderno).all()  # 根据文章的外键cid查询类别中分类的名称
    print(category_list)
    # 查询分类文章
    order = int(request.values.get('order', 1))
    page = int(request.values.get('page', 1))
    if order == 1:
        pagination = Article.query.filter(Article.cid == cid).order_by(Article.pub_date).paginate(page=page,per_page=10)
    elif order == 2:
        pagination = Article.query.filter(Article.cid == cid).order_by(-Article.hits).paginate(page=page, per_page=10)
    else:
        pagination = Article.query.filter(Article.cid == cid).order_by(Article.replycount).paginate(page=page,per_page=10)
    return render_template('list.html', **locals())


@blog.route("/content/")
@blog.route("/content/<int:tid>/")
@login_required
def content(tid=0):
    if tid == 0:
        article = Article.query.first()
    else:
        article = Article.query.filter(Article.tid == tid).first()
    # 侧边栏分类
    num = func.count(Article.tid)  # 根据文章tid，计算每个tid对应的文章总数量
    category_list = db.session.query(Article.cid, Category.name, num, Category.orderno).filter(Article.cid == Category.cid).group_by(Article.cid).order_by(Category.orderno).all()
    # print(category_list)
    return render_template('content.html', **locals())


@blog.route("/verifycode/")
def verifycode():
    code = vc.generate()
    session['code'] = vc.code       # 验证码字符串保存到session里
    response = make_response(code)
    response.headers['Content-Type'] = 'image/png'
    return response


@blog.route("/login/", methods=['GET', 'POST'])
def login_view():
    form = LoginForm(request.form)
    tid = int(request.values.get('tid', 0))
    print(tid)
    if request.method == 'POST':
        if form.validate_on_submit():       # 验证成功返回true
            # 获取验证后的数据
            username = form.username.data
            password = form.password.data
            user = User.query.filter(User.username == username).first()
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(f'/content/{tid}')
    return render_template('login.html', **locals())


@blog.route("/register/", methods=['GET', 'POST'])
def register_view():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = generate_password_hash(form.password.data)
            email = form.email.data
            user = User(username=username, password=password, email=email)
            user.save()
            return redirect(url_for('blog.login_view'))
    print(form.errors)
    return render_template('register.html', **locals())


@blog.route("/logout/")
def logout_view():
    logout_user()
    return redirect(url_for('blog.login_view'))


# 评论提交
@blog.route("/mark/", methods=['POST'])
def mark_view():
    if request.method == 'POST':
        data = request.values.get("comment")
        tid = int(request.values.get("tid", 0))
        comment = Comment(tid=tid, content=data, uid=current_user.id)
        comment.save()
        return redirect(f"/content/{tid}")


# 搜索
@blog.route("/search/", methods=['POST', 'GET'])
@login_required
def search_view():
    num = func.count(Article.tid)  # 根据文章tid，计算每个tid对应的文章总数量
    category_list = db.session.query(Article.cid, Category.name, num, Category.orderno).filter(Article.cid == Category.cid).group_by(Article.cid).order_by(Category.orderno).all()  # 根据文章的外键cid查询类别中分类的名称
    # print(category_list)
    keywords = request.values.get('kw', '')
    order = int(request.values.get('order', 1))
    page = int(request.values.get('page', 1))
    if order == 1:
        pagination = Article.query.filter(Article.title.contains(keywords)).order_by(Article.pub_date).paginate(page=page, per_page=10)
    elif order == 2:
        pagination = Article.query.filter(Article.title.contains(keywords)).order_by(-Article.hits).paginate(page=page, per_page=10)
    else:
        pagination = Article.query.filter(Article.title.contains(keywords)).order_by(Article.replycount).paginate(page=page, per_page=10)
    return render_template('search.html', **locals())
