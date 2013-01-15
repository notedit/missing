# -*- coding: utf-8 -*-

# author: notedit <notedit@gmail.com>
# date: 2013/01/14  morning

import sys 
import time
import flask
from flask import request
from flask import g
from flask import Response
from flask import current_app
from flask import session
from flask import jsonify
from flask import render_template
from flask.views import MethodView
from flask.views import View

from missing.site import instance
from missing.logic import backend
from missing.coreutil import BackendError


@instance.route('/login',methods=('GET','POST')) 
def login():
    pass

