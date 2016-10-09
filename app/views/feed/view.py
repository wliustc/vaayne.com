# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/06 10:14 

from . import feed, gen_rss, create_response


@feed.route('/flyertea')
def fly_rss():
    rss = gen_rss('spider_name', 'flyertea')
    return create_response(rss)


@feed.route('/wx/<aid>')
def wx_rss(aid):
    rss = gen_rss('aid', aid)
    return create_response(rss)


@feed.route('/smzdm')
def smzdm_rss():
    rss = gen_rss('spider_name', 'smzdm')
    return create_response(rss)
