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
    page=1
    span = 15
    order = "-created_at"
    search_query = None
    admitted_query = None
    published_query = None
    tag_queries = []
    search_target = 0
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
        search_option += "q=%s&" % "+".join(search_query)
    if request.GET.has_key('a'):
        try: # int キャストで失敗したらすべての年度生を返す
            admitted = int(request.GET['a'])
            if admitted is not 0:
                admitted_query = admitted
                search_option += "a=%s&" % admitted_query
        except:
            pass
    if request.GET.has_key('p'):
        try: # int キャストで失敗したらすべての年度の写真を返す
            published = int(request.GET['p'])
            if published is not 0:
                published_query = published
                search_option += "p=%s&" % published_query
        except:
            pass
    if request.GET.has_key('t'):
        try: # int キャストで失敗したらすべての年度生を返す
            t = int(request.GET['t'])
            if t is not 0:
                search_target = t
                search_option += "t=%s&" % search_target
        except:
            pass
    if request.GET.has_key('qt'):
        if request.GET['qt']:
            query_type = True
            search_option += "qt=1&"
    if request.GET.has_key('s'):
        # 同じクエリがきた場合、後を優先する
        sort_option = request.GET.getlist('s')[-1]
        search_option += "s=%s&" % sort_option
        if sort_option == "name":
            order = "-name"
            s_option = u"氏名"
        elif sort_option == "id": # sort as STRINGS
            order = "-student_id"
            s_option = u"学籍番号"
        elif sort_option == "update":
            order = "-updated_at"
            s_option = u"更新日"
    if request.GET.has_key('tag'):
        tg = request.GET.getlist('tag')
        if u"0" in tg:
            tg = []
        for t in tg:
            try:
                tag_queries.append(int(t))
                search_option += "tag=%s&" % t
            except:
                pass
    if request.GET.has_key('st'):
        # 同じクエリがきた場合、後を優先する
        try: # キャストで失敗したら降順表示
            if int(request.GET.getlist('st')[-1]):
                order = order.lstrip("-")
                # sort_type = True
                search_option += "st=1&"
                s_type = u"昇順"
        except:
            pass
    photos,entry_count = Photo.get_items(span=span, page=page, search_query=search_query,
                                         admitted_query=admitted_query, published_query=published_query, query_type=query_type,
                                         search_target=search_target, tag_queries=tag_queries,
                                         order=order)
    page_list,pages = get_page_list(page, entry_count, span)
    temp_values = {
        "target":"photo",
        "title":u"写真一覧ページ",
        "photos":photos,
        "tags":Tag.get_all(),
        "pub_years":Photo.get_years(),
        "page_list":page_list,
        "pages":pages,
        "search_query":search_query,
        "admitted_query":admitted_query,
        "published_query":published_query,
        "tag_queries":tag_queries,
        "query_type" : query_type,
        "search_option" : search_option,
        "sort_option": s_option,
        "sort_type": s_type,
        "search_target": search_target,
        }
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
        "target":"photo",
        "title":u"写真詳細[ %s ]" % photo.title,
        "photo":photo,
        "recent_authors":Author.objects.order_by("-updated_at").all()[:100],
        "subscroll":True,
        "datepicker":"datepicker",
        }
    return render_to_response('photo/detail.html',temp_values,
                              context_instance=RequestContext(request))

@csrf_protect
def delete(request, photo_uuid):
    """
    Case of DELETE REQUEST '/photo/<photo_uuid>/delete/'
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
        # uuidからPhotoを取得
        photo = Photo.get_by_uuid(photo_uuid)
        if not photo:
            # 見つからない場合は404エラー送出
            raise Http404
        photo.delete()
        return HttpResponseRedirect("/photo/")
@csrf_protect
def update(request, photo_uuid):
    """
    Case of UPDATE REQUEST '/photo/<photo_uuid>/update/'
    対象画像の更新
    UPDATE/POST リクエストにのみレスポンス
    """
    request_type = request.method
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
            "tag":request.POST['tag'],
            "pubdate":request.POST['pubdate'],
            }
        # author登録
        photo.authors.clear()
        for i in param['authors'].split(','):
            aid = re.sub('\(.*\)','',i.replace(u"　"," ").strip())
            aname = ''
            a = re.search('\(.*\)', i.strip())
            if a:
                aname = a.group(0).replace('(','').replace(')','').replace(u"　"," ").strip()
            if aid:
                author = Author.get_by_student_id(aid)
                if not author:
                    author = Author()
                    author.name = aname
                    author.student_id = aid
                    adate = None
                    try:
                        adate = date_validate(aid[:4]+"-04-01")
                    except:
                        pass
                    author.admitted_at = adate
                    author.save()
                photo.authors.add(author)
        # tag登録
        photo.tag.clear()
        for i in param['tag'].split(','):
            t = i.strip()
            if t:
                tag = Tag.get_by_name(t)
                if tag:
                    photo.tag.add(tag)
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
        # 元のページにリダイレクト ブラウザのキャッシュで更新されてない画面が出るのを防止
        return HttpResponseRedirect("/photo/%s/?update=%d" % (photo_uuid, datetime.datetime.now().microsecond))
    else:
        raise Http404

def main():
    pass


if __name__ == '__main__':
    main()


