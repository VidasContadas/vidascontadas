from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('comercios.views',
    url(r'^$', "home",name="home"),
    url(r'^noticias/$', "news",name="noticias"),
    url(r'^eventos/$', "events",name="eventos"),
    url(r'^comercios/$', "comercios",name="comercios"),
    url(r'^noticias/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w\-_]+)/$', "news",name="noticia"),
    url(r'^eventos/(?P<year>\d+)/(?P<slug>[\w\-_]+)/$', "events",name="evento"),
)
