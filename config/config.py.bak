# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/18 21:38
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'SECRET_KEY'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    MONGODB_DATABASE = 'blog'


class TestingConfig(Config):
    MONGODB_DATABASE = 'test'

config = dict(
    testing=TestingConfig,
    production=ProductionConfig,
    default=TestingConfig
)
