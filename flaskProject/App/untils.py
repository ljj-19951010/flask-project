"""
创建app
"""
import os.path

from flask import Flask

from App import settings
from App.exts import init_app
from App.settings import my_config
from App.views import blog


def create_app():
    base_dir = settings.BaseConfig.BASE_DIR
    # 目录不对无法访问html
    app = Flask(__name__,
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))
    app.config.from_object(my_config.get('development'))        # 导入配置
    app.register_blueprint(blog)        # 注册蓝图
    init_app(app)
    return app
