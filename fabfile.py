# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/10 19:20 

from fabric.api import *
import os

env.hosts = ['root@blog']


def push():
    with lcd(os.path.abspath(__file__)):
        local('git pull')
        local('git push')


def depoly():
    with cd('/var/www/vaayne.com'):
        run('git pull')


def go():
    push()
    depoly()
