# -*- coding: utf-8 -*-

# author: notedit <notedit@gmail.com>
# date: 2013/01/18  morning

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
from missing.authutil import user_required
from missing.helpers import keep_login_url

from missing.site.forms import PostForm


@instance.route('/post/new',methods=('GET','POST'))
@user_required
def post_new():
    
    form = PostForm()

    if form.validate_on_submit():

        title = form.title.data.encode('utf-8')
        content = form.content.data.encode('utf-8')
        author_id = g.user['id']
        
        try:
            post = backend.add_post(title,author_id,content)
        except BackendError,ex:
            flash('新建内容失败请重试','error')
            return render_template('site/post_new.html',form=form)
        else:
            flash('新建列表成功','success')

        return redirect('/post/%d' % post['id'])

    return render_template('site/post_new.html',form=form)



@instance.route('/post/<int:post_id>',methods=('GET',))
def post_one(post_id):
    try:
        post = backend.get_post(post_id)
    except BackendError,ex:
        abort(404)

    try:
        page = int(request.values.get('page','1'))
    except ValueError:
        page = 1

    if page <= 0: page = 1
    
    limit = 50
    offset = (page - 1) * 50
    items = backend.get_post_item(post_id,limit=limit,offset=offset)
    item_count = len(items) if len(items) <= 50 else \
                    backend.get_post_item_count(post_id)

    return render_template('site/post_one.html',
                            post=post,
                            items=items,
                            item_count=item_count)


@instance.route('/post/<int:post_id>/edit',methods=('GET','POST'))
@user_required
def post_edit(post_id):
    
    post = backend.get_post(post_id)
    if post['author_id'] != g.user_id:
        abort(403)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        
        title = form.title.data.encode('utf-8')
        content = form.content.data.encode('utf-8')

        try:
            post = backend.set_post(post_id,{
                            'title':title,
                            'content':content
                        })
        except BackendError,ex:
            flash('内容修改失败,请检查重试','error')
        else:
            return redirect('/post/%d' % post_id)


    return render_template('site/post_edit.html',form=form)


@instance.route('/post/<int:post_id>/delete',methods=('GET',))
@user_required
def post_delete(post_id):

    post = backend.get_post(post_id)
    if post['author_id'] != g.user_id:
        abort(403)

    post = backend.set_post(post_id,{'show':False})

    return redirect('/index')








    

