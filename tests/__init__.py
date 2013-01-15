# -*- coding: utf-8 -*-

import unittest

from flask import g
from flask.ext.testing import TestCase as Base

from missing import create_app
from missing import configs

from missing.configs import db
from missing.logic import backend
from missing.logic import *

class TestCase(Base):

    def create_app(self):
        app = create_app(configs.TestConfig)
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
