# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/27 11:54 

from flask import Flask
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from flask_mail import Mail
from flask_moment import Moment
import logging
from config.config import config
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = MongoClient().blog
lm = LoginManager()
csrf = CsrfProtect()


def init_log(log_name):
    log = logging.getLogger(log_name)
    logging.basicConfig(level=logging.INFO, format="%(filename)s %(asctime)s %(levelname)s %(message)s")
    fh = logging.FileHandler(filename=log_name + '.log', mode='w', encoding='utf-8')
    fh.setLevel(level=logging.INFO)
    fh.setFormatter(logging.Formatter("%(filename)s %(asctime)s %(levelname)s %(message)s"))
    log.addHandler(fh)
    return log


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # app.config['SERVER_NAME'] = 'vaayne.com'
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    lm.init_app(app)
    lm.login_view = 'login'
    csrf.init_app(app)
    # db.init_app(app)

    from .views import view
    app.register_blueprint(view)
    from .api import api as api
    app.register_blueprint(api, url_prefix='/api')
    from .feed import feed
    app.register_blueprint(feed, url_prefix='/feed')
    return app


