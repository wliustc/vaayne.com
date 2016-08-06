# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 12:59 


from . import view
from flask import render_template, request
from .. import db
from pymongo import DESCENDING
from flask_login import login_required
from app.func import update_articles


@view.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    items = db.posts.find({'spider_name': 'wx'}).skip(10 * (page - 1)).sort('post_time', DESCENDING).limit(10)
    return render_template('index.html', items=items, page=page)


@view.route('/update')
def update():
    update_articles.update()
    return '<h1>更新数据成功</h1>'


@view.route('/wx/<aid>')
@login_required
def category_wx(aid):
    page = request.args.get('page', 1, type=int)
    items = db.posts.find({'spider_name': 'wx', 'aid': aid}).skip(10 * (page - 1)).sort('post_time', DESCENDING).limit(10)
    return render_template('index.html', items=items, page=page)


@view.route('/category/<kind>')
def category(kind):
    page = request.args.get('page', 1, type=int)
    items = db.posts.find({'spider_name': kind}).skip(10 * (page - 1)).sort('post_time', DESCENDING).limit(10)
    return render_template('index.html', items=items, page=page)
