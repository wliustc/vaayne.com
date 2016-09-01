# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/09/01 14:10 
from gevent.monkey import patch_all
patch_all()
from gevent.pool import Pool
import logging
import coloredlogs
from wx_iwgc import WxWGC

log = logging.getLogger(__file__)
coloredlogs.install(logging.INFO)


def get_urls():
    with open('wx.csv', 'r') as f:
        res = f.readlines()
    urls = list(map(lambda x: x.replace('\n', '').split(',')[0:3], res))
    return urls


def run(info):
    iwgc = WxWGC(info=info)
    iwgc.get_articles()


def main():
    p = Pool(16)
    urls = get_urls()[0:1]
    p.map(run, urls)

if __name__ == '__main__':
    main()