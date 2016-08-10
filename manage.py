#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 11:18 
from gevent.monkey import patch_all
patch_all()
from app import create_app
app = create_app('production')
from app import db
from flask_script import Manager, Server, Shell

manage = Manager(app)


def make_shell_context():
    return dict(
        app=app,
        db=db,
    )

manage.add_command('shell', Shell(make_context=make_shell_context()))
manage.add_command('run', Server(
    use_reloader=True,
))

if __name__ == '__main__':
    manage.run()
