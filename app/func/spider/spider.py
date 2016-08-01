# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/18 21:47 

import requests
from pyquery import PyQuery
import logging
from user_agent import generate_user_agent
import re
import hashlib
from redis import StrictRedis
from random import choice
from pymongo import MongoClient, DESCENDING
from datetime import datetime


class Spider(object):
    rds = StrictRedis(host='localhost', port=6379, db=1)
    pq = PyQuery
    db = MongoClient().blog

    # proxy_api = 'http://ent.kuaidaili.com/api/getproxy?orderid=936588863967175&num=100&kps=1&format=json'
    # data = requests.get(proxy_api).json()
    # self.proxy_list = data['data']['proxy_list']

    @staticmethod
    def init_log(log_name):
        log = logging.getLogger(log_name)
        logging.basicConfig(level=logging.INFO, format="%(filename)s %(asctime)s %(levelname)s %(message)s")
        fh = logging.FileHandler(filename=log_name + '.log', mode='w', encoding='utf-8')
        fh.setLevel(level=logging.INFO)
        fh.setFormatter(logging.Formatter("%(filename)s %(asctime)s %(levelname)s %(message)s"))
        log.addHandler(fh)
        return log

    def req(self, url, **kwargs):
        header = {'User-Agent': generate_user_agent()}
        # proxy = {'http': choice(self.proxy_list)}
        # r = requests.get(url, headers=header, proxies=proxy)
        r = requests.get(url, headers=header, **kwargs)
        try:
            charset = re.search(re.compile(r'charset=(.*)'), r.headers.get('Content-Type')).group(1)
        except Exception as e:
            # self.log.warn(url)
            # self.log.warn(e)
            charset = 'utf-8'
        r.encoding = charset
        return r

    def repeat_check(self, source_url):
        hashurl = self.md5_value(source_url)
        # print("Check redis is %s" % hashurl)
        if self.rds.exists(hashurl):
            self.log.info('Alreay crawl %s' % source_url)
            return True
        else:
            self.log.info('Start crawl %s' % source_url)
            return False

    def insert_redis(self, key, slat='repeat_check'):
        # print('Insert in redsi is : %s' % self.md5_value(key))
        self.rds.set(self.md5_value(key), slat)

    @staticmethod
    def md5_value(key):
        return hashlib.md5(key).hexdigest()

    @staticmethod
    def get_img(soup, real):
        img_list = soup.find_all('img')
        for img in img_list:
            # new_tag = soup.new_tag("img")
            # new_tag['src'] = url_for('view.get_img', url=img['data-src'])
            # new_tag['src'] = "http://vaayne.com/img02?url=%s" % img[real]
            # img.replace_with(new_tag)
            img['src'] = "https://vaayne.com/img02?url=%s" % img[real]
        try:
            selects = soup.find_all('select')
            for sel in selects:
                sel.extract()
        except:
            pass
        return soup

    def add_result(self, title, post_time, source_name, source_url, aid=None, summary=None,
                   content=None, author=None, image=None, category=None, spider_name=None, content_type='html'):
        try:
            post_id = self.db.posts.find().sort('post_id', DESCENDING)[0].get('post_id')
            post_id = int(post_id) + 1
        except Exception as e:
            self.log.exception(e)
            post_id = 1
        print (post_id)
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
        try:
            self.db.posts.insert(post)
            self.log.info(u"Insert %s sucess.".encode('utf-8') % title)
            self.insert_redis(source_url)
        except Exception as e:
            # self.log.exception(e)
            self.log.warn(e)
