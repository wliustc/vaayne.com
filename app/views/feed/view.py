# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/06 10:14 

from app.func.insert_sql import wx_insert_sql, fly_insert_sql, smzdm_insert_sql
from ... import db
from . import feed, gen_rss, create_response
from flask import request


@feed.route('/flyertea')
def fly_rss():
    page = request.args.get('page')
    if page is None:
        page = 1
    fly_insert_sql(page)
    rss = gen_rss('spider_name', 'flyertea')
    return create_response(rss)


@feed.route('/wx/<aid>')
def wx_rss(aid):
    # db.wx_source.update({'wx_id': aid}, {'wx_id': aid}, upsert=True)
    wx_insert_sql(aid)
    rss = gen_rss('aid', aid)
    return create_response(rss)


@feed.route('/smzdm')
def smzdm_rss():
    smzdm_insert_sql()
    rss = gen_rss('spider_name', 'smzdm')
    return create_response(rss)
