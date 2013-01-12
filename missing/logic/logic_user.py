# -*- coding: utf-8 -*-
# author: notedit
# date: 2013-01-12

import types
import traceback

from werkzeug import generate_password_hash, check_password_hash

from missing.coreutil import BackendError,register,assert_error

from missing.logic.models import User,Post,Item

from missing.configs import db

@register('get_user')
def get_user(user_id):
    multi = False
    if type(user_id) == types.ListType:
        assert_error(all([type(u) == types.IntType for u in user_id]),'ParamError')
        multi = True
    else:
        assert_error(type(user_id) == types.IntType,'ParamError')
        user_id = user_id,

    users = User.query.filter(User.id.in_(user_id)).all()
    if not users:
        raise BackendError('EmptyError','用户不存在')

    if multi:
        return [u.json for u in users]
    else:
        return users[0].json

def _check_username(username):
    u = User.query.filter(db.func.lower(User.username) == username).first()
    return u

def _check_email(email):
    u = User.query.filter(User.email == email).first()
    return u

@register('add_user')
def add_user(username,email,passstr):
    assert_error(type(email)==types.StringType,'ParamError','邮箱应该为字符串')
    assert_error(type(passstr)==types.StringType,'ParamError','密码应该为字符串')
    assert_error(type(username)==types.StringType,'ParamError','用户昵称应该为字符串')
    
    if _check_username(username):
        raise BackendError('UsernameError','用户名已经存在')

    if _check_email(email):
        raise BackendError('EmailError','邮箱已经存在')

    try:
        user = User(email=email,username=username,password=passstr)
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        raise BackendError('InternalError',traceback.format_exc())

    return user.json

@register('set_user')
def set_user(user_id,info_d):
    assert_error(type(user_id) == types.IntType,'ParamError')
    user = User.query.get(user_id)
    try:
        for k,v in info_d.items():
            if v is not None:
                setattr(user,k,v)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    else:
        return user.json


@register('follow_user')
def follow(fid,tid):
    assert_error(all(map(lambda _id: type(_id) == types.IntType,[fid,tid])),'ParamError')
    try:
        asso = UserFollowAsso(user_id=fid,user_id_to=tid)
        db.session.add(asso)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    else:
        return True

@register('unfollow_user')
def unfollow_user(fid,tid):
    assert_error(all(map(lambda _id: type(_id) == types.IntType,[fid,tid])),'ParamError')
    try:
        asso = UserFollowAsso(user_id=fid,user_id_to=tid)
        db.session.delete(asso)
    except:
        db.session.rollback()
        raise
    else:
        return True


@register('get_user_following')
def get_user_following(user_id,limit=50,offset=0):
    assert_error(type(user_id) == types.IntType,'ParamError')
    follows = User.query.join(UserFollowAsso,User.id == UserFollowAsso.user_id_to).\
            filter(UserFollowAsso.user_id == user_id).limit(limit).offset(offset).all()
    return [u.json for u in follows]

@register('get_user_following_count')
def get_user_following_count(user_id):
    _count = UserFollowAsso.query.filter(UserFollowAsso.user_id == user_id).count()
    return _count

@register('get_user_follower')
def get_user_follower(user_id,limit=50,offset=0):
    assert_error(type(user_id) == types.IntType,'ParamError')
    follows = User.query.join(UserFollowAsso,User.id == UserFollowAsso.user_id).\
            filter(UserFollowAsso.user_id_to == user_id).limit(limit).offset(offset).all()
    return [u.json for u in follows]

@register('get_user_follower_count')
def get_user_follower_count(user_id):
    _count = UserFollowAsso.query.filter(UserFollowAsso.user_id_to == user_id).count()
    return _count


@register('is_following_user')
def is_following_user(fid,tid):
    assert_error(all(map(lambda _id: type(_id) == types.IntType,[fid,tid])),'ParamError')
    _count = UserFollowAsso.query.filter(UserFollowAsso.user_id == fid).\
            filter(UserFollowAsso.user_id_to == tid).count()
    return True if _count > 0 else False



