from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.conf import settings
import os


urlpatterns = patterns('',
                       # (r'^admin/(.*)', admin.site.root),
                       # url(r'^$', 'archives.general.home', name='home'),
                       url(r'^(/)?', include('archives.urls')),
                       url(r'^404/$', 'iArchives.views.status404', name='404'),
                       )

# urlpatterns = patterns('',
#                        # url(r'^$', 'iArchives.views.home', name='home'),
#                        # include app urls.py file
#                        url(r'^(/)?', include('iArchives.iarchives.urls')),
# )
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT}),
                            (r'^media/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
                            (r'^admin/(?P<path>.*)$','django.views.static.serve',
                             {'document_root': settings.ADMIN_MEDIA_PREFIX}),

                            )
