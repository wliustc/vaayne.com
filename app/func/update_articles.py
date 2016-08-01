# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/01 15:23

from gevent.monkey import patch_all
patch_all()
from ..api import fly, smzdm, wx

import gevent

symbols = ['bitsea', 'WebNotes', 'yangmaolife', 'BluewingSay', 'sagacity-mac', 'coderstory']


def update():
    gevent.joinall([
        gevent.spawn(wx.insert_sql(symbols)),
        gevent.spawn(smzdm.insert_sql()),
        gevent.spawn(fly.insert_sql(1))
    ])

