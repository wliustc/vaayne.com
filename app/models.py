# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/21 09:42 

import datetime
from . import db
from flask_mongokit import Document
# 标题, 作者(微信公众号为公众号名字), 发布时间戳, 文章访问id, 文章配图, 引言, 文章内容, 来源(微信公众号, 少数派,什么值得买等), 源地址, 分类(信用卡,软件等)


class Post(Document):
    structure = {
        'title': unicode,
        'author': unicode,  # 公众号为名字, 其他为作者
        # 'author_link': unicode,  # 点击作者名字跳转的链接
        'aid': unicode,  # 公众号为微信id, 其他为网站内分类
        'post_time': unicode,  # 发布时间, 统一存储为时间戳
        'post_id': int,  # 本站的post_id, 可跳转到文章正文
        'image': unicode,   # 文章概述图
        'summary': unicode,  # 文章概述
        'content': unicode,     # 正文
        'source_name': unicode,  # 来源, 公众号为公众号名字, 其他为网站名字(飞客茶馆, 什么值得买)
        'spider_name': unicode,  # (wx, flyertea, smzdm)
        'source_url': unicode,  # 原文链接
        'category': unicode     # 分类, 微信公众号, 信用卡, 软件等
    }
    required_fields = ['title', 'post_id', 'content']
    default_values = {
        'post_time': datetime.datetime.utcnow()
    }
    use_dot_notation = True


class Role(Document):
    structure = dict(
        id=int,
        name=unicode,
    )
    required_fields = ['name']
    use_dot_notation = True

    def __repr__(self):
        return '<Role %r>' % self.structure.get('name')


class User(Document):
    structure = dict(
        id=int,
        username=unicode,
        password=unicode
    )
    required_fields = ['username', 'password']
    use_dot_notation = True

    def __repr__(self):
        return '<User %r>' % self.structure.get('name')