from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       # url(r'^$', 'iArchives.views.home', name='home'),
                       url(r'^(/)?', include('iArchives.iarchives.urls')),
                       )
