import os
import sys
from flask import current_app
from flask.ext.script import Manager,prompt,prompt_pass,\
        prompt_bool,prompt_choices
from flask.ext.script import Server

from missing.configs import db
from missing import create_app

app = create_app()
manager = Manager(app)

@manager.command
def create_all():
    if prompt_bool("Are you sure? You will init your database"):
        db.create_all()

@manager.command
def drop_all():
    if prompt_bool("Are you sure? You will lose all your data!"):
        db.drop_all()

@manager.option('-u','--username',dest='username',required=True)
@manager.option('-p','--password',dest='password',required=True)
@manager.option('-e','--email',dest='email',required=True)
def createuser(username=None,password=None,email=None):
        pass

manager.add_command('runserver',Server())

if __name__ == '__main__':
    manager.run()
