# -*- coding: utf-8 -*-
# author: notedit
# date: 2013-01-13

import types
import traceback

from missing.coreutil import BackendError,register,assert_error

from missing.logic.models import User,Post,Item

from missing.configs import db


@register('get_post')
def get_post(post_id):
    post = Post.query.get(post_id)
    return post.json

@register('add_post')
def add_post(title,author_id,content=None,pic_small='',pic_big='',show=True,recommended=False):
    assert_error(type(title) == types.StringType,'ParamError')
    assert_error(type(author_id) == types.IntType,'ParamError')
    
    qd = {
            'title':title,
            'author_id':author_id,
            'content':content,
            'pic_small':pic_small,
            'pic_big':pic_big,
            'show':show,
            'recommended':recommended,
            }
    try:
        p = Post(**qd)
        db.session.add(p)
        db.session.commit()
    except:
        db.session.rollback()
        raise BackendError('InternalError',traceback.format_exc())
    return p.json



@register('set_post')
def set_post(post_id,pdict):
    fd_list = ('title','content','pic_small','pic_big','author_id','show',
                'recommended','date_create','date_update')
    cset = set(pdict.keys())
    if not cset.issubset(fd_list):
        raise BackendError('ParamError','更新的字段不允许')
    post = Post.query.get(post_id)
    for k,v in pdict.items():
        if v is not None:
            setattr(post,k,v)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise 

    return post.json


@register('get_latest_post')
def get_latest_post(offset=0,limit=50):
    posts = Post.query.filter(Post.show == True).order_by(Post.date_create.desc()).\
            limit(limit).offset(offset).all()

    _posts = []
    for p in posts:
        _u = p.author.json
        _p = p.json
        _p.update({'user':_u})
        _posts.append(_p)

    return _posts


@register('get_post_count')
def get_post_count():
    count = Post.query.filter(Post.show == True).count()
    return count

@register('get_hot_post')
def get_hot_post(offset=0,limit=50):
    posts = Post.query.filter(Post.show == True).order_by(Post.visite_count.desc()).\
            limit(limit).offset(offset).all()

    _posts = []
    for p in posts:
        _u = p.author.json
        _p = p.json
        _p.update({'user':_u})
        _posts.append(_p)

    return _posts


@register('get_post_item')
def get_post_item(post_id,limit=50,offset=0):
    items = Item.query.filter(db.and_(Item.post_id == post_id,Item.show == True)).\
            order_by(Item.date_create).limit(limit).offset(offset).all()
    return [i.json for i in items]

@register('get_post_item_count')
def get_post_item_count(post_id):
    count = Item.query.filter(db.and_(Item.post_id == post_id,Item.show == True)).count()
    return count

