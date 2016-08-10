# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/28 16:59 

from spider import Spider
import requests
import re
import random
import math
from arrow import Arrow
from bs4 import BeautifulSoup
from ...views.get_img import get_img
from flask import url_for

u = re.compile(r'"uuid":"(\w+)"')


class WX(Spider):
    log = Spider().init_log(__name__)
    spider_name = 'wx'
    category = u'微信公众号'

    @staticmethod
    def get_nonce():
        a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
        res = ''
        for i in range(9):
            e = int(math.floor(random.random() * 16))
            res += a[e]
        print res
        return res

    @staticmethod
    def get_uuid(symbol):
        url = 'http://www.newrank.cn/public/info/detail.html?account=%s' % symbol
        r = requests.get(url)
        if r.status_code != 200:
            return
        uid = u.search(r.text).group(1)
        return uid

    @staticmethod
    def parse_url(url):
        p = re.compile('&scene=.*')
        return p.sub('', url, count=1)

    # def get_content(self, url):
    #     r = requests.get(url)
    #     q = self.pq(r.text)
    #     content = q('.rich_media_content').html()
    #     return content

    def get_content(self, url):
        r = self.req(url)
        soup = BeautifulSoup(r.text, 'lxml')
        content = soup.find(class_='rich_media_content')
        try:
            content = self.get_img(content, 'data-src')
            img = content.find('img')['src']
        except:
            img = ''
        return unicode(content), img

    def run(self, symbol):
        uid = self.get_uuid(symbol)
        if uid is None:
            return
        url = 'http://www.newrank.cn/xdnphb/detail/getAccountArticle'
        params = {
            'uuid': uid,
            # 'nonce': '5bfcd1ae8',
            # 'xyz': '991deed649e6af9d3b8693b204729f7e'
        }
        r = requests.post(url, data=params)
        datas = r.json()
        try:
            infos = datas['value']['lastestArticle']
            for info in infos:
                source_url = self.parse_url(info.get('url'))
                if self.repeat_check(source_url):
                    continue
                title = info.get('title')
                wx_id = info.get('account')
                author = info.get('author')
                post_time = info.get('publicTime')
                post_time = Arrow.strptime(post_time, '%Y-%m-%d %H:%M:%S', tzinfo='Asia/Shanghai').timestamp
                summary = info.get('summary')
                content, img = self.get_content(source_url)
                if info.get('imageUrl') is None:
                    image = img
                else:
                    image = info.get('imageUrl')
                # print title, account, author, post_time
                # print summary
                # print source_url
                # print content
                self.add_result(title=title, author=author, post_time=post_time, source_name=author,
                                source_url=source_url, summary=summary, spider_name=self.spider_name,
                                content=content, image=image, category=self.category, aid=wx_id)
        except Exception as e:
            self.log.error(e)
        # return dict(
        #         wx_id=symbol,
        #         author=author,
        #         )




