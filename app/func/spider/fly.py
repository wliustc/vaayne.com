# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/23 08:17
from gevent.monkey import patch_all
patch_all()
from gevent.pool import Pool
from .spider import Spider, log
from bs4 import BeautifulSoup


class FlyerTea(Spider):
    def __init__(self):
        self.log = log
        self.category = u'信用卡'
        self.spider_name = u'flyertea'
        # self.api_list = 'http://www.flyertea.com/source/plugin/mobile/mobile.php?' \
        #                 'module=portal&version=4&mod=list&catid=124&ctype=card&page=1'
        # self.article_api = 'http://www.flyertea.com/newcomment/index.php/Api/Article/detail.html?' \
        #                    'aid=9237&p=1&page_size=20'

    def article_list(self, url):
        r = self.req(url)
        items = r.json().get('Variables').get('article')
        aids = list(map(lambda x: x.get('aid'), items))
        return aids

    def article(self, aid):
        url = 'http://www.flyertea.com/newcomment/index.php/Api/Article/detail.html?aid=%s&p=1&page_size=20' % aid
        if self.repeat_check(url):
            return
        self.insert_redis(url)
        try:
            r = self.req(url)
            data = r.json().get('data')
            title = data.get('title')
            author = data.get('author')
            post_time = data.get('dateline')
            source_url = 'http://www.flyertea.com/article-%s-1.html' % aid
            summary = data.get('summary')
            content = data.get('content').encode('utf-8')
            try:
                content = self.get_img(BeautifulSoup(content, 'lxml'), 'src').encode('utf-8')
            except Exception as e:
                print (e)
            aid = aid
            image = data.get('face')
            # self.add_result(title=title, author=author, post_time=post_time, source_name=self.spider_name,
            #                 source_url=source_url, summary=summary,
            #                 content=content, image=image, category=self.category, aid=aid)
            self.add_result(title=title, author=author, post_time=post_time, source_name=u'飞客茶馆',
                            source_url=source_url, summary=summary, spider_name=self.spider_name,
                            content=content, image=image, category=self.category, aid=aid)
        except Exception as e:
            self.log.error(e)

    def run(self, page):
        p = Pool(16)
        for i in range(int(page)):
            url = 'http://www.flyertea.com/source/plugin/mobile/mobile.php?' \
                  'module=portal&version=4&mod=list&catid=124&ctype=card&page=%s' % i
            self.log.info('Crawl page %s' % i)
            aids = self.article_list(url)
            p.map(self.article, aids)
            # self.article(aids[0])
            # for aid in aids:
            #     try:
            #         self.article(aid)
            #     except Exception as e:
            #         self.log.warn(e)
            #         continue
