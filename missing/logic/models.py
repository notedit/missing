# -*- coding: utf-8 -*-


# add your models here



import contextlib
from datetime import datetime
from werkzeug import cached_property

from missing.configs import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.Unicode(50),unique=True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(100))
    pic_small = db.Column(db.String(100))
    pic_big = db.Column(db.String(100))
    gender = db.Column(db.Boolean)
    date_create = db.Column(db.DateTime,default=datetime.now)
    date_update = db.Column(db.DateTime,default=datetime.now)

    @cached_property
    def json(self):
        return dict(id=self.id,
                    username=self.username,
                    email=self.email,
                    pic_small=self.pic_small,
                    pic_big=self.pic_big,
                    date_create=self.date_create,
                    date_update=self.date_update
                    )


class List(db.Model):
    __tablename__ = 'list'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.Unicode(300))
    content = db.Column(db.UnicodeText)
    pic_small = db.Column(db.String(255))
    pic_big = db.Column(db.String(255))
    author_id = db.Column(db.Integer,db.ForeignKey(User.id),index=True)
    show = db.Column(db.String(20),index=True)
    recommended = db.Column(db.Boolean,default=False,index=True)
    date_create = db.Column(db.DateTime,default=datetime.now)
    date_update = db.Column(db.DateTime,default=datetime.now)

    author = db.relation(User, innerjoin=True, lazy="joined")

    @cached_property
    def json(self):
        return dict(id=self.id,
                    title=self.title,
                    content=self.content,
                    pic_big=self.pic_big,
                    pic_small=self.pic_small,
                    author_id=self.author_id,
                    show=self.show,
                    recommended=self.recommended,
                    date_create=self.date_create,
                    date_update=self.date_update)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.Unicode(300))
    content = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer)
    type = db.Column(db.String(20))
    url = db.Column(db.String(300))
    post_id = db.Column(db.Integer,index=True)
    show = db.Column(db.Boolean,default=True,index=True)
    status = db.Column(db.String(20))
    liked_by = db.Column(db.Array(db.Integer,mutable=True),default=[])
    date_create = db.Column(db.DateTime,default=datetime.now)
    date_update = db.Column(db.DateTime,default=datetime.now)

    @cached_property
    def json(self):
        return dict(id=self.id,
                    title=self.title,
                    content=self.content,
                    author_id=self.author_id,
                    type=self.type,
                    url=self.url,
                    post_id=self.post_id,
                    show=self.show,
                    status=self.status,
                    liked_by = self.liked_by,
                    date_create=self.date_create,
                    date_update=self.date_create)


class UserFollowAsso(db.Model):

    __tablename__ = 'user_follow_asso'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    user_id_to = db.Column(db.Integer)
    date_create = db.Column(db.DateTime,default=datetime.now)

# 暂时先不用
class UserLikeAsso(db.Model):
    
    __tablename__ = 'user_like_asso'
    user_id = db.Column(db.Integer)
    object_id = db.Column(db.Integer)
    type = db.Column(db.String(20))
    date_create = db.Column(db.DateTime,default=datetime.now)

class Comment(db.Model):

    __tablename__ = 'comment'

    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    content = db.Column(db.UnicodeText)
    date_create = db.Column(db.DateTime,default=datetime.now)

    @cached_property
    def json(self):
        return dict(id=self.id,
                    post_id=self.post_id,
                    author_id=self.author_id,
                    content=self.content,
                    date_create=self.date_create)

