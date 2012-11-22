#!/usr/bin/env python
# encoding: utf-8
"""
move_tool.py

Created by mmiyaji on 2012-11-22.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'iArchives.settings'
from iArchives.settings import *
from archives.views import *
from archives.scan import Scanner

def update_image(authors, image_url, j):
    """
    Arguments:
    - `authors`:
    - `path`:
    - `name`:
    """
    orientation = None
    if True:
        print "full path: ",image_url
        if True:
            scan = Scanner(image_url)
            exif = scan.scanExif()
            try:
                if exif:
                    if exif.has_key(36867):
                        # DateTimeOriginal
                        published_at = date_validate(exif[36867], "%Y:%m:%d %H:%M:%S")
                    elif exif.has_key(36868):
                        # DateTimeDigitized
                        published_at = date_validate(exif[36868], "%Y:%m:%d %H:%M:%S")
                    elif exif.has_key(306):
                        # DateTime
                        published_at = date_validate(exif[306], "%Y:%m:%d %H:%M:%S")
                    else:
                        # now
                        published_at = date_validate("%s-04-01" % year)
                else:
                    published_at = datetime.datetime.now()
            except:
                published_at = datetime.datetime.now()
            try:
                if exif.has_key(274):
                    orientation = int(exif[274])
            except:
                pass
            print "published at: ", published_at
            print "orientation: ", orientation
            alltag = []
            photo = Photo.get_by_pub_and_name(published_at, j)
            if photo:
                print "photo is already istalled"
                return 0
            else:
                photo = Photo()
            photo.caption = j.split(".")[0]
            if orientation:
                photo.orientation = orientation
            photo.published_at = published_at
            photo.save(isFirst = True)
            name = force_unicode(photo.published_at.strftime((smart_str("%Y%m%d%H%M%S_"+str(photo.id).zfill(5)+"."+j.split(".")[-1]))))
            photo.title = name
            from django.core.files import File
            image = File(open(image_url))
            print image,image.size,name
            photo.image = image
            photo.original_title = j
            for a in authors:
                photo.authors.add(a)
            photo.tag.clear()
            tags = ""
            if alltag:
                for t in alltag:
                    tt = Tag.get_by_id(t)
                    photo.tag.add(tt)
                    tags += "%s," % tt.name
            photo.save()

def main():
    args = sys.argv
    rootpath = args[1]
    print "root directory: ",rootpath
    print "user list: ",
    for i in os.listdir(rootpath): print i,
    year = rootpath.rstrip("/").split("/")[-1]
    users_list = os.listdir(rootpath)
    print
    for i in users_list:
        if i.count("-") > 0:
            id,no = i.split("-",1)
        else:
            id = i.strip()
            no = "no name"
        print "#######"
        print "ID: ", id
        print "name: ", no
        author = Author.get_by_student_id(id)
        if author:
            print "found on database: ", author
            image_list = os.listdir(os.path.join(rootpath,i))
            print "image list: ", image_list
            for j in image_list:
                print "----"
                image_url = os.path.join(rootpath,i, j)
                print "full path: ",image_url
                update_image([author],image_url,j)

def update_all():
    all = Photo.objects.all()
#    c = len(allobj)
#    span = 50
#    step = c/50
#    for j in range(0,step):
#        all = allobj[j*span:(j+1)*span]
    if True:
        for i in all:
            if i.image:
                orientation = 1
                print i
                if i.orientation > 0:
                    print "skip"
                    continue
                image_url = i.image.path
                scan = Scanner(image_url)
                exif = scan.scanExif()
                try:
                    if exif.has_key(274):
                        orientation = int(exif[274])
                except:
                    pass
                print "orientation: ", orientation
                try:
                    i.orientation = orientation
                    i.save()
                except:
                    print "error"
if __name__ == '__main__':
    # main()
    update_all()

