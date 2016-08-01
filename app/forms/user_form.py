# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 20:29 
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class UserForm(Form):
    username = StringField("What's your name?", validators=[DataRequired()])
    email= StringField(validators=[Email()])
    password = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_on_submit(self):
        pass
