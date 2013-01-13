# -*- coding: utf-8 -*-
# author: notedit
# date: 2013-01-13

import types
import traceback

from werkzeug import generate_password_hash, check_password_hash

from missing.coreutil import BackendError,register,assert_error

from missing.logic.models import User,Post,Item,Comment

from missing.configs import db


@register('get_comment')
def get_comment(comment_id):
    assert_error(type(comment_id) == types.IntType,'ParamError')
    comm = Comment.query.get(comment_id)
    return comm.json

@register('get_post_comment')
def get_post_comment(post_id,limit=50,offset=0,show=True):
    assert_error(type(post_id) == types.IntType,'ParamError')
    _ans = [Comment.show == True,] if show else []
    _ans.append(Comment.post_id == post_id)
    q = reduce(db.and_,_ans)
    comms = Comment.query.filter(q).order_by(Comment.date_create.desc()).\
            limit(limit).offset(offset).all()
    return [c.json for c in comms]

@register('get_post_comment_count')
def get_post_comment_count(post_id,show=True):
    _ans = [Comment.show == True,] if show else []
    _ans.append(Comment.post_id == post_id)
    q = reduce(db.and_,_ans)
    count = Comment.query.filter(q).count()
    return count


