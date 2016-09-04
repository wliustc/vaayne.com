# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/19 13:54 

from gevent.monkey import patch_all
patch_all()
import gevent
from .spider import Spider
from arrow import Arrow
from bs4 import BeautifulSoup


class Smzdm(Spider):
    def __init__(self):
        super().__init__()
        self.spider_name = 'smzdm'
        self.category = '信用卡'
        self.kinds = ['news', 'jingyan', 'show', 'youhui', 'haitao', 'faxian']
        self.urls_api = 'https://api.smzdm.com/v1/%s/articles?search=信用卡'
        self.article_api = 'http://api.smzdm.com/v1/jingyan/articles/%s' % 'id'

    def get_aids(self, url):
        datas = self.req_get(url).json().get('data').get('rows')
        aids = list(map(lambda x: x.get('article_id'), datas))
        summarys = list(map(lambda x: x.get('article_filter_content'), datas))
        return aids, summarys

    def parse(self, kind, aid, summary):
        url = 'http://api.smzdm.com/v1/%s/articles/%s' % (kind, aid)
        if self.blf.exist(url):
            return
        self.blf.add(url)
        try:
            r = self.req_get(url)
            data = r.json().get('data')
            title = data.get('article_title')
            author = data.get('article_referrals')
            post_time = data.get('article_date')
            post_time = Arrow.strptime(post_time, '%Y-%m-%d %H:%M:%S', tzinfo='Asia/Shanghai').timestamp
            source_url = data.get('article_url')
            # summary = data.get('summary')
            content = data.get('article_filter_content')
            try:
                content = self.get_img(BeautifulSoup('<div>%s</div>' % content, 'lxml'), 'src')
            except Exception as e:
                self.log.exception(e)
            image = data.get('article_pic')
            # self.add_result(title=title, author=author, post_time=post_time, source_name=self.spider_name,
            #                 source_url=source_url, summary=summary,
            #                 content=content, image=image, category=self.category, aid=kind)
            self.add_result(title=title, author=author, post_time=post_time, source_name='什么值得买',
                            source_url=source_url, summary=summary, spider_name=self.spider_name,
                            content=content, image=image, category=self.category, aid=kind)
        except Exception as e:
            self.log.error(e)

    def run(self):
        for kind in self.kinds:
            url = 'https://api.smzdm.com/v1/%s/articles?search=信用卡' % kind
            try:
                aids, summarys = self.get_aids(url)
            except Exception as e:
                self.log.error(e)
                return
            threads = []
            for i in range(len(aids)):
                threads.append(gevent.spawn(self.parse(kind, aids[i], summarys[i])))
            gevent.joinall(threads)
