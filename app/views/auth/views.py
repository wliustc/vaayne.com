# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/06 07:51

from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, current_user
from ... import db
from . import auth
from .form import LoginForm, RegistrationForm
from .user import User
from werkzeug.security import generate_password_hash


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = db.users.find_one({'email': form.email.data})
        if user and User.validate_password(user.get('password_hash'), form.password.data):
            user_obj = User(user.get('email'))
            login_user(user_obj, form.remember_me.data)
            flash("Logged in successfully", category='success')
            return redirect(request.args.get('next') or url_for('view.index', current_user=current_user))
        flash("Wrong username or password", category='error')
    return render_template('login.html', title='login', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('view.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        db.users.insert(
            dict(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
                password_hash=generate_password_hash(form.password.data)
            )
        )
        flash('You can now login.')
        return redirect(url_for('view.index'))
    return render_template('register.html', form=form)
