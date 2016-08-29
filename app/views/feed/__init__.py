# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/29 14:26 

from flask import Blueprint, Response
from pymongo import DESCENDING
from ... import db, init_log
import PyRSS2Gen
import datetime
import xml.etree.cElementTree as ET
from arrow import Arrow
from io import StringIO
import sys

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


# def gen_wx_rss(key, value):
#     log.info('Gen RSS for Wechat')
#     item = db.posts.find_one({key: value})
#     datas = db.posts.find({key: value}).sort('post_time', DESCENDING)
#     items = parse(datas)
#     rss = PyRSS2Gen.RSS2(
#         title=item.get('author'),
#         link=item.get('link'),
#         description=item.get('desc'),
#         lastBuildDate=datetime.datetime.now(),
#         items=items
#     )
#
#     return rss.to_xml(encoding='utf-8')

#
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


def gen_xml(key, value):
    try:
        item = db.posts.find_one({key: {'$regex': value, '$options': 'i'}})
        items = db.posts.find({key: {'$regex': value, '$options': 'i'}}).sort('post_time', DESCENDING)
        return get_xml(item, items)
    except Exception as e:
        log.exception(e)


def write_xml(self, outfile, encoding="iso-8859-1"):
    from xml.sax import saxutils
    handler = saxutils.XMLGenerator(outfile, encoding)
    handler.startDocument()
    self.publish(handler)
    handler.endDocument()


def to_xml(self, encoding="iso-8859-1"):
    f = StringIO()
    self.write_xml(f, encoding)
    return f.getvalue()


def get_xml(item, items):
    root = ET.Element('rss')
    root.attrib = {'version': "2.0"}
    c = ET.SubElement(root, 'channel')
    ET.SubElement(c, 'copyright').text = 'Copyright 2016, Liu Vaayne'
    if item.get('source_name') == 'wx':
        ET.SubElement(c, 'title').text = item.get('author')
    else:
        ET.SubElement(c, 'title').text = item.get('title')
    ET.SubElement(c, 'link').text = item.get('link')
    ET.SubElement(c, 'description').text = item.get('desc')
    ET.SubElement(c, 'lastBuildDate').text = Arrow.now().format('YYYY-MM-DD HH:mm:ss')
    for item in items:
        i = ET.SubElement(c, 'item')
        ET.SubElement(i, 'title').text = item.get('title')
        # ET.SubElement(i, 'image').text = item.get('image')
        # ET.SubElement(i, 'pubDate').text = datetime.datetime.fromtimestamp(int(item.get('post_time')))
        ET.SubElement(i, 'pubDate').text = item.get('post_time').strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(i, 'link').text = item.get('source_url')
        # ET.SubElement(i, 'summary').text = item.get('summary')
        # ET.SubElement(i, 'description').text = item.get('content')
        ET.SubElement(i, 'category').text = item.get('category')
    tree = ET.ElementTree(root)
    f = StringIO()
    tree.write(sys.stdout)
    print f.getvalue()
    return f.getvalue()


def create_response(rss):
    return Response(
        response=rss,
        mimetype="application/xml",
        status=200,
        content_type='text/xml;charset=utf-8',
    )


from . import view

