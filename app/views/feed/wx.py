# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/29 14:28 

from . import feed, create_response, gen_rss
from ..api import wx
from ... import db


@feed.route('/wx/<aid>')
def wx_rss(aid):
    db.wx_source.update({'wx_id': aid}, {'wx_id': aid}, upsert=True)
    wx.insert_sql([aid])
    rss = gen_rss('aid', aid)
    return create_response(rss)



