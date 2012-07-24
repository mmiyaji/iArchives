#!/usr/bin/env python
# encoding: utf-8
"""
author.py

Created by mmiyaji on 2012-07-24.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from views import *

def home(request):
    """
    Case of GET REQUEST '/author/'
    著者の一覧を表示するページ
    """
    temp_values = Context()
    page=1
    span = 15
    if request.GET.has_key('page'):
        page = int(request.GET['page'])
    if request.GET.has_key('span'):
        span = int(request.GET['span'])
    authors,entry_count = Author.get_items(span=span, page=page, order="-created_at")
    print authors
    page_list,pages = get_page_list(page, entry_count, span)
    temp_values = {
        "target":"author",
        "title":u"製作者(著者)一覧ページ",
        "authors":authors,
        "page_list":page_list,
        "pages":pages,
        }
    return render_to_response('author/index.html',temp_values,
                              context_instance=RequestContext(request))

def main():
    pass


if __name__ == '__main__':
    main()
    

