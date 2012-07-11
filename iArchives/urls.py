from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'archives.general.home', name='home'),
                       )

# urlpatterns = patterns('',
#                        # url(r'^$', 'iArchives.views.home', name='home'),
#                        # include app urls.py file
#                        url(r'^(/)?', include('iArchives.iarchives.urls')),
                       # )
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$','django.views.static.serve',
                             {'document_root':os.path.dirname(__file__)+'/static'}),
                            )
