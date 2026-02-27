# coding: utf-8
import datetime
from flask_login import UserMixin

from App.exts import db, login_manager

datetime_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


class DBbase(object):
    # 添加一条记录
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False

    # 添加更多记录
    @classmethod
    def save_many(cls, *args):
        try:
            db.session.add_all(*args)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False

    # 删除
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False

class Article(db.Model):
    __tablename__ = 'articles'

    tid = db.Column(db.Integer, primary_key=True, info='序号')
    cid = db.Column(db.ForeignKey('category.cid', ondelete='CASCADE', onupdate='RESTRICT'), index=True, info='分类id')
    description = db.Column(db.String(300, 'utf8_general_ci'), info='简介')
    title = db.Column(db.String(255, 'utf8_general_ci'), nullable=False, info='标题')
    content = db.Column(db.String(collation='utf8_general_ci'), info='内容')
    author = db.Column(db.String(255, 'utf8_general_ci'), info='作者')
    pub_date = db.Column(db.DateTime, nullable=False)
    replycount = db.Column(db.Integer, server_default=db.FetchedValue(), info='回复数')
    hits = db.Column(db.Integer, server_default=db.FetchedValue(), info='点击数')
    isdeleted = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除')
    isreply = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否可以回复')
    iscreator = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否原创')
    isrecommend = db.Column(db.Integer, info='是否推荐')

    category = db.relationship('Category', primaryjoin='Article.cid == Category.cid', backref='articles')
    # user = db.relationship('User', primaryjoin='Article.cid == User.id', backref='articles')



class Carousel(db.Model):
    __tablename__ = 'carousel'

    cid = db.Column(db.Integer, primary_key=True, info='唯一编号')
    path = db.Column(db.String(1000, 'utf8_general_ci'), nullable=False, info='图片路径')
    pos = db.Column(db.String(255, 'utf8_general_ci'), info='排序位置')



class Category(db.Model):
    __tablename__ = 'category'

    cid = db.Column(db.Integer, primary_key=True, info='分类编号')
    name = db.Column(db.String(255, 'utf8_general_ci'), nullable=False, unique=True, info='分类名称')
    num = db.Column(db.Integer, server_default=db.FetchedValue(), info='文章数量')
    orderno = db.Column(db.Integer, info='排序位置')



class Comment(db.Model, DBbase):
    __tablename__ = 'comments'

    rid = db.Column(db.Integer, primary_key=True, info='评论编号')
    content = db.Column(db.String(1000, 'utf8_general_ci'), info='评论内容')
    replydate = db.Column(db.DateTime, default=datetime_now, info='回复时间')
    uid = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='RESTRICT'), index=True, info='用户编号')
    tid = db.Column(db.ForeignKey('articles.tid', ondelete='CASCADE', onupdate='RESTRICT'), index=True, info='文章编号')

    article = db.relationship('Article', primaryjoin='Comment.tid == Article.tid', backref='comments')
    user = db.relationship('User', primaryjoin='Comment.uid == User.id', backref='comments')



class Friendlink(db.Model):
    __tablename__ = 'friendlink'

    fid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255, 'utf8_general_ci'), nullable=False)
    link = db.Column(db.String(255, 'utf8_general_ci'), nullable=False)
    orderyno = db.Column(db.Integer)



class Label(db.Model):
    __tablename__ = 'labels'

    lid = db.Column(db.Integer, primary_key=True, info='标签id')
    name = db.Column(db.String(255, 'utf8_general_ci'), info='标签名')
    description = db.Column(db.String(255, 'utf8_general_ci'), info='标签描述')
    tid = db.Column(db.ForeignKey('articles.tid', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True, info='文章id')

    article = db.relationship('Article', primaryjoin='Label.tid == Article.tid', backref='labels')



class User(DBbase, UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, info='用户id', autoincrement=True)
    username = db.Column(db.String(150, 'utf8_general_ci'), nullable=False, unique=True, info='用户名')
    password = db.Column(db.String(128, 'utf8_general_ci'), nullable=False, info='密码')
    portrait = db.Column(db.String(255, 'utf8_general_ci'), info='头像地址')
    last_login = db.Column(db.DateTime, info='上次登录', default=datetime_now)
    is_superuser = db.Column(db.Integer, info='是否是超级用户')
    email = db.Column(db.String(254, 'utf8_general_ci'), info='邮箱')
    is_active = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否激活')
    date_joined = db.Column(db.DateTime, info='注册日期', default=datetime_now)
    position = db.Column(db.String(255, 'utf8_general_ci'), info='职业')
    address = db.Column(db.String(255, 'utf8_general_ci'), info='家庭地址')
    skill = db.Column(db.String(255, 'utf8_general_ci'), info='技能')


# 实现回调
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
