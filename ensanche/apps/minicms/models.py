# coding=utf-8

from django.db import models

from django.utils import translation
from django.utils.translation import ugettext as _
from django.conf import settings
from django.http import Http404
from logicaldelete.models import Model as LogicalDeletableModel
from redactor.fields import RedactorField


class Page(LogicalDeletableModel):
    titulo = models.CharField(max_length=255)
    contenido = RedactorField()
    slug = models.SlugField("URL",max_length=255,blank=True,db_index=True)
    orden = models.PositiveIntegerField(default=0,blank=False,help_text=_(u"0 for the index"),db_index=True)
    language = models.CharField("Idioma",max_length=255,blank=False,choices=settings.LANGUAGES,default=settings.LANGUAGE_CODE,db_index=True)
    meta_keywords = models.TextField(help_text=_(u"csv meta keywords for SEO"))
    meta_description = models.TextField(help_text=_(u"meta description for SEO"))
    updated = models.DateField(u"Última modificación",auto_now=True)
    
    def __unicode__(self):
        return self.titulo
    
    def get_absolute_url(self):
        if not self.domain:
            return self.this_url()
        
        return u"http://%s/%s/" % (self.domain,self.slug)
    
    #@models.permalink
    def this_url(self):
        if self.slug:
            return "/%s/" % self.slug
        else:
            return "/"
    
    @classmethod
    def get_by_slug(self,slug):
        try:
            return self.objects.get(slug=slug,language=translation.get_language())
        except self.DoesNotExist:
            pass
        
        try:
            return self.objects.get(slug=slug,language=settings.LANGUAGE_CODE)
        except self.DoesNotExist:
            raise Http404
    
    @classmethod
    def get_index(self):
        try:
            return self.objects.get(sort=0,language=translation.get_language())
        except self.DoesNotExist:
            return self.objects.get(sort=0,language=settings.LANGUAGE_CODE)
    
    @classmethod
    def get_others(self):
        return self.objects.exclude(sort=0).filter(language=translation.get_language())
    
    @classmethod
    def get_all(self):
        return self.objects.all().filter(language=translation.get_language())
    
    def is_index(self):
        return self.sort == 0

    def save(self,*args,**kwargs):

        if not self.slug:
            self.slug = slugify(self.nombre)

        super(Page,self).save(*args,**kwargs)
    
    class Meta:
        ordering = ('orden',)
        verbose_name = 'pagina'
