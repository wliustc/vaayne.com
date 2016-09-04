# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/09/03 20:21 

import pymongo
from redis import StrictRedis

rds = StrictRedis(host='localhost', port=6379, password='9tBJEUr4wbnf')

mgd = pymongo.MongoClient().blog

r = rds.flushall()
m = mgd.posts.remove({})

print(r)
print(m)