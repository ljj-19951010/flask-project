"""
初始化
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def init_app(app):
    db.init_app(app)
    login_manager.init_app(app)


login_manager.login_view = 'blog.login_view'
login_manager.login_message = '你还没有登录，请先登录'
