# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/30 17:32 

from flask import request
from . import api, create_response, log
from ..func.spider import Smzdm


sm = Smzdm()


def insert_sql():
    log.info('Start update SMZDM articles')
    sm.run()


@api.route('/smzdm')
def smzdm_api():
    insert_sql()
    return create_response('spider_name', ['smzdm'])
