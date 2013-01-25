# -*- coding: utf-8 -*-

# author: notedit <notedit@gmail.com>

import flask
from flask import Blueprint

instance = Blueprint('site','site')

from missing.site import user
from missing.site import post
from missing.site import index
