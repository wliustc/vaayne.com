#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 11:18 

from app import create_app
app = create_app('production')
from app import db
from flask_script import Manager, Server, Shell
from config import config

manage = Manager(app)


def make_shell_context():
    return dict(
        app=app,
        db=db,
        # User=User,
        # Post=Post,
    )

manage.add_command('shell', Shell(make_context=make_shell_context()))
manage.add_command('run', Server(
    # use_debugger=True,
    use_reloader=True,
    # host='0.0.0.0',
    # port='80'
))

if __name__ == '__main__':
    manage.run()
