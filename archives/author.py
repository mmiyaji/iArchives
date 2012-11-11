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
    order = "-created_at"
    search_query = None
    admitted_query = None
    search_option = ""
    sort_option = ""
    s_option = ""
    s_type = ""
    sort_type = False # ordering type flag. False -> DESC, True -> ASC
    query_type = False # Search type flag. False -> OR, True -> AND
    if request.GET.has_key('page'):
        page = int(request.GET['page'])
    if request.GET.has_key('span'):
        span = int(request.GET['span'])
    if request.GET.has_key('q'):
        search_query = request.GET['q'].strip().replace(u"　", " ").split(" ")
        search_option += "q=%s&amp;" % "+".join(search_query)
    if request.GET.has_key('a'):
        try: # int キャストで失敗したらすべての年度生を返す
            admitted = int(request.GET['a'])
            if admitted is not 0:
                admitted_query = admitted
                search_option += "a=%s&amp;" % admitted_query
        except:
            pass
    if request.GET.has_key('qt'):
        if request.GET['qt']:
            query_type = True
            search_option += "qt=1&amp;"
    if request.GET.has_key('s'):
        # 同じクエリがきた場合、後を優先する
        sort_option = request.GET.getlist('s')[-1]
        search_option += "s=%s&amp;" % sort_option
        if sort_option == "name":
            order = "-name"
            s_option = u"氏名"
        elif sort_option == "id": # sort as STRINGS
            order = "-student_id"
            s_option = u"学籍番号"
        elif sort_option == "update":
            order = "-updated_at"
            s_option = u"更新日"
    if request.GET.has_key('st'):
        # 同じクエリがきた場合、後を優先する
        try: # キャストで失敗したら降順表示
            if int(request.GET.getlist('st')[-1]):
                order = order.lstrip("-")
                # sort_type = True
                search_option += "st=1&amp;"
                s_type = u"昇順"
        except:
            pass
    authors,entry_count = Author.get_items(span=span, page=page, search_query=search_query,
                                           admitted_query=admitted_query, query_type=query_type,
                                           order=order)
    page_list,pages = get_page_list(page, entry_count, span)
    temp_values = {
        "target":"author",
        "title":u"製作者(著者)一覧ページ",
        "authors":authors,
        "auth_years":Author.get_years(),
        "page_list":page_list,
        "pages":pages,
        "search_query":search_query,
        "admitted_query":admitted_query,
        "query_type" : query_type,
        "search_option" : search_option,
        "sort_option": s_option,
        "sort_type": s_type,
        }
    return render_to_response('author/index.html',temp_values,
                              context_instance=RequestContext(request))
def detail(request, author_id):
    """
    Case of GET REQUEST '/author/<author_id>/'
    著者詳細を表示するページ
    """
    temp_values = Context()
    page=1
    span = 30
    search_query = None
    author = Author.get_by_student_id(author_id)
    if not author:
        # 見つからない場合は404エラー送出
        raise Http404
    if request.GET.has_key('page'):
        page = int(request.GET['page'])
    if request.GET.has_key('span'):
        span = int(request.GET['span'])
    if request.GET.has_key('search_query'):
        search_query = request.GET['search_query'].replace(u"　", " ").split(" ")
    files,entry_count = author.get_photos(span=span, page=page, search_query=search_query)
    page_list,pages = get_page_list(page, entry_count, span)
    temp_values = {
        "target":"author",
        "title":u"著者詳細[ %s ]" % author.name,
        "author":author,
        "files":files,
        "page_list":page_list,
        "pages":pages,
        "search_query":search_query,
        "subscroll":True,
        "datepicker":"datepicker",
        }
    return render_to_response('author/detail.html',temp_values,
                              context_instance=RequestContext(request))
@csrf_protect
def meiboadd(request):
    """
    Case of UPDATE REQUEST '/author/meibo/add/'
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
        # 学籍番号,名前のよみ,氏名,ニックネーム, の形式で入力
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
            author = Author.get_by_student_id(element[0].strip())
            if not author:
                author = Author()
                author.student_id = element[0].strip()
                adate = None
                try:
                    # せめて数字かどうかチェック それ以外なら今日の日付を入力
                    ayear = int(element[0].strip()[:4])
                    adate = date_validate(str(ayear)+"-04-01")
                except:
                    pass
                if not adate:
                    adate = datetime.datetime.now()
                author.admitted_at = adate
                if len(element) > 1:
                    author.roman = element[1].strip()
                if len(element) > 2:
                    author.name = element[2].strip()
                if len(element) > 3:
                    author.nickname = element[3].strip()
                author.save()
        return HttpResponseRedirect("/author/")
    else:
        raise Http404

@csrf_protect
def update(request, author_id):
    """
    Case of UPDATE REQUEST '/author/<author_id>/update/'
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
        # author_idからAuthorを取得
        author = Author.get_by_student_id(author_id)
        if not author:
            # 見つからない場合は404エラー送出
            raise Http404
        # 必要なリクエストパラメータを変数に抽出
        param = {
            "name":request.POST['name'],
            "roman":request.POST['roman'],
            "student_id":request.POST['student_id'],
            "admitted_year":request.POST['admitted_year'],
            "nickname":request.POST['nickname'],
            }
        if param['name']:
            author.name = param['name']
        if param['roman']:
            author.roman = param['roman']
        if param['student_id']:
            author.student_id = param['student_id']
            adate = None
            try:
                adate = date_validate(param['admitted_year'].replace(u"　",u" ").strip()+"-04-01")
            except:
                pass
            author.admitted_at = adate
        if param['nickname']:
            author.nickname = param['nickname']
        author.save()
        # 元のページにリダイレクト ブラウザのキャッシュで更新されてない画面が出るのを防止
        return HttpResponseRedirect("/author/%s/?update=%d" % (param['student_id'], datetime.datetime.now().microsecond))
    else:
        raise Http404

def main():
    pass


if __name__ == '__main__':
    main()

