# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/01 17:37 

from werkzeug.security import check_password_hash, generate_password_hash
from ... import db, lm


@lm.user_loader
def load_user(email):
    u = db.users.find_one({'email': email})
    if not u:
        return
    return User(u['email'])


class User(object):

    def __init__(self, email):
        self.email = email
        self.password_hash = ''

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def validate_password(password_hash, password):
        return check_password_hash(password_hash, password)
