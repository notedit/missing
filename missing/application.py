# -*- coding: utf-8 -*-


import os
import logging
from flask import Flask

from missing import configs
from missing.configs import db,cache,mail

from missing import logic
from missing import authutil
from missing.logic import backend
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

def configure_handler(app):
    
    def after_this_request(f):
        if not hasattr(g,'after_request_callbacks'):
            g.after_request_callbacks = []
        g.after_request_callbacks.append(f)
        return f

    @app.after_request
    def call_after_request_callbacks(response):
        for callback in getattr(g,'after_request_callbacks',()):
            response = callback(response)
        return response

    @app.before_request
    def cookie_auth():
        if request.cookies.get('is_logined'):
            if authutil.is_logined(request):
                max_age = 3600*24*30*6
                expires_time = int(time.time()) + max_age
                expires = strutil.cookie_date(expires_time) 
                g.user = backend.get_user(int(request.cookie.get('ukey')))
                @after_this_request
                def set_cookie(response):
                    response.set_cookie('is_logined',
                                        'True',
                                        max_age=max_age,
                                        expires=expires,
                                        path='/')
                    return response
            else:
                g.user = {}
                @after_this_request
                def delete_cookie(response):
                    response.delete_cookie('is_logined')
                    return response
        else:
            g.user = {}



def configure_blueprints(app):
    app.register_blueprint(site)
    print app.url_map
