from django.contrib import sitemaps
import datetime

class Sitemap(sitemaps.Sitemap):
    def __init__(self, names):
        self.names = names

    def items(self):
        return self.names

    def changefreq(self, obj):
        return 'weekly'

    def lastmod(self, obj):
        return datetime.datetime.now()

    def location(self, obj):
        return reverse(obj)

from comercios.models import Comercio

class ComercioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Comercio.objects.all()

    def lastmod(self, obj):
        return obj.date
