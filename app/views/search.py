# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/06 19:32 

from .. import db
from ..func import insert_sql
from . import view
from flask import request, abort, render_template, flash, url_for
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import current_user


class SearchForm(Form):
    aid = StringField('aid', validators=[DataRequired()])
    submit = SubmitField('搜索')


def try_find(aid):
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
        print items
        return render_template('search.html', items=items)
    else:
        insert_sql.wx_insert_sql(aid)
        items = try_find(aid)
        if len(items):
            print items
            return render_template('search.html', items=items)
        else:
            abort(404)


@view.route('/search')
def search():
    form = SearchForm()
    if form.validate_on_submit():
        aid = form.aid.data
        return url_for('view.search_result', aid=aid)
    flash(u'搜索不能为空')



