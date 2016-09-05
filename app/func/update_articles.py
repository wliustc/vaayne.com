# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/01 15:23

from gevent.monkey import patch_all
patch_all()
from .insert_sql import fly_insert_sql, smzdm_insert_sql, wx_insert_sql
from app import db
import gevent
from gevent.pool import Pool


symbols = []
for item in db.wx_source.find():
    symbols.append(item.get('wx_id'))
# symbols = ['bitsea', 'WebNotes', 'yangmaolife', 'BluewingSay', 'sagacity-mac', 'coderstory', 'AstonCAR']


def update_wx():
    p = Pool(100)
    p.map(wx_insert_sql, symbols)


def update():
    gevent.joinall([
        gevent.spawn(update_wx()),
        gevent.spawn(smzdm_insert_sql()),
        gevent.spawn(fly_insert_sql(1))
    ])

