# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/12 17:24 

import multiprocessing
import os

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
chdir = '/var/www/vaayne.com'
# env = os.path.join(chdir, 'venv')
reload = True

x_forwarded_for_header = 'X-FORWARDED-FOR'
