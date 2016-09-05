# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/09/04 10:31 

from .. import db
from . import view, log
from flask import render_template, Markup
import markdown2


@view.route('/about')
def article():
    log.info("Try to find the About Me.")
    item = db.posts.find_one({'post_id': 'about'})
    content = neomarkdown(item['content'])
    return render_template('about.html', content=content)


@view.template_filter('neomarkdown')
def neomarkdown(markdown_content):
    content = Markup(markdown2.markdown(markdown_content, extras=["tables"]))
    return content
