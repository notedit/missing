# -*- coding: utf-8 -*-

import socket
import datetime

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from flask.ext.mail import Mail

db = SQLAlchemy()
cache = Cache()
mail = Mail()

class DefaultConfig(object):

    DEBUG = True
    SECRET_KEY = 'lifeistooshorttowait'
    SESSION_COOKIE_PATH='/'
    SESSION_COOKIE_HTTPONLY = True
    #SESSION_COOKIE_SECURE = True
    #SESSION_COOKIE_NAME = 'themissing'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(180)
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://user:password@localhost/missing'
    SQLALCHEMY_ECHO = False

class TestConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://user:password@localhost/test'
    SQLALCHEMY_ECHO = False
    CSRF_ENABLED = False

class ProductionConfig(object):
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://user:password@localhost/missing'
    DEBUG = False

