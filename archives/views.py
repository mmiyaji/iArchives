#!/usr/bin/env python
# encoding: utf-8
"""
views.py

Created by mmiyaji on 2012-07-11.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

import os, re, sys, commands, time, datetime, random, logging
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from archives.models import *
from django.conf import settings
from django.http import Http404

# from utils import *
# from getimageinfo import *
# import isbooks.networkx as nx
# from django.core.cache import cache
logger = logging.getLogger('app')
def date_validate(date, dateformat="%Y-%m-%d"):
    # 指定したフォーマットでdatetimeオブジェクトに変換可能かチェック
    try:
        return datetime.datetime.strptime(date, dateformat)
    except:
        return None

def main():
    pass


if __name__ == '__main__':
    main()

