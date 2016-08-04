# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 11:20
from gevent.monkey import patch_all
patch_all()
from gevent.pool import Pool
from flask import request, abort
from . import api, create_response, log
from ...func.spider import WX, WxWGC


wx = WX()



def insert_sql(symbol):
    log.info('Start update %s articles' % symbol)
    try:
        wgc = WxWGC(symbol)
        if not wgc.run():
            wx.run(symbol)
    except Exception as e:
        log.exception(e)


@api.route('/wx')
def wx_api():
    symbols = request.args.get('symbols')
    if symbols is None:
        abort(404)
        return
    symbols = symbols.replace(' ', '').split(',')
    print symbols
    p = Pool(16)
    p.map(insert_sql, symbols)
    return create_response('aid', symbols)

