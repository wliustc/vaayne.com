# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/28 22:41 

from flask import request
from . import api, create_response, log
from ...func.spider import FlyerTea


fly = FlyerTea()


def insert_sql(page):
    log.info('Start update Flyertea articles')
    fly.run(page)


@api.route('/flyertea')
def fly_api():
    page = request.args.get('page')
    if page is None:
        page = 10
    insert_sql(page)
    return create_response('spider_name', ['flyertea'])