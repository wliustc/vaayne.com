# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/04 13:32 

import requests
import re
from pyquery import PyQuery

re_url = re.compile(r'<a href="(/list/\w+)">(.*?)</a>')
re_real_url = re.compile(r"window.location.href = '(.*?)'")


def search_id(wid):
    url = 'http://www.iwgc.cn/search?q=%s' % wid
    r = requests.get(url)
    if not int(re.search(re.compile(r'<h3 class="box-head">.*(\w+)</h3>'), r.text).group(1)):
        return
    info = re.search(re.compile(r'/list/\w+'), r.text)
    url = 'http://www.iwgc.cn' + info.group(1)
    author = info.group(2)
    return url, author


def get_real_url(url):
    r = requests.get(url)
    url = re_real_url.search(r.text).group(1)
    return url


def get_content(url):
    return 'content'


def get_info(self, item):
    title = item('h2:first').text()
    post_time = item('span:first').text()
    summary = item('p:first').text()
    source_url = get_real_url('http://www.iwgc.cn' + item('a').attr('href'))
    content, image = get_content(source_url)
    self.add_result(title=title, author=self.author, post_time=post_time, source_name=self.author,
                    source_url=source_url, summary=summary, spider_name=self.spider_name,
                    content=content, image=image, category=self.category, aid=self.aid)


def get_article_list(url):
    # for i in range(1, 20):
    #     url = '%s/p/%s' % (base_url, i)
    #     print url
    r = requests.get(url)
    q = PyQuery(r.text)
    items = q('.panel-body div a')
    print len(items)
    for item in items.items():
        get_info(item)


def run(wid):
    url, author = search_id(wid)
    print url
    if not url:
        return
    get_article_list(url)


# run('coderstory')
get_article_list('http://www.iwgc.cn/list/1086/p/3')