# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 11:54 
from gevent.monkey import patch_all
patch_all()
from flask import Flask
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from flask_mail import Mail
from flask_moment import Moment
from config.config import config
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = MongoClient().blog
lm = LoginManager()
csrf = CsrfProtect()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # app.config['SERVER_NAME'] = 'vaayne.com'
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    lm.init_app(app)
    lm.login_view = 'auth.login'
    csrf.init_app(app)

    from .views import view
    app.register_blueprint(view)
    from .views.api import api as api
    app.register_blueprint(api, url_prefix='/api')
    from .views.feed import feed
    app.register_blueprint(feed, url_prefix='/feed')
    from .views.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    return app


def init_log(name, level="INFO"):
    import logging, colorlog
    formatter = colorlog.ColoredFormatter(
        fmt="%(log_color)s%(asctime)s-%(name)s | %(levelname)-8s| %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    sh = logging.StreamHandler()
    fh = logging.FileHandler(filename=name + '.log', encoding='utf-8')
    logging._defaultFormatter = formatter
    log_ = logging.getLogger(name)
    level_name = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    log_.setLevel(level=level_name.get(level.lower()))
    log_.addHandler(sh)
    log_.addHandler(fh)
    return log_
