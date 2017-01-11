# coding=utf-8

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^redactor/', include('redactor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include("asociacion.urls")),
    url(r'^mi-cuenta/logout/$', logout, {'next_page': '/'}),    
    url(r'^mi-cuenta/', include('registration.backends.default.urls')),
    url(r'^ajax-upload/', include('cicu.urls')),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.sitemaps.views import sitemap
from vidascontadas.sitemap import ComercioSitemap

# Define sitemaps
sitemaps = {
    'comercios': ComercioSitemap,
}
urlpatterns += url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),


