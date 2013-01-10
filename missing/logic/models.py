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


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.Unicode(300))
    pic_small = db.Column(db.String(255))
    pic_big = db.Column(db.String(255))
    pic_width = db.Column(db.Integer)
    pic_height = db.Column(db.Integer)
    author_id = db.Column(db.Integer,db.ForeignKey(User.id),index=True)
    show = db.Column(db.String(20),index=True)
    recommended = db.Column(db.Boolean,default=False)
    date_create = db.Column(db.DateTime,default=datetime.now)
    date_update = db.Column(db.DateTime,default=datetime.now)

    author = db.relation(User, innerjoin=True, lazy="joined")

    @cached_property
    def json(self):
        return dict(id=self.id,
                    title=self.title,
                    pic_big=self.pic_big,
                    pic_small=self.pic_small,
                    pic_width=self.pic_width,
                    pic_height=self.pic_height,
                    author_id=self.author_id,
                    show=self.show,
                    recommended=self.recommended,
                    date_create=self.date_create,
                    date_update=self.date_update)


class Dot(db.Model):
    __tablename__ = 'dot'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.Unicode(300))
    content = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer)
    type = db.Column(db.String(20))
    url = db.Column(db.String(300))
    post_id = db.Column(db.Integer,index=True)
    x_coordinate = db.Column(db.Float)
    y_coordinate = db.Column(db.Float)
    date_create = db.Column(db.DateTime,default=datetime.now)
    
    @cached_property
    def json(self):
        return dict(id=self.id,
                    title=self.title,
                    content=self.content,
                    author_id=self.author_id,
                    type=self.type,
                    url=self.url,
                    post_id=self.post_id,
                    x_coordinate=self.x_coordinate,
                    y_coordinate=self.y_coordinate
                    date_create=self.date_create)


class UserFollowAsso(db.Model):

    __tablename__ = 'user_follow_asso'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    user_id_to =f db.Column(db.Integer)



