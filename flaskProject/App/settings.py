"""
配置文件
1.数据库配置
2.debug
3.test
4.安全密钥
5.本地文件路径
"""
import os


class BaseConfig(object):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/blog'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = 'QWERTYUIOP123456<><>,./,.ASDFGHJKL123456abcdefg'


class TestingConfig(BaseConfig):
    TESTING = True
    SECRET_KEY = 'ABCDEFGabcdefg123456_+()&*&*('


class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = 'QWERTYU4651@!&$#^!(%$!*#32798IOP123456<><>,./,.ASDFGHJABCDasdf12431&(*@$JOIJ(4324EFGabcde234{}|P+_L<:"Z<CPOI@!$Yfg123456_+()&*&*(KL123456abcdefg'


my_config = {
    'default': BaseConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
