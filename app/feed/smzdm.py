# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/30 17:32 

from . import feed, gen_rss, create_response
from ..api import smzdm


@feed.route('/smzdm')
def smzdm_rss():
    smzdm.insert_sql()
    rss = gen_rss('spider_name', 'smzdm')
    return create_response(rss)
