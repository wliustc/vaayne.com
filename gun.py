# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/12 17:24 
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing


bind = '127.0.0.1:8000'

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'
