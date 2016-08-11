# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/10 19:20 

from fabric.api import *
import os

env.hosts = ['root@blog']


def push():
    with lcd(os.path.split(os.path.abspath(__file__))[0]):
        local('git pull')
        local('git push origin master')


def depoly():
    with cd('/var/www/vaayne.com'):
        run('git pull')
        run('supervisorctl restart vaayne')
        run('tail -f /var/log/supervisor/vaayne.log')


def restart():
    with cd('/var/www/vaayne.com'):
        run('supervisorctl restart vaayne')
        run('tail -f /var/log/supervisor/vaayne.log')


def go():
    push()
    depoly()
