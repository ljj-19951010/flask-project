"""
用于后端验证账户
表单
"""

from flask import session
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

from App.models import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired("用户名必须输入!")])
    password = PasswordField('password', validators=[DataRequired("密码必须输入!"), Length(min=6, message="密码最少6位")])
    # 验证码
    code = StringField('code', validators=[DataRequired("验证码必须输入!")])

    # 验证用户名
    def validate_username(self, field):
        value = field.data
        username = User.query.filter(User.username==value).first()
        if not username:
            raise ValidationError("用户名不存在!")
        return field

    # 验证码验证
    def validate_code(self, field):
        print(field)
        value = field.data
        code = session.get('code')
        if code != value:
            raise ValidationError("验证码错误!")
        return field


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired("用户名必须输入!"), Length(min=3, message="最少3位")])
    password = PasswordField('password', validators=[DataRequired("密码必须输入!"), Length(min=6, message="最少6位")])
    confirm = PasswordField(validators=[EqualTo('password', message="密码输入不一致!")])
    email = EmailField()

    # 检查用户名是否与数据库相同
    def validate_username(self, field):
        value = field.data
        if User.query.filter(User.username==value).first():
            raise ValidationError("用户名不能重复!")
        return field

    # 检查邮箱是否与数据库相同
    def validate_email(self, field):
        value = field.data
        if User.query.filter(User.email==value).first():
            raise ValidationError('该邮箱已注册！')
        return field
