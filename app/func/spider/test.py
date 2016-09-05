# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/09/01 14:10 
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
    p = Pool(16)
    if sys.argv[1] == 'wx':
        urls = list(map(lambda x: 'http://www.iwgc.cn/list/%s' % x, [i for i in range(1, 5)]))
        p.map(iwgc.run_, urls)
    elif sys.argv[1] == 'fly':
        try:
            page = sys.argv[2]
        except:
            page = 1
        fly.run(page)
    elif sys.argv[1] == 'smzdm':
        sm.run()
    else:
        print(sys.argv)


if __name__ == '__main__':
    main()
