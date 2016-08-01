# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/29 15:13 


from . import feed, gen_rss, create_response
from ..api import fly
from flask import request


@feed.route('/flyertea')
def fly_rss():
    page = request.args.get('page')
    if page is None:
        page = 1
    fly.insert_sql(page)
    rss = gen_rss('source_name', 'flyertea')
    return create_response(rss)
