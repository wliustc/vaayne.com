# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 12:59 


from . import view
from flask import render_template
from .. import db
from pymongo import DESCENDING


@view.route('/')
def index():
    items = db.posts.find().sort('post_time', DESCENDING).limit(10)
    return render_template('index.html', items=items)


