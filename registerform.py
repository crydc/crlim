from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('用户名不能为空'),Length(max=10,min=6,message='用户名长度为6-10')])
    pwd = PasswordField('Password', validators=[DataRequired('密码不能为空'),Length(max=10,min=6,message='密码长度为6-10')])
    sub = SubmitField('注册')