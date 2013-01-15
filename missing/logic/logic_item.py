# -*- coding: utf-8 -*-
# author: notedit
# date: 2013-01-13

import types
import traceback

from missing.coreutil import BackendError,register,assert_error

from missing.logic.models import User,Post,Item

from missing.configs import db


@register('get_item')
def get_item(item_id):
    assert_error(type(item_id) in (types.IntType,types.ListType),'ParamError')
    multi = False
    if type(item_id) == types.ListType:
        assert_error(all([type(i) == types.IntType for i in item_id]),'ParamError')
        multi = True
    else:
        item_id = item_id,

    items = Item.query.filter(Item.id.in_(item_id)).all()
    if len(items) == 0:
        raise BackendError('EmptyError','item不存在')

    if multi:
        return dict([(i.id,i.json) for i in items])
    else:
        return items[0].json


@register('add_item')
def add_item(title,author_id,post_id,atype,url=None,content=None):
    assert_error(type(title) == types.StringType,'ParamError')
    assert_error(type(author_id) == types.IntType,'ParamError')
    assert_error(type(post_id) == types.IntType,'ParamError')
    
    qd = {
            'title':title,
            'author_id':author_id,
            'post_id':post_id,
            'content':content,
            'atype':atype,
            'url':url,
            }
    try:
        i = Item(**qd)
        db.session.add(i)
        db.session.commit()
    except:
        db.session.rollback()
        raise BackendError('InternalError',traceback.format_exc())
    return i.json


@register('set_item')
def set_item(item_id,idict):
    fd_list = ('title','content','author_id','atype','url','post_id','show','status',
                'date_create','date_update')
    cset = set(idict.keys())
    if not cset.issubset(fd_list):
        raise BackendError('ParamError','更新的字段不允许')
    i = Item.query.get(item_id)
    for k,v in idict.items():
        if v is not None:
            setattr(i,k,v)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise 
    return i.json

