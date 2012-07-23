#!/usr/bin/env python
# encoding: utf-8
"""
photo.py

Created by mmiyaji on 2012-07-18.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from views import *

def home(request):
    """
    Case of GET REQUEST '/photo/'
    画像の一覧を表示するページ
    """
    temp_values = Context()
    return render_to_response('photo/index.html',temp_values,
                              context_instance=RequestContext(request))

def detail(request, photo_uuid):
    """
    Case of GET REQUEST '/photo/<photo_uuid>/'
    個別の画像の詳細を表示するページ
    """
    temp_values = Context()
    photo = Photo.get_by_uuid(photo_uuid)
    if not photo:
        # 見つからない場合は404エラー送出
        raise Http404
    temp_values = {
        "photo":photo,
        "subscroll":True,
        "datepicker":"datepicker",
        }
    return render_to_response('photo/index.html',temp_values,
                              context_instance=RequestContext(request))

def delete(request, photo_uuid):
    """
    Case of DELETE REQUEST '/photo/<photo_uuid>/delete/'
    対象画像の削除
    DELETE リクエストにのみレスポンス
    """

def update(request, photo_uuid):
    """
    Case of UPDATE REQUEST '/photo/<photo_uuid>/update/'
    対象画像の更新
    UPDATE リクエストにのみレスポンス
    """

def main():
    pass


if __name__ == '__main__':
    main()


