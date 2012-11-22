#!/usr/bin/env python
# encoding: utf-8
"""
move_tool.py

Created by mmiyaji on 2012-11-22.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from settings import *
from iArchives.archives.views import *
from archives.scan import Scanner

def main():
    args = sys.argv
    rootpath = args[1]
    print rootpath,os.listdir(rootpath)
    year = rootpath.rstrip("/").split("/")[-1]
    print year
    users_list = os.listdir(rootpath)
    print users_list
    for i in users_list:
        id,no = i.split("-",1)
        # print id,no
        author = Author.get_by_student_id(id)
        if True:
            image_list = os.listdir(os.path.join(rootpath, year))
            print "#######",os.path.join(rootpath, year)
            for j in image_list:
                image_url = os.listdir(os.path.join(rootpath, year, j))
                scan = Scanner(image_url)
                exif = scan.scanExif()
                print image_url
if __name__ == '__main__':
    main()


