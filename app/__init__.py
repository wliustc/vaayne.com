# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 11:54 
from gevent.monkey import patch_all
patch_all()
from flask import Flask
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from flask_mail import Mail
from flask_moment import Moment
import logging
from config.config import config
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_cache import Cache


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = MongoClient().blog
lm = LoginManager()
csrf = CsrfProtect()
cache = Cache()


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
    cache.init_app(app)

    from .views import view
    app.register_blueprint(view)
    from .views.api import api as api
    app.register_blueprint(api, url_prefix='/api')
    from .views.feed import feed
    app.register_blueprint(feed, url_prefix='/feed')
    from .views.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    return app


def init_log(log_name):
    import logging
    LOG_LEVEL = logging.INFO
    from colorlog import ColoredFormatter
    # logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)-8s%(reset)s-%(log_color)s%(name)s-%(log_color)s%(filename)s| "
        "%(log_color)s%(levelname)8s%(reset)s | %(log_color)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)

    fh = logging.FileHandler(filename=log_name+'.log', encoding='utf-8')
    fh.setLevel(LOG_LEVEL)
    fh.setFormatter(formatter)

    log_ = logging.getLogger(log_name)
    log_.setLevel(LOG_LEVEL)
    log_.addHandler(stream)
    log_.addHandler(fh)

    return log_
