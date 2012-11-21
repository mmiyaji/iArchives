from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.conf import settings
import os
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'archives.general.home', name='home'),
                       url(r'^login/$', 'archives.general.signin'),
                       url(r'^logout/$', 'archives.general.signout'),
                       url(r'^upload/$', 'archives.upload.home', name='upload'),
                       url(r'^archive/$', 'archives.archive.home'),
                       url(r'^archive/author/$', 'archives.archive.authors'),
                       url(r'^archive/author/(?P<author_id>\w+)/$', 'archives.archive.author'),
                       url(r'^archive/year/$', 'archives.archive.years'),
                       url(r'^archive/year/(?P<year>\d+)/$', 'archives.archive.year'),
                       url(r'^photo/$', 'archives.photo.home'),
                       url(r'^photo/(?P<photo_uuid>\w{32})/$', 'archives.photo.detail'),
                       url(r'^photo/(?P<photo_uuid>\w{32})/delete/$', 'archives.photo.delete'),
                       url(r'^photo/(?P<photo_uuid>\w{32})/update/$', 'archives.photo.update'),
                       url(r'^author/$', 'archives.author.home'),
                       url(r'^author/meibo/add/$', 'archives.author.meiboadd'),
                       url(r'^author/(?P<author_id>\w+)/$', 'archives.author.detail'),
                       url(r'^author/(?P<author_id>\w+)/update/$', 'archives.author.update'),
                       url(r'^group/$', 'archives.group.home'),
                       url(r'^group/(?P<group_id>\d+)/$', 'archives.group.detail'),
                       url(r'^group/(?P<group_id>\d+)/update/$', 'archives.group.update'),
                       url(r'^group/(?P<group_id>\d+)/delete/$', 'archives.group.delete'),
                       url(r'^group/meibo/add/$', 'archives.group.meiboadd'),
                       url(r'^tag/$', 'archives.tag.home'),
                       url(r'^tag/(?P<tag_id>\d+)/$', 'archives.tag.detail'),
                       url(r'^tag/(?P<tag_id>\d+)/update/$', 'archives.tag.update'),
                       url(r'^tag/(?P<tag_id>\d+)/delete/$', 'archives.tag.delete'),
                       url(r'^tag/meibo/add/$', 'archives.tag.meiboadd'),
                       url(r'^search/$', 'archives.search.home'),
                       url(r'^search/author/$', 'archives.search.author'),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^adminsite/', include(admin.site.urls)),
                       )
