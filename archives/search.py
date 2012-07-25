#!/usr/bin/env python
# encoding: utf-8
"""
search.py

Created by mmiyaji on 2012-07-25.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

from views import *
import re
def home(request):
    """
    Case of GET REQUEST '/search/'
    検索用のフォームを表示するページ
    """
    temp_values = Context()
    page=1
    span = 15
    if request.GET.has_key('page'):
        page = int(request.GET['page'])
    if request.GET.has_key('span'):
        span = int(request.GET['span'])
    # photos,entry_count = Photo.get_items(span=span, page=page, order="-created_at")
    # print photos
    # page_list,pages = get_page_list(page, entry_count, span)
    # temp_values = {
    #     "target":"photo",
    #     "title":u"写真一覧ページ",
    #     "photos":photos,
    #     "page_list":page_list,
    #     "pages":pages,
    #     }
    return render_to_response('photo/index.html',temp_values,
                              context_instance=RequestContext(request))

def author(request):
    """
    Case of GET REQUEST '/search/author/'
    著者検索結果を表示するページ
    """
    temp_values = Context()
    # photo = Photo.get_by_uuid(photo_uuid)
    # if not photo:
    #     # 見つからない場合は404エラー送出
    #     raise Http404
    # temp_values = {
    #     "target":"photo",
    #     "title":u"写真詳細[ %s ]" % photo.title,
    #     "photo":photo,
    #     "subscroll":True,
    #     "datepicker":"datepicker",
    #     }
    return render_to_response('photo/index.html',temp_values,
                              context_instance=RequestContext(request))

def main():
    pass


if __name__ == '__main__':
    main()
    

