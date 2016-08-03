# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 20:29 
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from validators import Unique
from ... import db


class EmailPasswordForm(Form):
    email = StringField(validators=[DataRequired(), Email()])
    password = StringField(validators=[DataRequired()])
    # captcha = RecaptchaField()

