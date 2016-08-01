# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/28 17:10 

from flask import render_template
from . import view


@view.route('/view/1')
def test():
    return render_template('index.html')