# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/30 23:39 

from . import view
from flask import request, Response
import requests


@view.route('/img02')
def get_img():
    url = request.args.get('url')
    r = requests.get(url)
    return Response(
        response=r.content,
        # mimetype="application/json",
        status=200,
        content_type='image/png',
    )
