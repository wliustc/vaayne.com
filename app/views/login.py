# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/01 17:00 

from . import view
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user
from ..forms.form import EmailPasswordForm
from ..forms.user import User
from .. import db
from .. import lm


@view.route('/login', methods=['GET', 'POST'])
def login():
    form = EmailPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = db.users.find_one({'email': form.email.data})
        passwd = db.users.find_one({'password': str(form.password.data)})
        if user is not None and passwd is not None:
            return '<h1>Login Success</h1>'
    #     # user = db.users.find_one({"email": form.email.data})
    #     if user and User.validate_login(user['password'], form.password.data):
    #         user_obj = User(user['_id'])
    #         login_user(user_obj)
    #         flash("Logged in successfully!", category='success')
    #         return redirect(request.args.get("next"))
    #     flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


@lm.user_loader
def load_user(username):
    u = db.users.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])

sorted('14327', reverse=1)