# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/04 14:53
from gevent.monkey import patch_all
patch_all()
from gevent.pool import Pool
from app.func.spider.wx import WX
import re
from arrow import Arrow


re_url = re.compile(r'<a href="(/list/\w+)">(.*?)</a>')
re_real_url = re.compile(r"window.location.href = '(.*?)'")
ct = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')


class WxWGC(WX):
    def __init__(self, info=None,  url=None):
        super().__init__()
        if url is not None:
            self.url = url
            self.aid = ''
            self.author = ''
        elif info:
            self.author = info[0]
            self.aid = info[1]
            self.url = info[2]
        else:
            raise Exception("初始化错误,请输入URL或者其他信息!")

    def get_articles(self, page=2):
        for i in range(1, page):
            url = '%s/p/%s' % (self.url, i)
            self.log.info('Now is page %s, %s' % (i, url))
            r = self.req_get(url)
            q = self.pq(r.text)
            items = q('.panel-body div a')
            if len(items) == 0:
                self.log.info("There are total %s page" % i)
                return
            p = Pool(1)
            p.map(self.parse, items.items())

    def parse(self, item):
        title = item('h2:first').text()
        post_time = self.parse_time(item('span:first').text())
        summary = item('p:first').text()
        source_url = self.get_real_url('http://www.iwgc.cn' + item('a').attr('href'))
        source_url = self.parse_url(source_url)
        if self.blf.exist(source_url):
            self.log.info("Already crawl it!")
            return
        self.log.info("Start crawl %s" % source_url)
        content, image = self.get_content(source_url)
        self.add_result(title=title, author=self.author, post_time=post_time, source_name=self.author,
                        source_url=source_url, summary=summary, spider_name=self.spider_name,
                        content=content, image=image, category=self.category, aid=self.aid)

    def get_real_url(self, url):
        r = self.req_get(url)
        real_url = re_real_url.search(r.text).group(1)
        return real_url

    @staticmethod
    def parse_time(time_str):
        t = ct.search(time_str).group(0)
        return Arrow.strptime(t, '%Y-%m-%d %H:%M:%S', tzinfo='Asia/Shanghai').timestamp


