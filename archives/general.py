#!/usr/bin/env python
# encoding: utf-8
"""
general.py

Created by mmiyaji on 2012-07-11.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

import os, re, sys, commands, time, datetime, random
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from utils import *
# from getimageinfo import *
# import isbooks.networkx as nx
# from django.core.cache import cache


def home(request):
    """
    """
    temp_values = Context()
    temp_values["hoge"]="huga"
    return render_to_response('general/index.html',temp_values,
                              context_instance=RequestContext(request))

def main():
    pass


if __name__ == '__main__':
    main()

