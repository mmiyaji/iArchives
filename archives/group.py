#!/usr/bin/env python
# encoding: utf-8
"""
group.py

Created by mmiyaji on 2012-11-20.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from views import *

def home(request):
    """
    Case of GET REQUEST '/group/'
    グループの一覧を表示するページ
    """
    temp_values = Context()
    page=1
    span = 30
    order = "-created_at"
    groups,entry_count = Group.get_items(span=span, page=page)
    page_list,pages = get_page_list(page, entry_count, span)
    temp_values = {
        "target":"group",
        "title":u"グループ一覧ページ",
        "groups":groups,
        "page_list":page_list,
        "pages":pages,
        }
    return render_to_response('group/index.html',temp_values,
                              context_instance=RequestContext(request))
def detail(request, group_id):
    """
    Case of GET REQUEST '/group/<group_id>/'
    著者詳細を表示するページ
    """
    temp_values = Context()
    page=1
    span = 30
    search_query = None
    group = Group.get_by_id(group_id)
    if not group:
        # 見つからない場合は404エラー送出
        raise Http404
    temp_values = {
        "target":"group",
        "title":u"著者詳細[ %s ]" % group.name,
        "group":group,
        "subscroll":True,
        "datepicker":"datepicker",
        }
    return render_to_response('group/detail.html',temp_values,
                              context_instance=RequestContext(request))
@csrf_protect
@login_required
def meiboadd(request):
    """
    Case of UPDATE REQUEST '/group/meibo/add/'
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
            group = Group.get_by_name(element[0].strip())
            if not group:
                group = Group()
                group.name = element[0].strip()
                if len(element) > 1:
                    group.roman = element[1].strip()
                group.save()
        return HttpResponseRedirect("/group/")
    else:
        raise Http404

@csrf_protect
@login_required
def update(request, group_id):
    """
    Case of UPDATE REQUEST '/group/<group_id>/update/'
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
        # group_idからGroupを取得
        group = Group.get_by_id(group_id)
        if not group:
            # 見つからない場合は404エラー送出
            raise Http404
        # 必要なリクエストパラメータを変数に抽出
        param = {
            "name":request.POST['name'],
            "roman":request.POST['roman'],
            }
        if param['name']:
            group.name = param['name']
        if param['roman']:
            group.roman = param['roman']
        group.save()
        # 元のページにリダイレクト ブラウザのキャッシュで更新されてない画面が出るのを防止
        return HttpResponseRedirect("/group/%s/?update=%d" % (group_id, datetime.datetime.now().microsecond))
    else:
        raise Http404

def main():
    pass


if __name__ == '__main__':
    main()

