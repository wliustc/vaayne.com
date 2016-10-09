# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/28 15:53 
from flask import Blueprint


view = Blueprint('view', __name__,
                 template_folder='templates',
                 static_folder='static'
                 )

from .. import init_log
log = init_log('view')

from . import index, error, get_img, article, search, feed, ss

