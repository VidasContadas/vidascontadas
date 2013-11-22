from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('comercios.views',
    url(r'^$', "home",name="home"),
    url(r'^noticias/$', "news",name="noticias"),
    url(r'^noticias/(?P<slug>[\w\-_]+)/$', "news",name="noticia"),
)
