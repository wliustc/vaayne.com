# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/09/04 09:49 

from gevent.monkey import patch_all
patch_all()
from gevent.pool import Pool
import logging
import coloredlogs
from .wx_iwgc import WxWGC
from .smzdm import Smzdm
from .fly import FlyerTea
import os
import sys
import time

log = logging.getLogger(__file__)
coloredlogs.install(logging.INFO)

iwgc = WxWGC()
fly = FlyerTea()
sm = Smzdm()


def get_urls():
    with open('wx.csv', 'r') as f:
        res = f.readlines()
    urls = list(map(lambda x: x.replace('\n', '').split(',')[0:3], res))
    return urls


def main():
    path = os.path.abspath(os.getcwd())
    os.chdir(path)
    fly.run(page=1)
    sm.run()
    p = Pool(16)
    urls = list(map(lambda x: 'http://www.iwgc.cn/list/%s' % x, [i for i in range(1, 1001)]))
    p.map(iwgc.run_, urls)


if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as e:
            log.exception(e)
        finally:
            time.sleep(60*60)
