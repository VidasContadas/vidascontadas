from django.contrib.sitemaps import Sitemap
from minicms.models import Page

class PageSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Page.objects.all()

    def lastmod(self, obj):
        return obj.updated
