# -*- coding: utf-8 -*-

# author: notedit <notedit@gmail.com>
# date: 2013/01/19  morning

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

from missing.site.forms import SignupForm,LoginForm


@instance.route('/post/<int:post_id>/additem',methods=('GET','POST'))
@user_required
def item_add(post_id):
    
    form = ItemForm()
    if form.validate_on_submit():
        title = form.title.data.encode('utf-8')
        author_id = g.user_id
        atype = ''
        content = form.content.data
        try:
            item = backend.add_item(title,author_id,post_id,atype,content=content)
        except BackendError,ex:
            flash('新内容添加失败请重试','error')
    
    return redirect('/post/%d' % post_id)



@instance.route('/post/<int:post_id>/delitem/<int:item_id>',methods=('GET'))
@user_required
def item_del(post_id,item_id):

    post = backend.get_post(post_id)
    item = backend.get_item(item_id)

    if g.user_id != post['author_id'] or item['post_id'] != post_id:
        abort(403)

    backend.set_item(item_id,{'show':False})

    return redirect('/post/%d' % post_id)


@instance.route('/post/<int:post_id>/edititem/<int:item_id>',methods=('GET','POST'))
@user_required
def item_edit(post_id,item_id):
 
    post = backend.get_post(post_id)
    item = backend.get_item(item_id)

    if g.user_id != post['author_id'] or item['post_id'] != post_id:
        abort(403)

    form = ItemForm(**item)
    if form.validate_on_submit():
        title = form.title.data.encode('utf-8')
        author_id = g.user_id
        atype = ''
        content = form.content.data

        try:
            item = backend.set_item(post_id,{
                                    'title':title,
                                    'content':content
                                })
        except BackendError,ex:
            flash('内容修改失败,请检查重试','error')

    return redirect('/post/%d' % post_id)
        
