#!/usr/bin/env python
# encoding: utf-8
"""
archive.py

Created by mmiyaji on 2012-07-25.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from views import *
import re
import zipfile
def home(request):
    """
    Case of GET REQUEST '/archive/'
    アーカイブ化(ダウンロード)の設定ページ
    """
    temp_values = Context()
    page=1
    span = 15
    if request.GET.has_key('page'):
        page = int(request.GET['page'])
    if request.GET.has_key('span'):
        span = int(request.GET['span'])
    photos,entry_count = Photo.get_items(span=span, page=page, order="-created_at")
    print photos
    page_list,pages = get_page_list(page, entry_count, span)
    temp_values = {
        "target":"archive",
        "title":u"アーカイブ化",
        "photos":photos,
        "page_list":page_list,
        "pages":pages,
        }
    return render_to_response('archive/index.html',temp_values,
                              context_instance=RequestContext(request))

def authors(request):
    """
    Case of GET REQUEST '/archive/author/'
    著者アーカイブ化(ダウンロード)ページ
    """
    temp_values = Context()
    request_type = request.method
    if request_type == 'GET':
        page=1
        span = 100
        search_query = None
        admitted_query = None
        if request.GET.has_key('page'):
            page = int(request.GET['page'])
        if request.GET.has_key('span'):
            span = int(request.GET['span'])
        if request.GET.has_key('q'):
            search_query = request.GET['q'].replace(u"　", " ").split(" ")
        if request.GET.has_key('a'):
            admitted_query = int(request.GET['a'])
        authors,entry_count = Author.get_items(span=span, page=page, search_query=search_query, admitted_query=admitted_query, order="-created_at")
        print authors
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
            }
        return render_to_response('archive/authors.html',temp_values,
                              context_instance=RequestContext(request))
    else:
        ziplist = []
        exportlist = []
        # アーカイブ対象のユーザIDが入ったリスト
        isarchive = request.POST.getlist('isarchive')
        # ディレクトリ構造
        archive_type = int(request.POST['archive_type'])
        # ファイル名
        archive_filename = int(request.POST['archive_filename'])
        # zipファイル名
        archive_zipfile = request.POST['archive_zipfile']
        filename = replace_validname(force_unicode(archive_zipfile)) #"archive_"+author.student_id
        for i in isarchive:
            author = Author.get_by_student_id(i)
            if not author:
                continue
            zip_filename = replace_validname(force_unicode(i))
            print zip_filename
            files,entry_count = author.get_photos(all=True, listvalue="uuid")
            z = createZip(list(files[0]), archive_type, archive_filename, zip_filename)
            filepath = os.path.join(settings.MEDIA_URL, settings.EXPORT_PATH, zip_filename+".zip")
            ziplist.append(filepath)
            exportlist.append(zip_filename+".zip")
        all_filepath = os.path.join(settings.EXPORT_URL, filename+".zip")
        filepath = os.path.join(settings.MEDIA_URL, settings.EXPORT_PATH, filename+".zip")
        execZip(ziplist, exportlist, filepath)
        return HttpResponseRedirect(all_filepath)
def author(request, author_id):
    """
    Case of GET REQUEST '/archive/author/<author_id>/'
    アーカイブページ
    """
    temp_values = Context()
    author = Author.get_by_student_id(author_id)
    if not author:
        # 見つからない場合は404エラー送出
        raise Http404
    request_type = request.method
    logger.debug(request_type)
    print request_type
    if request_type == 'GET':
        files,entry_count = author.get_photos(all=True)
        page_list,pages = get_page_list(1, entry_count, 10000)
        temp_values = {
            "target":"author",
            "title":u"アーカイブページ[ %s ]" % author.name,
            "author":author,
            "files":files,
            "page_list":page_list,
            "pages":pages,
            "subscroll":True,
            }
        return render_to_response('archive/author_detail.html',temp_values,
                              context_instance=RequestContext(request))
    else:
        # アーカイブ対象の写真UUIDが入ったリスト
        isarchive = request.POST.getlist('isarchive')
        # ディレクトリ構造
        archive_type = int(request.POST['archive_type'])
        # ファイル名
        archive_filename = int(request.POST['archive_filename'])
        # zipファイル名
        archive_zipfile = request.POST['archive_zipfile']
        return HttpResponseRedirect(createZip(isarchive, archive_type, archive_filename, archive_zipfile))

def createZip(isarchive, archive_type, archive_filename, archive_zipfile):
    """
    """
    filename = replace_validname(force_unicode(archive_zipfile)) #"archive_"+author.student_id
    dir_type = "/%Y/%m/%d/"
    if archive_type == 1:
        dir_type = "/%Y/%m/%d/"
    elif archive_type == 2:
        dir_type = "/%Y/%m/"
    elif archive_type == 3:
        dir_type = "/%Y/"
    elif archive_type == 4:
        dir_type = "/"
    photos = []
    fileList = []
    exportPath = []
    for i in isarchive:
        p = Photo.get_by_uuid(i)
        if p:
            photos.append(p)
            fileList.append(p.image.path)
            title = ""
            if archive_filename == 1:
                title = p.title
            elif archive_filename == 2:
                title = p.original_title
            else:
                if p.caption:
                    title = p.caption + "." +p.title.split(".")[-1]
                    title = replace_validname(title)
                else:
                    title = p.title
            exportPath.append(filename+p.published_at.strftime(dir_type)+title)
    print photos,fileList,exportPath
    filepath = os.path.join(settings.MEDIA_URL, settings.EXPORT_PATH, filename+".zip")
    execZip(fileList, exportPath, filepath)
    return os.path.join(settings.EXPORT_URL, filename+".zip")

def years(request):
    pass
def year(request, year):
    pass

def execZip(fileList, exportPath, filename):
    # 指定したファイル群をzipに圧縮する
    # execZip(["/Users/mmiyaji/tmp/sc.JPG","/Users/mmiyaji/tmp/sc.psd","/Users/mmiyaji/tmp/scs.jpg"], ["a/sc.JPG","a/psd/sc.psd","a/scs.JPG"],"exporttest.zip")
    z = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    for l,p in zip(fileList, exportPath):
        z.write(force_unicode(l).encode('cp932'), p.encode('cp932'))
    z.close()
    return filename

def detail(request, photo_uuid):
    """
    Case of GET REQUEST '/archive/<photo_uuid>/'
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
        "subscroll":True,
        "datepicker":"datepicker",
        }
    return render_to_response('photo/detail.html',temp_values,
                              context_instance=RequestContext(request))


def main():
    pass


if __name__ == '__main__':
    main()

