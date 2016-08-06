# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 20:29 
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from user import User
from ... import db





class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me login in')
    submit = SubmitField('Log In')
    # captcha = RecaptchaField()


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              u'用户名只能包含字母、数字、点.和下划线_')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message=u'密码必须匹配'),
        Regexp('((?=.*\d)(?=.*[a-zA-Z?=.*[@#$%]).{6,20})',
               0, u'密码太弱,请使用字母加数字组合,最好含有特殊字符,长度6-20')
    ])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField()

    def validate_email(self, field):
        print type(field), field
        if db.users.find_one({'email': field.data}):
            raise ValidationError(u'此Email已经注册')

    def validate_username(self, field):
        print type(field), field
        if db.users.find_one({'username': {'$regex': field.data, '$options':"$i"}}):
            raise ValidationError(u'此用户名已存在')

