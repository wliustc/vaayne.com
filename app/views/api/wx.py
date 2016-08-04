# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 11:20 
from gevent.monkey import patch_all
from gevent.pool import Pool
from flask import request, abort
from . import api, create_response, log
from ...func.spider import WX, WxWGC


patch_all()
wx = WX()
wgc = WxWGC()
p = Pool(16)


def insert_sql(symbols):
    log.info('Start update WX articles')
    for symbol in symbols:
        try:
            if not wgc.run(symbol):
                wx.run(symbol)
        except Exception as e:
            print e
            continue


@api.route('/wx')
def wx_api():
    symbols = request.args.get('symbols')
    if symbols is None:
        abort(404)
        return
    symbols = symbols.replace(' ', '').split(',')
    print symbols
    insert_sql(symbols)
    return create_response('aid', symbols)

