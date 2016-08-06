# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/28 15:53 

from ... import init_log
from flask import Blueprint

auth = Blueprint('auth', __name__)
log = init_log(__name__)

from . import form, views, user
