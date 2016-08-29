# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/06 19:32 

from .. import db
from ..func import insert_sql
from . import view
from flask import request, abort, render_template, flash, url_for
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from . import log


class SearchForm(Form):
    aid = StringField('aid', validators=[DataRequired()])
    submit = SubmitField('搜索')


def try_find(aid):
    log.info(u'Try to find %s in wx_source'.encode('utf-8') % aid)
    items = db.wx_source.find({'$or': [
        {'wx_name': {'$regex': aid, '$options': 'i'}},
        {'wx_id': {'$regex': aid, '$options': 'i'}}
    ]})
    return list(items)


@view.route('/search')
def search_result():
    aid = request.args.get('aid')
    items = try_find(aid)
    if len(items):
        log.info('Success find %s, Show results.' % aid)
        return render_template('search.html', items=items)
    else:
        log.info('Try to find %s not success, Try to crawl it from web.')
        insert_sql.wx_insert_sql(aid)
        items = try_find(aid)
        if len(items):
            log.info('Success find %s, Show results.' % aid)
            return render_template('search.html', items=items)
        else:
            log.warn('Try search %s failed, show 404' % aid)
            abort(404)


@view.route('/search')
def search():
    form = SearchForm()
    if form.validate_on_submit():
        aid = form.aid.data
        return url_for('view.search_result', aid=aid)
    flash(u'搜索不能为空')



