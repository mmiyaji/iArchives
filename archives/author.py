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
    span = 30
    search_query = None
    if request.GET.has_key('page'):
        page = int(request.GET['page'])
    if request.GET.has_key('span'):
        span = int(request.GET['span'])
    if request.GET.has_key('search_query'):
        search_query = request.GET['search_query'].replace(u"　", " ").split(" ")
    authors,entry_count = Author.get_items(span=span, page=page, search_query=search_query, order="-created_at")
    print authors
    page_list,pages = get_page_list(page, entry_count, span)
    temp_values = {
        "target":"author",
        "title":u"製作者(著者)一覧ページ",
        "authors":authors,
        "page_list":page_list,
        "pages":pages,
        "search_query":search_query,
        }
    return render_to_response('author/index.html',temp_values,
                              context_instance=RequestContext(request))
def detail(request, author_id):
    """
    Case of GET REQUEST '/author/<author_id>/'
    著者詳細を表示するページ
    """
    temp_values = Context()
    author = Author.get_by_student_id(author_id)
    if not author:
        # 見つからない場合は404エラー送出
        raise Http404
    temp_values = {
        "target":"author",
        "title":u"著者詳細[ %s ]" % author.name,
        "author":author,
        "files":author.get_photos(),
        "subscroll":True,
        "datepicker":"datepicker",
        }
    return render_to_response('author/detail.html',temp_values,
                              context_instance=RequestContext(request))

def main():
    pass


if __name__ == '__main__':
    main()

