# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/29 14:26

from flask import Blueprint, Response
from pymongo import DESCENDING
from ... import db, init_log
import PyRSS2Gen
import datetime

feed = Blueprint('feed', __name__)
log = init_log(__name__)


def parse(datas):
    items = []
    for data in datas:
        try:
            item = PyRSS2Gen.RSSItem(
                title=data.get('title'),
                link=data.get('source_url'),
                description=data.get('content'),
                pubDate=data.get('post_time'),
                # categories=data.get('category'),
                # author=data.get('author')
                # image=data.get('image')
                # title=None,  # string
                # link=None,  # url as string
                # description=None,  # string
                # author=None,  # email address as string
                # categories=None,  # list of string or Category
                # comments=None,  # url as string
                # enclosure=None,  # an Enclosure
                # guid=None,  # a unique string
                # pubDate=None,  # a datetime
                # source=None,  # a Source
            )
            items.append(item)
        except Exception as e:
            log.error(e)
            continue
    return items


def gen_rss(key, value):
    log.info('Gen RSS for %s: %s' % (key, value))
    item = db.posts.find_one({key: {'$regex': value, '$options': 'i'}})
    try:
        if item.get('source_name') == 'wx':
            title = item.get('author')
        else:
            title = item.get('source_name')
    except Exception as e:
        log.error(e)
        return
    datas = db.posts.find({key: {'$regex': value, '$options': 'i'}}).sort('post_time', DESCENDING)
    items = parse(datas)
    rss = PyRSS2Gen.RSS2(
        title=title,
        link=item.get('link'),
        description=item.get('desc'),
        lastBuildDate=datetime.datetime.now(),
        items=items
    )
    return rss.to_xml(encoding='utf-8')


def create_response(rss):
    return Response(
        response=rss,
        mimetype="application/rss+xml",
        status=200,
        content_type='text/xml;charset=utf-8',
    )


from . import view
