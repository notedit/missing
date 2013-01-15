# -*- coding: utf-8 -*-


import os
import logging
from flask import Flask

from missing import configs
from missing.configs import db,cache,mail

from missing import logic
from missing.site import instance as site

# add some other view

__all__ = ['create_app']


DEFAULT_APP_NAME = 'missing'


def create_app(config=None,app_name=None):
    
    if app_name is None:
        app_name = DEFAULT_APP_NAME
    
    app = Flask(app_name)

    configure_app(app,config)
    configure_db(app)
    configure_blueprints(app)
    #configure_cache(app)
    return app

def configure_app(app,config):
    app.config.from_object(configs.DefaultConfig())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar('APP_CONFIG',silent=True)

def configure_db(app):
    db.init_app(app)

def configure_blueprints(app):
    app.register_blueprint(site)

    
