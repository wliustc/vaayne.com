# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/29 14:28 

from . import feed, gen_xml, create_response, gen_rss
from ..api import wx


@feed.route('/wx/<aid>')
def wx_rss(aid):
    wx.insert_sql([aid])
    rss = gen_rss('aid', aid)
    return create_response(rss)



