# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/01 17:37 

from wtforms.validators import ValidationError


class Unique(object):
    def __init__(self, db, field, message=u'该内容已经存在。'):
        self.db = db.users
        self.field = field
        self.message = message

    def __call__(self, *args, **kwargs):
        check = self.db.find_one({'email': self.field})
        if check:
            raise ValidationError(self.message)

