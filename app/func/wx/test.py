# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/05 21:00
import json
from pymongo import MongoClient

db = MongoClient().blog


def alias():
    with open('content.txt') as f:
        infos = f.readlines()
        items = []
        for info in infos:
            print info.replace('\n', '')
            item = json.loads(info)
            items.append(item.get('Alias'))
        with open('gzh.txt', 'w') as f:
            for item in items:
                f.write(item)
                f.write('\n')


def insert_db():
    with open('gzh.txt', 'r') as f:
        items = f.readlines()
    for item in items:
        item = item.replace('\n', '')
        if item != '':
            print item
            db.wx_source.insert({'wx_id': item})

insert_db()