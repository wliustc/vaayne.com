# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 12:59 


from . import view
from flask import render_template, request
from .. import db
from pymongo import DESCENDING
from flask_login import login_required, LoginManager
from app.func import update_articles, insert_sql
from app.func.del_wx import d_wx


@view.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    items = db.posts.find({'spider_name': 'wx'}).skip(10 * (page - 1)).sort('post_time', DESCENDING).limit(10)
    return render_template('index.html', items=items, page=page)


@view.route('/update')
def update():
    update_articles.update()
    return '<h1>更新数据成功</h1>'


@view.route('/wx/del')
@login_required
def del_wx():
    aids = request.args.get('id')
    for aid in aids.split(','):
        d_wx(aid)
    return '<h1>Success del</h1>'


@view.route('/wx/<aid>')
@login_required
def category_wx(aid):
    if not request.args.get('page') or request.args.get('page') == 1:
        insert_sql.wx_insert_sql(aid)
    page = request.args.get('page', 1, type=int)
    items = db.posts.find({'spider_name': 'wx', 'aid': aid}).skip(10 * (page - 1)).sort('post_time', DESCENDING).limit(10)
    title = db.posts.find_one({'spider_name': 'wx', 'aid': aid}).get('source_name')
    return render_template('category_wx.html', items=items, page=page, aid=aid, title=title)


@view.route('/category/<kind>')
def category(kind):
    if not request.args.get('page') or request.args.get('page') == 1:
        if kind == 'smzdm':
            insert_sql.smzdm_insert_sql()
        elif kind == 'flyertea':
            insert_sql.fly_insert_sql(1)
    page = request.args.get('page', 1, type=int)
    items = db.posts.find({'spider_name': kind}).skip(10 * (page - 1)).sort('post_time', DESCENDING).limit(10)
    title = db.posts.find_one({'spider_name': kind}).get('source_name')
    return render_template('category.html', items=items, page=page, kind=kind, title=title)
