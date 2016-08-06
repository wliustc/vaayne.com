# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/06 10:20 

from .spider import WX, WxWGC, Smzdm, FlyerTea
from . import log, db

wx = WX()
sm = Smzdm()
fly = FlyerTea()


def fly_insert_sql(page):
    log.info('Start update Flyertea articles')
    fly.run(page)


def smzdm_insert_sql():
    log.info('Start update SMZDM articles')
    sm.run()


def wx_insert_sql(symbol):
    symbol = symbol.encode('utf-8')
    log.info('Start update %s articles' % symbol)
    if db.wx_source.find_one({'wx_id': symbol}):
        log.info('Already add this account, update it from NewRank.')
        wx.run(symbol)
    else:
        log.info('First time to add this account, try get history from iwgc.')
        try:
            wgc = WxWGC(symbol)
            if not wgc.run():
                wx.run(symbol)
        except Exception as e:
            log.exception(e)
