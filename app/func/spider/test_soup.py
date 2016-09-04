# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/09/03 22:37 
import requests
from bs4 import BeautifulSoup


def get_img(soup, real):
    img_list = soup.find_all('img')
    for img in img_list:
        img['src'] = "https://vaayne.com/img02?url=%s" % img[real]
    # print(type(soup))
    # print(soup.prettify())
    # return soup.find('div')
    try:
        return str(soup.find('div').encode('utf-8'), 'utf-8')
    except AttributeError:
        return str(soup.encode('utf-8'), 'utf-8')

url = 'http://mp.weixin.qq.com/s?__biz=MjM5ODIyMTE0MA==&mid=2650968628&idx=1&sn=31fcf37fc80b1c82f44d5f71430e0023&' \
      'chksm=bd38360f8a4fbf1965646b3cd068c6794a365c1d81ae2c2c2faefc479b73bbe26e53ba388015&scene=0#rd'
# url = 'http://www.smzdm.com/p/6386100/'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'lxml')
soup = soup.find(id='js_content')
# print(soup.prettify())

# data = r.json().get('data')
# content = data.get('article_filter_content')
# # print(content)
#
# soup = BeautifulSoup('<div>%s</div>' % content, 'lxml')

# print(type(soup))
# print(soup.prettify())

content = get_img(soup, 'src')
print(type(content))
print(content)
