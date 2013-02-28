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
    著者モデル
    QRコードから抽出した情報を保持する
    """
    name = models.CharField(max_length = 100, default="", blank=True, null=True, db_index=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    roman = models.CharField(max_length=255, blank=True, null=True)
    student_id = models.CharField(max_length = 100, default="", blank=True, null=True, unique=True, db_index=True)
    ROLL_CHOICES = (
        ('s','Student'),
        ('t','Teacher'),
        ('g','Graduated'),
        ('e','Etcetera'),
        )
    roll = models.CharField(max_length=10, choices=ROLL_CHOICES, default="s", db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    admitted_at = models.DateTimeField(blank=True, null=True, db_index=True)
    graduated_at = models.DateTimeField(blank=True, null=True, db_index=True)
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    def get_photos(self, span=10, page=0, search_query=None, isvalid=True, order="-created_at", all=False, listvalue=None):
        """
        自分の著作を返す
        """
        result,count = Photo.get_items(author=self, span=span, page=page, search_query=search_query, isvalid=isvalid, order=order, all=all, listvalue=listvalue)
        return result,count
    def get_photo_num(self):
        """
        自分の著作の数を返す
        """
        num = Photo.objects.filter(authors__exact=self).count()
        return num
    def get_groups(self):
        """
        自分の所属グループリスト（年度別）を返す
        """
        result = GroupHandler.get_by_author(self)
        return result
    def my_groups(self):
        # 所属するグループのリストを作成
        groups = []
        try:
            g = self.get_groups()
            syear = self.admitted_at.year
            for i in range(syear, syear+6):
                gh = GroupHandler.get_item(self,i)
                gn = ""
                if gh and gh.group: gn = gh.group.name
                groups.append((i,gn))
        except:
            pass
        return groups
    @staticmethod
    def get_years():
        """
        すべての入学年度のリストを返す
        """
        return Author.objects.dates('admitted_at', 'year')
    @staticmethod
    def get_items(span=10, page=0, search_query=None, admitted_query=None, query_type=False,
                  group_year=None, group_name=None,
                  isvalid=True, order="-created_at", all=False, listvalue=None):
        result = None
        result_count = 0
        if page!=0:
            page = page*span - span
        endpage = page + span
        try:
        # if True:
            # 検索対象のすべてのエントリー数とSPANで区切ったエントリーを返す
            result = Author.objects.order_by(order).filter(isvalid=isvalid)
            if admitted_query:
                result = result.filter(admitted_at__year=admitted_query)
            if group_name:
                group = Group.get_by_name(group_name)
                if group_year:
                    result = result.filter(grouphandler__group=group,grouphandler__year__year=group_year) # 後方参照
                else:
                    result = result.filter(grouphandler__group=group) # 後方参照
            else:
                if group_year:
                    result = result.filter(grouphandler__year__year=group_year) # 後方参照
            if search_query:
                # 漢字とよみがなの場合を結合して検索．ANDかつ混合時には検索対象にならない
                qs1 = [Q(name__icontains=w) for w in search_query]
                qs2 = [Q(roman__icontains=w) for w in search_query]
                query1 = qs1.pop()
                query2 = qs2.pop()
                if query_type: # AND method
                    for q in qs1:
                        query1 &= q
                    for q in qs2:
                        query2 &= q
                else: # OR method
                    for q in qs1:
                        query1 |= q
                    for q in qs2:
                        query2 |= q
                query = query1 | query2
                result = result.filter(query)
            result_count = result.count()
            if not all:
                result = result[page:endpage]
            if listvalue:
                result = result.values_list(listvalue)
        except:
            pass
        return result, result_count
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
    else:
        name = os.path.splitext(os.path.basename(self.title))[0]+"."+filename.split(".")[-1]
    return os.path.join(user_path, name)
class Tag(models.Model):
    """
    タグモデル
    写真につけるタグの定義
    """
    name = models.CharField(max_length = 100, default="", blank=True, null=True)
    roman = models.CharField(max_length = 100, default="", blank=True, null=True)
    image_url = models.CharField(max_length = 255, default="", blank=True, null=True)
    comment = models.TextField(default="", db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    @staticmethod
    def get_all():
        return Tag.objects.filter(isvalid__exact=True)
    @staticmethod
    def get_items(page=0, span=10):
        result = Tag.objects.filter(isvalid__exact=True)
        if page!=0:
            page = page*span - span
            endpage = page + span
        return result[page:endpage],result.count()
    @staticmethod
    def tag_list():
        return Tag.objects.all()
    @staticmethod
    def get_by_id(id):
        result=None
        try:
            result = Tag.objects.get(id=int(id))
        except:
            result = None
        return result
    @staticmethod
    def get_by_name(name=""):
        result=None
        try:
            result = Tag.objects.filter(name=name).get()
        except:
            result = None
        return result
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/tag/%s" % self.id

class Photo(models.Model):
    """
    写真モデル
    アップロードした写真を保存、保存時にQRコードとExif情報を解析してメタ情報を記録しておく
    保存時には、自動で縮小したサムネイル用画像も作成する
    """
    authors = models.ManyToManyField(Author, blank=True, null=True, db_index=True)
    uuid = models.CharField(max_length = 32, default="", db_index=True)
    title = models.CharField(max_length = 100, default="", blank=True, null=True)
    original_title = models.CharField(max_length = 100, default="", blank=True, null=True)
    orientation = models.IntegerField(default=0, blank=True, null=True)
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
    caption = models.CharField(max_length = 250, default="", blank=True, null=True, db_index=True)
    comment = models.TextField(default="", db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    tag = models.ManyToManyField(Tag, blank=True, null=True, db_index=True)
    @staticmethod
    def get_years():
        """
        すべての登録書籍の年度リストを返す
        """
        return Photo.objects.dates('published_at', 'year')
    @staticmethod
    def get_items(author=None, span=10, page=0,
                  search_query=None, admitted_query=None, published_query=None, tag_queries=None, query_type=False,
                  order="-published_at", search_target=0, isvalid=True, all=False, listvalue=None):
        result = None
        result_count = 0
        if page!=0:
            page = page*span - span
        endpage = page + span
        try:
        # if True:
            # 検索対象のすべてのエントリー数とSPANで区切ったエントリーを返す
            result = Photo.objects.order_by(order).filter(isvalid=isvalid)
            if author:
                result = result.filter(authors__exact=author)
            if admitted_query:
                result = result.filter(authors__admitted_at__year=admitted_query)
            if published_query:
                result = result.filter(published_at__year=published_query)
            if search_query:
                qs1 = []
                qs2 = []
                query1 = []
                query2 = []
                if search_target is not 1:
                    qs1 = [Q(caption__icontains=w) for w in search_query]
                    query1 = qs1.pop()
                if search_target is not 0:
                    qs2 = [Q(comment__icontains=w) for w in search_query]
                    query2 = qs2.pop()
                if query_type: # AND method
                    for q in qs1:
                        query1 &= q
                    for q in qs2:
                        query2 &= q
                else: # OR method
                    for q in qs1:
                        query1 |= q
                    for q in qs2:
                        query2 |= q
                if query1 and not query2:
                    query = query1
                elif query2 and not query1:
                    query = query2
                else:
                    query = query1 | query2
                result = result.filter(query)
            if tag_queries:
                qs = []
                query = []
                qs = [Q(tag__exact=w) for w in tag_queries]
                query = qs.pop()
                for q in qs:
                    query |= q
                result = result.filter(query)
            result_count = result.count()
            if not all:
                result = result[page:endpage]
            if listvalue:
                result = result.values_list(listvalue)
        except:
            pass
        return result, result_count

    @staticmethod
    def get_by_pub_and_name(pub, name):
        result = None
        try:
            # 写真の撮影日時が同一の場合 ファイル名が同じ場合
            result = Photo.objects.filter(published_at__exact=pub).filter(original_title__exact=name)[0]
        except:
            result = None
        return result
    @staticmethod
    def get_by_uuid(photo_uuid):
        result = None
        try:
            result = Photo.objects.filter(uuid__exact=photo_uuid)[0]
        except:
            result = None
        return result
    def get_authors(self):
        return self.authors.all()
    def get_original_img_url(self):
        return "/media/"+str(self.image.name)
    def get_thumbnail_img_url(self):
        return "/media/"+str(self.thumbnail.name)
    def __str__(self):
        # aname = ""
        # for i in self.author:
        #     aname += i.name +", "
        # return "%s owner: %s" % (self.title, aname)
        return self.title
    def __unicode__(self):
        return self.title
    def save(self, force_update=False, force_insert=False, thumb_size=(800,1000), isFirst = False):
        if isFirst:
            if not self.uuid:
                # 万が一uuidの被りがあった場合は再精製。最大10回繰り返す。
                cuuid = ""
                for i in range(0,10):
                    cuuid = uuid.uuid4().hex
                    if not Photo.get_by_uuid(cuuid):
                        break
                self.uuid = cuuid
            super(Photo, self).save(force_update, force_insert)
        else:
            image = Image.open(self.image)
            # if image.mode not in ('L', 'RGB'): # ウィンドウシャドウが消えるので変換中止
            #     image = image.convert('RGB')
            # save the original size
            self.image_width, self.image_height = image.size
            image.thumbnail(thumb_size, Image.ANTIALIAS)
            try: # EXIF にしたがってサムネイル画像を回転
                if self.orientation and self.orientation != 1:
                    r = {3:180,6:-90,8:90}
                    image = image.rotate(r[self.orientation])
            except:
                pass
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
class Group(models.Model):
    """
    グループモデル
    著者が所属するグループの定義
    年度ごとに所属するグループを変更可能。学年と組の関係などを表すときに使います。
    """
    name = models.CharField(max_length = 100, default="", blank=True, null=True)
    roman = models.CharField(max_length = 100, default="", blank=True, null=True)
    image_url = models.CharField(max_length = 255, default="", blank=True, null=True)
    comment = models.TextField(default="", db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    @staticmethod
    def get_all():
        return Group.objects.filter(isvalid__exact=True)
    @staticmethod
    def get_items(page=0, span=10):
        result = Group.objects.filter(isvalid__exact=True)
        if page!=0:
            page = page*span - span
            endpage = page + span
        return result[page:endpage],result.count()
    @staticmethod
    def group_list():
        return Group.objects.all()

    @staticmethod
    def get_by_id(id):
        result=None
        try:
            result = Group.objects.get(id=int(id))
        except:
            result = None
        return result
    @staticmethod
    def get_by_name(name=""):
        result=None
        try:
            result = Group.objects.filter(name=name).get()
        except:
            result = None
        return result
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/group/%s" % self.id

class GroupHandler(models.Model):
    author = models.ForeignKey(Author, db_index=True)
    group = models.ForeignKey(Group, db_index=True, blank=True, null=True, )
    year = models.DateTimeField(blank=True, null=True, db_index=True)
    isvalid = models.BooleanField(default=True, db_index=True)
    updated_at = models.DateTimeField(auto_now = True, db_index=True)
    created_at = models.DateTimeField(auto_now_add = True, db_index=True)
    @staticmethod
    def get_by_author(author):
        result = GroupHandler.objects.order_by("year").filter(author__exact=author)
        return result
    @staticmethod
    def get_item(author, year):
        result = None
        try:
            result = GroupHandler.objects.filter(isvalid__exact=True).filter(author__exact=author).filter(year__year=year)[0]
        except:
            pass
        return result
    @staticmethod
    def get_authors(group=None):
        result = GroupHandler.objects.order_by("year")
        if group:
            result = result.filter(group=group)
        return result
    @staticmethod
    def get_years():
        """
        すべての年度のリストを返す
        """
        return GroupHandler.objects.dates('year', 'year')
    def __unicode__(self):
        return self.author.name

class Meta:
    ordering = ['-created_at']
