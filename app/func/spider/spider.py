# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/18 21:47 

import requests
from requests.auth import HTTPProxyAuth
from pyquery import PyQuery
from user_agent import generate_user_agent
import re
import hashlib
from redis import StrictRedis
from random import choice
from pymongo import MongoClient, DESCENDING
from datetime import datetime
from .bloomfilter import BloomFilter
import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(logging.INFO)

proxy_api = 'http://ent.kuaidaili.com/api/getproxy?orderid=936588863967175&num=100&kps=1&format=json'
proxy_list = requests.get(proxy_api).json()['data']['proxy_list']


class Spider(object):
    def __init__(self):
        self.blf = BloomFilter(connection=StrictRedis(host='127.0.0.1', port=6379, db=8, password='9tBJEUr4wbnf'), bitvector_key='bloomfilter')
        self.pq = PyQuery
        self.db = MongoClient().blog
        self.log = logger

    def req_get(self, url, charset='utf-8', **kwargs):
        header = {'User-Agent': generate_user_agent()}
        proxy = {
            'http': choice(proxy_list),
            'https': choice(proxy_list)
        }
        try:
            r = requests.get(url, headers=header, proxies=proxy, auth=HTTPProxyAuth('reg', 'noxqofb0'), **kwargs)
        except Exception as e:
            self.log.warn("使用代理失败,直接连接(%s)" % e)
            r = requests.get(url, headers=header, **kwargs)
        r.encoding = charset
        return r

    def req_post(self, url, charset='utf-8', **kwargs):
        header = {'User-Agent': generate_user_agent()}
        proxy = {
            'http': choice(proxy_list),
            'https': choice(proxy_list)
        }
        try:
            r = requests.post(url, headers=header, proxies=proxy, auth=HTTPProxyAuth('reg', 'noxqofb0'), **kwargs)
        except Exception as e:
            self.log.warn("使用代理失败,直接连接(%s)" % e)
            r = requests.post(url, headers=header, **kwargs)
        r.encoding = charset
        return r

    @staticmethod
    def md5_value(key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        return hashlib.md5(key).hexdigest()

    def repeat_check(self, url):
        if self.blf.exist(url):
            self.log.info("ALready crawl it, %s" % url)
            return True
        self.log.info("Start crawl url %s" % url)
        return False

    def get_img(self, soup, real):
        img_list = soup.find_all('img')
        for img in img_list:
            img['src'] = "https://vaayne.com/img02?url=%s" % img[real]
        try:
            selects = soup.find_all('select')
            for sel in selects:
                sel.extract()
        except Exception as e:
            self.log.exception(e)
        try:
            return str(soup.find('div').encode('utf-8'), 'utf-8')
        except AttributeError:
            return str(soup.encode('utf-8'), 'utf-8')

    def add_result(self, title, post_time, source_name, source_url, aid=None, summary=None,
                   content=None, author=None, image=None, category=None, spider_name=None, content_type='html'):
        try:
            post_id = self.db.posts.find().sort('post_id', DESCENDING)[0].get('post_id')
            post_id = int(post_id) + 1
        except Exception as e:
            self.log.exception(e)
            post_id = 1
        print(post_id)
        post = dict(
            post_id=int(post_id),
            aid=aid,
            title=title,
            post_time=datetime.fromtimestamp(int(post_time)),
            author=author,
            source_name=source_name,
            spider_name=spider_name,
            source_url=source_url,
            summary=summary,
            content=content,
            image=image,
            category=category,
            slug=self.md5_value(source_url),
            content_type=content_type
        )
        # print(post)
        try:
            self.db.posts.insert(post)
            self.log.info(u"Insert %s  from %s sucess." % (title, source_name))
            if spider_name == 'wx':
                self.blf.add(source_url)
        except Exception as e:
            self.log.warn(e)
