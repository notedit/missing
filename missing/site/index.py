# -*- coding: utf-8 -*-

# author: notedit <notedit@gmail.com>
# date: 2013/01/25  morning

import sys 
import time
import logging
import flask
from flask import g
from flask import request
from flask import redirect
from flask import Response
from flask import current_app
from flask import session
from flask import jsonify
from flask import flash
from flask import render_template
from flask.views import MethodView
from flask.views import View


from missing import authutil
from missing.site import instance
from missing.logic import backend
from missing.coreutil import BackendError



@instance.route('/',methods=('GET',)) 
def index():
    try:
        page = int(request.values.get('page',1))
    except:
        page = 1

    if page <= 0:page = 1
    
    offset = (page-1) * 50
    latest_posts = backend.get_latest_post(offset=offset,limit=50)
    post_count = backend.get_post_count()

    hot_posts = backend.get_hot_post(offset=offset,limit=50)
    
    return render_template(latest_posts=latest_posts,hot_posts=hot_posts,
                                post_count=post_count,page=page)





    




