# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/08/01 14:37 

from app import create_app
app = create_app('production')
from flask_script import Manager, Server, Shell

manage = Manager(app)


def make_shell_context():
    return dict(
        app=app,
    )

manage.add_command('shell', Shell(make_context=make_shell_context()))
manage.add_command('run', Server(
    use_debugger=True,
    use_reloader=True,
    # host='0.0.0.0',
    # port='80'
))

if __name__ == '__main__':
    manage.run()

