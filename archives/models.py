#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by mmiyaji on 2012-07-16.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

import sys
import os
from django.db import models
from django.db.models import Q
from django.core.cache import cache

from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile

class Photo(models.Model):
    author_name = models.CharField(max_length = 100)
    author_id = models.IntegerField()
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to ="archives/originals/%Y/%m/%d/",
                              width_field="image_width",
                              height_field="image_height",
                              )
    image_height = models.IntegerField()
    image_width = models.IntegerField()
    thumbnail = models.ImageField(upload_to="archives/thumbs/%Y/%m/%d/",
                                  width_field="thumbnail_width",
                                  height_field="thumbnail_height",
                                  )
    thumbnail_height = models.IntegerField()
    thumbnail_width = models.IntegerField()
    caption = models.CharField(max_length = 250, blank =True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s owner:%s"%self.title, self.author_name
    def __unicode__(self):
        return self.title
    def save(self, force_update=False, force_insert=False, thumb_size=(180,300)):

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
