# -*- coding: utf-8 -*-


import os
import sys
import types
import time
import json

from datetime import datetime
from datetime import timedelta

from tests import TestCase

from missing.coreutil import BackendError
from missing.logic.models import User,Post,Item,Comment,Action,UserFollowAsso
from missing.logic import backend
from missing.configs import db

class TestUserLogic(TestCase):

    def test_get_user(self):
        user1 = User(username='user01',email='user01@gmail.com')
        user2 = User(username='user02',email='user02@gmail.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        user = backend.get_user(user1.id)
        assert user['username'] == user1.username

        users = backend.get_user([user1.id,user2.id])
        assert len(users) == 2

    def test_add_user(self):
        user1 = User(username='user01',email='user01@gmail.com',password='pass01')
        db.session.add(user1)
        db.session.commit()

        user = backend.add_user('user02','user02@gmail.com','pass02')
        assert user['username'] == 'user02'

        self.assertRaises(BackendError,backend.add_user,'user02','user02@gmail.com','pass02')

    def test_auth_user(self):
        user = backend.add_user('user02','user02@gmail.com','pass02')
        ret,_user = backend.auth_user('user02@gmail.com','pass02')
        print ret
        assert ret == True

        ret,_user = backend.auth_user('user01@gmail.com','pass02')
        assert ret == False

    def test_set_user(self):
        user1 = User(username='user01',email='user01@gmail.com',password='pass01')
        db.session.add(user1)
        db.session.commit()


        user2 = backend.set_user(user1.id,{'username':'user02'})
        assert user2['username'] == 'user02'


    def test_follow(self):
        user1 = User(username='user01',email='user01@gmail.com')
        user2 = User(username='user02',email='user02@gmail.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        ret = backend.follow_user(user1.id,user2.id)
        assert ret > 0

        asso = UserFollowAsso.query.get(ret)
        assert asso.user_id == user1.id
        assert asso.user_id_to == user2.id

        ret = backend.unfollow_user(user1.id,user2.id)

        assert ret == True
        asso = UserFollowAsso.query.filter(UserFollowAsso.user_id == user1.id).\
                filter(UserFollowAsso.user_id_to == user2.id).first()
        print asso 
        assert asso == None


    def test_get_user_following(self):
        user1 = User(username='user01',email='user01@gmail.com')
        user2 = User(username='user02',email='user02@gmail.com')
        user3 = User(username='user03',email='user03@gmail.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()

        backend.follow_user(user1.id,user2.id)
        backend.follow_user(user1.id,user3.id)

        users = backend.get_user_following(user1.id)
        assert len(users) == 2

        count = backend.get_user_following_count(user1.id)
        assert count == 2

    def test_get_user_follower(self):

        user1 = User(username='user01',email='user01@gmail.com')
        user2 = User(username='user02',email='user02@gmail.com')
        user3 = User(username='user03',email='user03@gmail.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()

        backend.follow_user(user2.id,user1.id)
        backend.follow_user(user3.id,user1.id)

        users = backend.get_user_follower(user1.id)
        assert len(users) == 2

        count = backend.get_user_follower_count(user1.id)
        assert count == 2

    
    def test_is_following_user(self):
 
        user1 = User(username='user01',email='user01@gmail.com')
        user2 = User(username='user02',email='user02@gmail.com')
        user3 = User(username='user03',email='user03@gmail.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()

        backend.follow_user(user1.id,user2.id)
        
        ret = backend.is_following_user(user1.id,user2.id)
        assert ret == True

        ret = backend.is_following_user(user1.id,user3.id)
        assert ret == False


class TestPostLogic(TestCase):

    def test_get_post(self):
        user = backend.add_user('user02','user02@gmail.com','pass02')
        post = Post(title='post01',author_id=user['id'],content='content01',pic_small='pic_small')
        db.session.add(post)
        db.session.commit()
        
        _post = backend.get_post(post.id)
        assert _post['title'] == 'post01'
        
    def test_add_post(self):
        user = backend.add_user('user02','user02@gmail.com','pass02')

        post = backend.add_post('title01',user['id'],content='content01')
        assert post['title'] == 'title01'

        self.assertRaises(BackendError,backend.add_post,'title02','',content='content01')


    def test_set_post(self):

        user = backend.add_user('user02','user02@gmail.com','pass02')
        post = backend.add_post('title01',user['id'],content='content01')

        post = backend.set_post(post['id'],{'title':'title03','date_create':datetime.now()})
        assert post['title'] == 'title03'

        # backendError

        self.assertRaises(BackendError,backend.set_post,post['id'],{'liked_by':'aaaaaa'})


    def test_get_latest_post(self):
        user = backend.add_user('user02','user02@gmail.com','pass02')
        post1 = backend.add_post('title01',user['id'],content='content01')
        post2 = backend.add_post('title02',user['id'],content='content02')
        post2 = backend.add_post('title03',user['id'],content='content03')

        posts = backend.get_latest_post()
        assert len(posts) == 3

        count = backend.get_post_count()
        assert count == 3

    def test_get_hot_post(self):
        user = backend.add_user('user02','user02@gmail.com','pass02')
        post1 = backend.add_post('title01',user['id'],content='content01')
        post2 = backend.add_post('title02',user['id'],content='content02')
        post2 = backend.add_post('title03',user['id'],content='content03')

        posts = backend.get_hot_post()
        assert len(posts) == 3

        count = backend.get_post_count()
        assert count == 3
        

    def test_get_post_item(self):
        user = backend.add_user('user02','user02@gmail.com','pass02')
        post1 = backend.add_post('title01',user['id'],content='content01')
    
        item1 = Item(post_id=post1['id'],title='title01',content='content01')
        item2 = Item(post_id=post1['id'],title='title02',content='content02')
        item3 = Item(post_id=post1['id'],title='title03',content='content03')

        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.commit()

        items = backend.get_post_item(post1['id'])
        assert len(items) == 3

        count = backend.get_post_item_count(post1['id'])
        assert count == 3


class TestItemLogic(TestCase):

    def test_get_item(self):
        user = backend.add_user('user02','user02@gmail.com','pass02')
        post1 = backend.add_post('title01',user['id'],content='content01')
    
        item1 = Item(post_id=post1['id'],title='title01',content='content01')

        db.session.add(item1)
        db.session.commit()

        item = backend.get_item(item1.id)
        assert item['title'] == item1.title


    def test_add_item(self):
        user = backend.add_user('user02','user02@gmail.com','pass02')
        post1 = backend.add_post('title01',user['id'],content='content01')

        item = backend.add_item('item1',user['id'],post1['id'],'')
        assert item['title'] == 'item1'
        
    def test_set_item(self):

        user = backend.add_user('user02','user02@gmail.com','pass02')
        post1 = backend.add_post('title01',user['id'],content='content01')

        item = backend.add_item('item1',user['id'],post1['id'],'')

        item = backend.set_item(item['id'],{'title':'title3'})
        assert item['title'] ==  'title3'

        
