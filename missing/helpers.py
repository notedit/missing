# -*- coding: utf-8 -*-
# author: notedit <notedit@gmail.com>

import functools

from flask import g


def keep_login_url(func):

    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        g.keep_login_url = True
        return func(*args,**kwargs)
    return wrapper
