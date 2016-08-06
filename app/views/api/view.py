# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/06 10:16 

# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 11:20
from gevent.monkey import patch_all
patch_all()
from gevent.pool import Pool
from flask import request, abort
from . import api, create_response, log
from ...func.insert_sql import fly_insert_sql, smzdm_insert_sql, wx_insert_sql


@api.route('/flyertea')
def fly_api():
    page = request.args.get('page')
    if page is None:
        page = 10
    fly_insert_sql(page)
    return create_response('spider_name', ['flyertea'])


@api.route('/smzdm')
def smzdm_api():
    smzdm_insert_sql()
    return create_response('spider_name', ['smzdm'])


@api.route('/wx')
def wx_api():
    symbols = request.args.get('symbols')
    if symbols is None:
        abort(404)
        return
    symbols = symbols.replace(' ', '').split(',')
    print symbols
    p = Pool(16)
    p.map(wx_insert_sql, symbols)
    return create_response('aid', symbols)

