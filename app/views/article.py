# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/31 08:52 


from .. import db
from . import view, log
from flask import abort, render_template
from datetime import datetime


@view.route('/article/<int:post_id>')
def article(post_id):
    log.info("Try to find the article.")
    item = db.posts.find_one({'post_id': post_id})
    if item is None:
        abort(404)
    else:
        log.info('Success find article, %s.'.encode('utf-8') % item.get('title'))
        return render_template('article.html', item=item, post_time=datetime.fromtimestamp(int(item.get('post_time'))))

