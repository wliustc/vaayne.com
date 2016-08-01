# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 12:59 

from . import view
from flask import render_template


@view.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@view.app_errorhandler(500)
def internet_server_error(e):
    return render_template('500.html'), 500