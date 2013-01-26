# -*- coding: utf-8 -*-

import re

from flask.ext.wtf import Form,HiddenField,BooleanField,\
        TextField,PasswordField,SubmitField,ValidationError,required,\
        email,equal_to,regexp,length

from missing.logic import backend


RE_MATCH_NICKNAME = ur'^[\w\u4e00-\u9fcb\u3400-\u4db5.-_]{1,20}$'
RE_MATCH_UKEY = r'^[a-zA-Z0-9_.]+$'

class LoginForm(Form):
    
    next = HiddenField()
    remember = BooleanField()
    email = TextField(validators=[required(message=u'邮箱是必须的'),email(message=u'你的邮箱不合法')])
    password = PasswordField(validators=[required(message=u'密码没有填写')])
    submit = SubmitField()

class SignupForm(Form):

    next = HiddenField()
    username = TextField(default='',validators=[required(message=u'用户名是必须的'),
                regexp(RE_MATCH_UKEY,message=u'用户名只能包含英文,数字,小数点,下划线')])
    password = TextField(default='',validators=[required(message=u'密码不能为空')])
    repassword = TextField(default='',validators=[equal_to('password',message=u'两次输入的密码不相符')])
    email = TextField(default='',validators=[required(message=u'邮箱是必须的'),email(message='u你的邮箱不合法')])


    def validate_username(self,field):
        if backend.is_username_exist(field.data.encode('utf-8')):
            raise ValidationError,u'用户名已经存在'

    def validate_email(self,field):
        if backend.is_email_exist(field.data.encode('utf-8')):
            raise ValidationError,u'邮箱已经存在'


class EmailForm(Form):
    email = TextField(validators=[required(message=u'邮箱是必须的'),email(message=u'你的邮箱不合法')])


class PostForm(Form):
    
    title = TextField(default='',validators=[length(min=4,max=50,message=u'标题太短或者太长')])
    content = TextField()


class SuggestTitleForm(Form):

	url = TextField()

class ProfileSettingsForm(Form):
	# to do some check
	email = TextField(validators=[email(message='你的邮箱不合法')])
	nickname = TextField()
	website = TextField()
	signature = TextField()
	introduction = TextField()

class PasswordSettingsForm(Form):

	old_password = TextField(validators=[required(message='原有密码不能为空')])
	password = TextField(validators=[required(message='新密码不能为空')])
	repeat_password = TextField(validators=[equal_to("password",message='两次输入的新密码不匹配')])


