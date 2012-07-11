from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       # url(r'^$', 'iArchives.views.home', name='home'),
                       # include app urls.py file
                       url(r'^(/)?', include('iArchives.iarchives.urls')),
                       )
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$','django.views.static.serve',
                             {'document_root':os.path.dirname(__file__)+'/static'}),
                            )
