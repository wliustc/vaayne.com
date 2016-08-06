# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/28 17:44 

from flask import Blueprint, Response
import json
from pymongo import DESCENDING
from ... import db, init_log

api = Blueprint('api', __name__)

log = init_log(__name__)


def get_data_from_sql(key, value):
    log.info('Get %s:%s date from sql' % (key, value))
    datas = []
    items = db.posts.find({key: value}).sort('post_time', DESCENDING).limit(10)
    for item in items:
        item.pop('content')
        item.pop('_id')
        item.pop('spider_name')
        item.pop('slug')

        item['post_time'] = item.get('post_time').strftime('%Y-%m-%d %H:%M:%S')
        datas.append(item)
    return datas


def create_response(key, values):
    datas = {}
    for value in values:
        datas[value] = get_data_from_sql(key, value)
        # datas.append()
    formater = json.dumps({'datas': datas}, ensure_ascii=False).encode('utf-8')
    log.info('Create response success!')
    return Response(
        response=formater,
        mimetype="application/json",
        status=200,
        content_type='text/json;charset=utf-8',
    )

from . import view

