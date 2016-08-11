# -*- coding:utf-8 -*-
# Created by Vaayne at 2016/07/18 21:38
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'SECRET_KEY'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379


class ProductionConfig(Config):
    MONGODB_DATABASE = 'blog'


class TestingConfig(Config):
    MONGODB_DATABASE = 'test'

config = dict(
    testing=TestingConfig,
    production=ProductionConfig,
    default=TestingConfig
)
