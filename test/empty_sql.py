# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/01 15:47 

from pymongo import MongoClient
from redis import StrictRedis

mog = MongoClient().blog.posts
rds = StrictRedis()

mog.remove({})
rds.flushall()
