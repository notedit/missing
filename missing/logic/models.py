# -*- coding: utf-8 -*-


# add your models here



import contextlib
from datetime import datetime
from peewee import *

pg_db = PostgresqlDatabase(None)


def init_db(dbname,user='',password='',host='localhost',port=5432):
    pg_db.init(dbname,user=user,password=password,host=host,port=port)
    pg_db.connect()



class BaseModel(Model):
    class Meta:
        database = pg_db

class User(BaseModel):
    
    username = CharField(max_length=30)
    email = CharField(max_length=50)
    password = CharField(max_length=80)
    pic_small = CharField(max_length=100)
    pic_big = CharField(max_length=100)
    gender = BooleanField()
    date_create = DateTimeField(default=datetime.now())
    date_update = DateTimeField(default=datetime.now())

    def json(self):
        return {
                'id':self.id,
                'username':self.username,
                'email':self.email,
                'pic_small':self.pic_small,
                'pic_big':self.pic_big,
                'date_create':self.date_create,
                'date_update':self.date_update
                }


class Post(BaseModel):

    title = CharField(max_length=255)
    pic_small = CharField(max_length=255)
    pic_big = CharField(max_length=255)
    pic_width = IntegerField()
    pic_height = IntegerField()
    author = ForeignKeyField(User)
    show = CharField(max_length=20)
    recommended = BooleanField(default=False)
    date_create = DateTimeField(default=datatime.now())
    date_update = DateTimeField(default=datetime.now())

    def json(self):
        return {
                'id':self.id,
                'title':self.title,
                'pic_big':self.pic_big,
                'pic_small':self.pic_small,
                'pic_width':self.pic_width,
                'pic_height':self.pic_height,
                'author_id':self.author_id,
                'show':self.show,
                'recommended':self.recommended,
                'date_create':self.date_create,
                'date_update':self.date_update,
                }


class Dot(BaseModel):

    title = CharField(max_length=255)
    content = TextField()
    author = ForeignKeyField(User)
    
