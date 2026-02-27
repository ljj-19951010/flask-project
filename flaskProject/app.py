"""
执行
"""
from flask_script import Manager
from App.untils import create_app

app = create_app()
manager = Manager(app)


if __name__ == '__main__':
    """
    新版flask shell输入flask run --debug ,由于该文件名为app.py所以可以直接运行，如果名字不为app则需要加上文件名字运行， debug表示打开测试模式
    旧版直接shell输入 python app.py runserver -d -p5000运行， -d表示ip -p表示端口，都可以自己指定，如果指定ip0.0.0.0 表示任意服务器都可以访问
    """
    manager.run()
