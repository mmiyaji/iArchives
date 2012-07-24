#!/usr/bin/env python
# encoding: utf-8
"""
photo.py

Created by mmiyaji on 2012-07-18.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from views import *
import re
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

@csrf_protect
def update(request, photo_uuid):
    """
    Case of UPDATE REQUEST '/photo/<photo_uuid>/update/'
    対象画像の更新
    UPDATE/POST リクエストにのみレスポンス
    """
    request_type = request.method
    print request_type
    logger.debug(request_type)
    if request_type == 'GET':
        raise Http404
    elif request_type == 'OPTION' or request_type == 'HEAD':
        return HttpResponse("OK")
    elif request_type == 'POST' or request_type == 'UPDATE':
        # uuidからPhotoを取得
        photo = Photo.get_by_uuid(photo_uuid)
        if not photo:
            # 見つからない場合は404エラー送出
            raise Http404
        # 必要なリクエストパラメータを変数に抽出
        param = {
            "authors":request.POST['authors'],
            "caption":request.POST['caption'],
            "comment":request.POST['comment'],
            "pubdate":request.POST['pubdate'],
            }
        print param
        # author登録
        photo.authors.clear()
        for i in param['authors'].split(','):
            aid = re.sub('\(.*\)','',i.strip())
            aname = ''
            a = re.search('\(.*\)', i.strip())
            if a:
                aname = a.group(0).replace('(','').replace(')','').strip()
            if aid:
                author = Author.get_by_student_id(aid)
                if not author:
                    author = Author()
                    author.name = aname
                    author.student_id = aid
                    author.save()
                photo.authors.add(author)
        if param['caption']:
            photo.caption = param['caption']
        if param['comment']:
            photo.comment = param['comment']
        if param['pubdate']:
            p = date_validate(param['pubdate'])
            if p:
                # 年月日のみ更新
                photo.published_at = photo.published_at.replace(year=p.year, month=p.month, day=p.day)
        photo.save()
        return HttpResponseRedirect("/photo/%s/" % (photo_uuid))
    else:
        raise Http404

def main():
    pass


if __name__ == '__main__':
    main()


