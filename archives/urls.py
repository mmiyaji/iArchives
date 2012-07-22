from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.conf import settings
import os
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'archives.general.home', name='home'),
                       url(r'^upload/$', 'archives.upload.home', name='upload'),
                       url(r'^photo/$', 'archives.photo.home'),
                       url(r'^photo/(?P<photo_uuid>\d+)/$', 'archives.photo.detail'),
                       url(r'^photo/(?P<photo_uuid>\d+)/delete/$', 'archives.photo.delete'),
                       url(r'^photo/(?P<photo_uuid>\d+)/update/$', 'archives.photo.update'),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^adminsite/', include(admin.site.urls)),
                       )
