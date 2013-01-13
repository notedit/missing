# -*- coding: utf-8 -*-
# author: notedit
# date: 2013-01-13

import types
import traceback

from missing.coreutil import BackendError,register,assert_error

from missing.logic.models import User,Post,Item,Action

from missing.configs import db


@register('add_action')
def add_action(ainfo={}):
    pass



