#encoding: utf-8
from flask_wtf import Form
from wtforms import SelectField,StringField
from wtforms.validators import DataRequired,Length

class PasswordForm(Form):
    password = StringField('密码', validators=[DataRequired(), Length(6, 20)])

class LoginForm(PasswordForm):
    email = StringField('邮箱', validators=[DataRequired(),Length(4,64)])

class SettingForm(Form):
    setting = SelectField('设置',coerce=int,validators=[DataRequired()])