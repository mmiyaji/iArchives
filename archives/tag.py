#!/usr/bin/env python
# encoding: utf-8
"""
tag.py

Created by mmiyaji on 2012-11-22.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from views import *

def home(request):
    """
    Case of GET REQUEST '/tag/'
    tagの一覧を表示するページ
    """
    temp_values = Context()
    page=1
    span = 30
    order = "-created_at"
    tags,entry_count = Tag.get_items(span=span, page=page)
    page_list,pages = get_page_list(page, entry_count, span)
    temp_values = {
        "target":"tag",
        "title":u"グループ一覧ページ",
        "tags":tags,
        "page_list":page_list,
        "pages":pages,
        }
    return render_to_response('tag/index.html',temp_values,
                              context_instance=RequestContext(request))
def detail(request, tag_id):
    """
    Case of GET REQUEST '/tag/<tag_id>/'
    著者詳細を表示するページ
    """
    temp_values = Context()
    page=1
    span = 30
    search_query = None
    tag = Tag.get_by_id(tag_id)
    if not tag:
        # 見つからない場合は404エラー送出
        raise Http404
    temp_values = {
        "target":"tag",
        "title":u"著者詳細[ %s ]" % tag.name,
        "tag":tag,
        "subscroll":True,
        "datepicker":"datepicker",
        }
    return render_to_response('tag/detail.html',temp_values,
                              context_instance=RequestContext(request))
@csrf_protect
@login_required
def meiboadd(request):
    """
    Case of UPDATE REQUEST '/tag/meibo/add/'
    著者の一括登録
    UPDATE/POST リクエストにのみレスポンス
    """
    request_type = request.method
    logger.debug(request_type)
    if request_type == 'GET':
        raise Http404
    elif request_type == 'OPTION' or request_type == 'HEAD':
        return HttpResponse("OK")
    elif request_type == 'POST' or request_type == 'UPDATE':
        # グループ名,よみがな の形式で入力
        meibo = request.POST['meibo']
        # 行ごとに分割
        meibos = meibo.split("\n")
        for m in meibos:
            # カンマ区切り に分割
            element = m.split(",")
            if not element:
                continue
            if not element[0]:
                continue
            tag = Tag.get_by_name(element[0].strip())
            if not tag:
                tag = Tag()
                tag.name = element[0].strip()
                if len(element) > 1:
                    tag.roman = element[1].strip()
                tag.save()
        return HttpResponseRedirect("/tag/")
    else:
        raise Http404

@csrf_protect
@login_required
def update(request, tag_id):
    """
    Case of UPDATE REQUEST '/tag/<tag_id>/update/'
    対象著者の更新
    UPDATE/POST リクエストにのみレスポンス
    """
    request_type = request.method
    logger.debug(request_type)
    if request_type == 'GET':
        raise Http404
    elif request_type == 'OPTION' or request_type == 'HEAD':
        return HttpResponse("OK")
    elif request_type == 'POST' or request_type == 'UPDATE':
        # tag_idからTagを取得
        tag = Tag.get_by_id(tag_id)
        if not tag:
            # 見つからない場合は404エラー送出
            raise Http404
        # 必要なリクエストパラメータを変数に抽出
        param = {
            "name":request.POST['name'],
            "roman":request.POST['roman'],
            }
        if param['name']:
            tag.name = param['name']
        if param['roman']:
            tag.roman = param['roman']
        tag.save()
        # 元のページにリダイレクト ブラウザのキャッシュで更新されてない画面が出るのを防止
        return HttpResponseRedirect("/tag/%s/?update=%d" % (tag_id, datetime.datetime.now().microsecond))
    else:
        raise Http404
@csrf_protect
@login_required
def delete(request, tag_id):
    """
    Case of DELETE REQUEST '/tag/<tag_id>/delete/'
    対象画像の削除
    DELETE リクエストにのみレスポンス
    """
    request_type = request.method
    logger.debug(request_type)
    if request_type == 'GET':
        raise Http404
    elif request_type == 'OPTION' or request_type == 'HEAD':
        return HttpResponse("OK")
    elif request_type == 'POST' or request_type == 'DELETE':
        # idからTagを取得
        tag = Tag.get_by_id(tag_id)
        if not tag:
            # 見つからない場合は404エラー送出
            raise Http404
        tag.delete()
        return HttpResponseRedirect("/tag/")

def main():
    pass


if __name__ == '__main__':
    main()

