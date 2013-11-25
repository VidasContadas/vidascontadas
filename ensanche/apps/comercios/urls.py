from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('comercios.views',
    url(r'^$', "home",name="home"),
    url(r'^noticias/$', "news",name="noticias"),
    url(r'^comercios/$', "comercios",name="comercios"),
    url(r'^noticias/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w\-_]+)/$', "news",name="noticia"),
)
