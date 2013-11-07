# coding=utf-8

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


from sitemaps import *

sitemaps = {'page':PageSitemap(),}

urlpatterns = patterns('',

    
    (r'^urllist\.txt$', 'minicms.views.urllist'),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^$', 'minicms.views.page'),
    ( settings.MINICMS_CONTACT_URL, 'minicms.views.contact', ),
    (r'(?P<slug>.*)/', 'minicms.views.page'),
)

#handler500 = 'TheChurchofHorrors.site.views.server_error'

