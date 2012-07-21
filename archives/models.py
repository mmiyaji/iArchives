#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by mmiyaji on 2012-07-16.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

import sys, os, datetime, uuid
from django.db import models
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings
from django.utils.encoding import force_unicode, smart_str
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile

class Author(models.Model):
    """
    """
    name = models.CharField(max_length = 100, default="", blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    roman = models.CharField(max_length=255, blank=True, null=True)
    student_id = models.CharField(max_length = 100, default="", blank=True, null=True, unique=True)
    ROLL_CHOICES = (
        ('s','Student'),
        ('t','Teacher'),
        ('g','Graduated'),
        ('e','Etcetera'),
        )
    roll = models.CharField(max_length=10, choices=ROLL_CHOICES, default="s")
    admitted_at = models.DateTimeField(blank=True, null=True)
    graduated_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)
    @staticmethod
    def get_by_student_id(keyid=""):
        result=None
        try:
            result = Author.objects.get(student_id__exact=keyid.strip())
        except:
            result = None
        return result

    def __str__(self):
        return "%s" % (self.name)
    def __unicode__(self):
        return self.name

def get_origin_photo_upload_path(self, filename):
    return get_photo_upload_path(self, filename, types="originals")
def get_thumb_photo_upload_path(self, filename):
    return get_photo_upload_path(self, filename, types="thumbs")
def get_photo_upload_path(self, filename, types="originals"):
    root_path = "archives/"+types+"/%Y/%m/%d/"
    now = self.published_at
    # user_path =  os.path.join(settings.MEDIA_ROOT, force_unicode(now.strftime(smart_str(root_path))))
    user_path = force_unicode(now.strftime(smart_str(root_path)))
    # name = force_unicode(now.strftime((smart_str("%Y%m%d%H%M%S_"+str(self.id).zfill(5)+"."+filename.split(".")[-1]))))
    if types == "originals":
        # at the case of originals, set title
        name = self.title
        # self.title = name
        print "origin: ", name, os.path.splitext(os.path.basename(self.title))[0]
    else:
        name = os.path.splitext(os.path.basename(self.title))[0]+"."+filename.split(".")[-1]
        print "thumbs: ",name
    return os.path.join(user_path, name)

class Photo(models.Model):
    authors = models.ManyToManyField(Author, blank=True, null=True)
    uuid = models.CharField(max_length = 32, unique = True, default=uuid.uuid4().hex)
    title = models.CharField(max_length = 100, default="", blank=True, null=True)
    original_title = models.CharField(max_length = 100, default="", blank=True, null=True)
    image = models.ImageField(upload_to=get_origin_photo_upload_path,
                              width_field="image_width",
                              height_field="image_height",
                              blank=True, null=True
                              )
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to=get_thumb_photo_upload_path,
                                  width_field="thumbnail_width",
                                  height_field="thumbnail_height",
                                  blank=True, null=True
                                  )
    thumbnail_width = models.IntegerField(blank=True, null=True)
    thumbnail_height = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length = 250, default="", blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)

    @staticmethod
    def get_by_pub_and_title(pup, title):
        result = None
        try:
            result = Photo.objects.filter(published_at__exact=pub).filter(title__exact=title)
        except:
            result = None
    def __str__(self):
        # aname = ""
        # for i in self.author:
        #     aname += i.name +", "
        # return "%s owner: %s" % (self.title, aname)
        return self.title
    def __unicode__(self):
        return self.title
    def save(self, force_update=False, force_insert=False, thumb_size=(180,300), isFirst = False):
        if not self.uuid:
            self.uuid = uuid.uuid4().hex
        if isFirst:
            super(Photo, self).save(force_update, force_insert)
        else:
            image = Image.open(self.image)
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')
            # save the original size
            self.image_width, self.image_height = image.size
            image.thumbnail(thumb_size, Image.ANTIALIAS)
            # save the thumbnail to memory
            temp_handle = StringIO()
            image.save(temp_handle, 'png')
            temp_handle.seek(0) # rewind the file
            # save to the thumbnail field
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                     temp_handle.read(),
                                     content_type='image/png')
            self.thumbnail.save(suf.name+'.png', suf, save=False)
            self.thumbnail_width, self.thumbnail_height = image.size
            # save the image object
            super(Photo, self).save(force_update, force_insert)

class Meta:
    ordering = ['-create_at']
