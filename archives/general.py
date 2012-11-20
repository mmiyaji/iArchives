#!/usr/bin/env python
# encoding: utf-8
"""
general.py

Created by mmiyaji on 2012-07-11.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

from views import *

def home(request):
    """
    Case of GET REQUEST '/'
    home page
    """
    temp_values = Context()
    temp_values = {
        "subscroll":True,
        }
    return render_to_response('general/index.html',temp_values,
                              context_instance=RequestContext(request))

def signin(request):
    """
    Case of GET or POST REQUEST '/login/'
    login page
    """
    request_type = request.method
    if request_type == 'GET':
        temp_values = Context()
        temp_values = {
            "target":"login",
            "title":u"ログインページ",
            }
        return render_to_response('general/login.html',temp_values,
                              context_instance=RequestContext(request))
    elif request_type == 'POST' or request_type == 'UPDATE':
        return login_user(request)
# userログイン
def login_user(request):
    name = ""
    password = ""
    try:
        name = request.POST['name']
        password = request.POST['pass']
        users = authenticate(username=name, password=password)
        if users is not None:
            if users.is_active:
                login(request, users)
                return HttpResponseRedirect('/')
            else:
                return more_try(request,name,password)
            return more_try(request,name,password)
    except:
        return more_try(request,name,password)
def more_try(request,name,password = ''):
    error = u"入力されたユーザ名･パスワードは正しくありません．"
    return render_to_response('general/login.html',
                              {'loginError':error,'username':name},
                              context_instance=RequestContext(request))
# logoutページ
def signout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def main():
    pass


if __name__ == '__main__':
    main()
