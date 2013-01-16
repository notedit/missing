# -*- coding: utf-8 -*-

# author: notedit <notedit@gmail.com>
# date: 2013/01/14  morning

import sys 
import time
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


@instance.route('/login',methods=('GET','POST')) 
def login():
    if authutil.is_logined(request):
        return redirect('/')

    form = LoginForm(email=request.values.get('email',None),
                    password=request.values.get('password',None))
    if form.validate_on_submit():
        pass


@instance.route('/signup',methods=('GET','POST'))
def signup():
    if authutil.is_logined(request):
        return redirect('/')

    form = SignupForm()
    if form.validate_on_submit():
        pass


