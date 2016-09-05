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
    def __init__(self):
        super().__init__()

    # def get_basic_info(self, info, i_type):
    #     self.log.info("Start ... %s" % info)
    #     if i_type == 1:
    #         self.url = info
    #         item = self.db.wx_source.find_one({'iwgc_link': info})
    #         print(item)
    #         self.aid = item['id']
    #         self.author = item['name']
    #     elif i_type == 2:
    #         self.author = info[0]
    #         self.aid = info[1]
    #         self.url = info[2]
    #     else:
    #         raise Exception("初始化错误,请输入URL或者其他信息!")

    def get_articles(self, url, page=2):
        for i in range(1, page):
            url_ = '%s/p/%s' % (url, i)
            self.log.info('Now is page %s, %s' % (i, url_))
            r = self.req_get(url_)
            q = self.pq(r.text)
            items = q('.panel-body div a')
            if len(items) == 0:
                self.log.info("There are total %s page" % i)
                return
            for item in items.items():
                self.parse(item, url)

    def parse(self, item, url):
        title = item('h2:first').text()
        post_time = self.parse_time(item('span:first').text())
        summary = item('p:first').text()
        source_url = self.get_real_url('http://www.iwgc.cn' + item('a').attr('href'))
        source_url = self.parse_url(source_url)
        info = self.db.wx_source.find_one({'iwgc_link': url})
        aid = info['id']
        author = info['name']
        if self.repeat_check(source_url):
            return
        self.log.info("Start crawl %s" % source_url)
        content, image = self.get_content(source_url)
        self.add_result(title=title, author=author, post_time=post_time, source_name=author,
                        source_url=source_url, summary=summary, spider_name=self.spider_name,
                        content=content, image=image, category=self.category, aid=aid)

    def get_real_url(self, url):
        r = self.req_get(url)
        real_url = re_real_url.search(r.text).group(1)
        return real_url

    @staticmethod
    def parse_time(time_str):
        t = ct.search(time_str).group(0)
        return Arrow.strptime(t, '%Y-%m-%d %H:%M:%S', tzinfo='Asia/Shanghai').timestamp

    def run_(self, url):
        try:
            self.get_articles(url)
        except Exception as e:
            self.log.exception(e)
