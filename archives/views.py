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

def get_page_list(page, count, search_span, view_max=13):
    # pagerのために必要な値を計算するメソッド
    pages = dict()
    page_max = (count / search_span)
    if page <= 0:
        page = 1
    if count%search_span!=0:
        page_max +=1
        pre_page = None
    next_page = None
    if page_max >= page+1:
        next_page = page+1
    if page!=0:
        pre_page = page-1
    pages['next_page'] = next_page
    pages['now_page'] = page
    pages['pre_page'] = pre_page
    pages['max'] = count
    pages['start'] = (page-1)*search_span+1
    end = 0
    if (page)*search_span>=count:
        end=count
    else:
        end = (page)*search_span
    pages['end'] = end
    page_list = []
    if page_max>(view_max+2):
        page_list.append(1)
        mins = page-(int)(view_max/2)
        maxs = page+(int)(view_max/2)
        if (maxs - mins) < view_max:
            mins = maxs - view_max
        if mins<2:
            mins = 2
            maxs = view_max
        else:
            page_list.append(-1)
        if maxs>page_max:
            maxs = page_max
        for x in range(mins, maxs):
            page_list.append(x)
        if maxs<page_max:
            page_list.append(-1)
        page_list.append(page_max)
    else:
        for x in range(1, page_max+1):
            page_list.append(x)
        if len(page_list)==1:
            page_list = None
    return page_list,pages
def main():
    pass


if __name__ == '__main__':
    main()

