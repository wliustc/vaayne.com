# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/04 14:53 

from gevent.monkey import patch_all
patch_all()
from gevent.pool import Pool
from .wx import WX
import re
from arrow import Arrow


re_url = re.compile(r'<a href="(/list/\w+)">(.*?)</a>')
re_real_url = re.compile(r"window.location.href = '(.*?)'")
ct = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')


class WxWGC(WX):
    def __init__(self, aid):
        self.aid = aid
        self.author = ''

    def search_id(self, wid):
        url = 'http://www.iwgc.cn/search?q=%s' % wid
        self.log.info('Search for %s' % wid)
        r = self.req(url)
        if not int(re.search(re.compile(r'<h3 class="box-head">.*(\w+)</h3>'), r.text).group(1)):
            self.log.warn(u'微广场没有收录%s' % wid)
            return
        info = re_url.search(r.text)
        url = 'http://www.iwgc.cn' + info.group(1)
        self.aid = wid
        self.author = info.group(2)
        return url

    def get_articles(self, base_url, page):
        for i in range(1, page):
            url = '%s/p/%s' % (base_url, i)
            self.log.info('Now is page %s, %s' % (i, url))
            r = self.req(url)
            q = self.pq(r.text)
            items = q('.panel-body div a')
            if len(items) == 0:
                self.log.info("There are total %s page" % i)
                return
            p = Pool(16)
            p.map(self.parse, items.items())

    def get_real_url(self, url):
        r = self.req(url)
        real_url = re_real_url.search(r.text).group(1)
        return real_url

    @staticmethod
    def parse_time(time_str):
        t = ct.search(time_str).group(0)
        return Arrow.strptime(t, '%Y-%m-%d %H:%M:%S', tzinfo='Asia/Shanghai').timestamp

    def parse(self, item):
        title = item('h2:first').text()
        post_time = self.parse_time(item('span:first').text())
        summary = item('p:first').text()
        source_url = self.get_real_url('http://www.iwgc.cn' + item('a').attr('href'))
        source_url = self.parse_url(source_url)
        if self.repeat_check(source_url):
            return
        content, image = self.get_content(source_url)
        print(title.encode('utf-8'), post_time)
        self.add_result(title=title, author=self.author, post_time=post_time, source_name=self.author,
                        source_url=source_url, summary=summary, spider_name=self.spider_name,
                        content=content, image=image, category=self.category, aid=self.aid)

    def run(self, page):
        try:
            url = self.search_id(self.aid)
            if not url:
                return
            self.get_articles(url, page)
            return True
        except Exception as e:
            self.log.exception(e)
