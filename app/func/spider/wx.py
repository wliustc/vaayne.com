# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/28 16:59 

from app.func.spider import Spider
import requests
import re
from arrow import Arrow
from bs4 import BeautifulSoup


u = re.compile(r'"uuid":"(\w+)"')


class WX(Spider):
    spider_name = 'wx'
    category = u'微信公众号'

    def __init__(self):
        super().__init__()

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

    def get_content(self, url):
        r = self.req_get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        content = soup.find(class_='rich_media_content')
        try:
            content = self.get_img(content, 'data-src')
            img = content.find('img')['src']
        except:
            img = ''
        return content, img

    def run(self, symbol):
        uid = self.get_uuid(symbol)
        if uid is None:
            return
        url = 'http://www.newrank.cn/xdnphb/detail/getAccountArticle'
        params = {
            'uuid': uid,
        }
        r = self.req_post(url, data=params)
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
                self.add_result(title=title, author=author, post_time=post_time, source_name=author,
                                source_url=source_url, summary=summary, spider_name=self.spider_name,
                                content=content, image=image, category=self.category, aid=wx_id)
        except Exception as e:
            self.log.error(e)





