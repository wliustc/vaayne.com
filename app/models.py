# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/21 09:42 

import hashlib
from . import db


diac = {
    'username': 'Vaayne',
    'email': 'lyishaou@gmail.com',
    'password': 'Passwd',
    'hash_passwd': '1a7dcac1e378896ddaefd39463c4f600'
}

hass = hashlib.md5('Passwd').hexdigest()


class Post(db.Document):
    title = db.StringField()
    post_id = db.IntField(),
    aid = db.StringField(),
    post_time = db.StringField(),
    author = db.StringField(),
    source_name = db.StringField(),
    spider_name = db.StringField(),
    source_url = db.StringField(),
    summary = db.StringField(),
    content = db.StringField(),
    image = db.StringField(),
    category = db.StringField(),
    slug = db.StringField(),
    content_type = db.StringField()




