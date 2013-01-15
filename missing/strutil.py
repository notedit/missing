# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime

from email.utils import formatdate



def cookie_date(epoch_seconds=None):

    rfcdate = formatdate(epoch_seconds)
    return '%s-%s-%s GMT' % (rfcdate[:7], rfcdate[8:11], rfcdate[12:25])


def int2path(uint,baseurl,extname='.caf'):
    """将32bit正整数转换为path"""
    file_key = ''
    for i in range(6):
        uint,remainder = divmod(uint,36)
        if remainder < 10:
            file_key = chr(remainder+48) + file_key
        else:
            file_key = chr(remainder+97-10) + file_key
    
    fullurl = os.path.join(baseurl,file_key[0:2],file_key[2:4],file_key[4:6],file_key+extname)
    return fullurl


def int2ukey(uint):

    ukey = ''
    for i in range(6):
        uint,remainder = divmod(uint,36)
        if remainder < 10:
            ukey = chr(remainder+48) + ukey
        else:
            ukey = chr(remainder+97-10) + ukey
    return ukey



