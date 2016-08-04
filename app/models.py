# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/21 09:42 

import hashlib
from . import dba

diac = {
    'username': 'Vaayne',
    'email': 'lyishaou@gmail.com',
    'password': 'Passwd',
    'hash_passwd': '1a7dcac1e378896ddaefd39463c4f600'
}

hass = hashlib.md5('Passwd').hexdigest()


class Post(dba.Document):
    title = dba.StringField()
    post_id = dba.IntField(),
    aid = dba.StringField(),
    post_time = dba.StringField(),
    author = dba.StringField(),
    source_name = dba.StringField(),
    spider_name = dba.StringField(),
    source_url = dba.StringField(),
    summary = dba.StringField(),
    content = dba.StringField(),
    image = dba.StringField(),
    category = dba.StringField(),
    slug = dba.StringField(),
    content_type = dba.StringField()


class CursorWrapper(object):

    """Wraps the MongoDB cursor to work with the paginate module."""

    def __init__(self, cur):
        self.cur = cur

    __iter__ = lambda self: self.cur.__iter__()
    __len__ = lambda self: self.cur.count()
    __getitem__ = lambda self, key: self.cur.__getitem__(key)

