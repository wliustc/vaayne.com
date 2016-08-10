# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/07 09:03 

from . import view
from flask import Response, url_for


@view.route('/pac/i.pac')
def pac():
    pac_file = file('ftp/i.pac')
    return Response(pac_file, mimetype='.pac')
