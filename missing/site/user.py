# -*- coding: utf-8 -*-

# author: notedit <notedit@gmail.com>
# date: 2013/01/14  morning

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

from werkzeug import generate_password_hash, check_password_hash

from missing import authutil
from missing.site import instance
from missing.logic import backend
from missing.coreutil import BackendError

from missing.site.forms import SignupForm,LoginForm


@instance.route('/login',methods=('GET','POST')) 
def login():
    if authutil.is_logined(request):
        return redirect('/')

    form = LoginForm(email=request.values.get('email',''),
                    password=request.values.get('password',''))

    if form.validate_on_submit():
        email = form.email.data.encode('utf-8')
        password = form.password.data.encode('utf-8')

        ret,user = backend.auth_user(email,password)
        if ret:
            next_url = form.next.data
            if not next_url or next_url == request.path:
                next_url = '/'
            resp = redirect(next_url)
            timeout = 24 * 3600 * 180 if form.remember.data else None
            authutil.set_logined(request,resp,str(user['id']),timeout=timeout)
            return resp

        flash(u'用户名或者密码错误,请重试','error')

    return render_template('site/login.html',form=form)


@instance.route('/logout',methods=('GET',))
def logout():
    resp = redirect('/')
    authutil.set_logout(request,resp)
    return resp
        



@instance.route('/signup',methods=('GET','POST'))
def signup():
    if authutil.is_logined(request):
        return redirect('/')

    form = SignupForm(next=request.values.get('next'))

    if form.validate_on_submit():
        
        username = form.username.data.encode('utf-8')
        password = form.password.data.encode('utf-8')
        email = form.email.data.encode('utf-8')

        
        try:
            user = backend.add_user(username,email,password)
        except BackendError,ex:
            logging.info(traceback.format_exc())
            flash('用户注册失败,请稍后再试','error')
            return render_template('signup.html',form=form)

        next_url = form.next.data

        if not next_url or next_url == request.path:
            next_url = '/'

        return redirect(next_url)

    print form.errors
    return render_template('site/signup.html',form=form)




