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

log = logging.getLogger(__file__)
coloredlogs.install(logging.INFO)


def get_urls():
    with open('wx.csv', 'r') as f:
        res = f.readlines()
    urls = list(map(lambda x: x.replace('\n', '').split(',')[0:3], res))
    return urls


def run_wx(info):
    iwgc = WxWGC(info=info)
    iwgc.get_articles()


def run_smzdm():
    sm = Smzdm()
    sm.run()


def run_fly(page):
    fly = FlyerTea()
    fly.run(page=page)


def main():
    path = os.path.abspath(os.getcwd())
    os.chdir(path)
    p = Pool(16)
    if sys.argv[1] == 'wx':
        # urls = get_urls()[0:1]
        urls = [['小道消息', 'WebNotes', 'http://www.iwgc.cn/list/2']]
        p.map(run_wx, urls)
    elif sys.argv[1] == 'fly':
        try:
            page = sys.argv[2]
        except:
            page = 1
        run_fly(page)
    elif sys.argv[1] == 'smzdm':
        run_smzdm()
    else:
        print(sys.argv)


if __name__ == '__main__':
    main()
