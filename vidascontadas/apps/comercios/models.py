# coding=utf-8

from django.db import models
from redactor.fields import RedactorField
from filer.fields.image import FilerImageField, FilerFileField
from logicaldelete.models import Model as LogicalDeletableModel
from vidascontadas.settings import MEDIA_ROOT
from categories.models import CategoryBase
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User
#from django.template.defaultfilters import slugify
from uuslug import uuslug

#from django.db.models import get_model
#Asociado = get_model('asociacion', 'Asociado')

class CategoriaComercio(CategoryBase):
    """
    A simple example
    """    

    @classmethod    
    def get_list(cls,exclude=None):
        return cls.objects.filter(parent=None, active=True)

    class Meta:
        verbose_name_plural = 'Categorías comercios'

class Comercio(LogicalDeletableModel):

    nombre = models.CharField(max_length=255,unique=True)
    slug = models.SlugField("URL",blank=True,unique=True,help_text=u"Si lo deja en blanco se generará a partir del nombre")
    #logotipo = models.ImageField(verbose_name="Logotipo", null=True, blank=True, upload_to=MEDIA_ROOT, max_length=300)
    imagen = models.ImageField(verbose_name="Imagen principal", null=True, blank=True, upload_to='%Y/%m/%d', max_length=300)

    categorias = models.ManyToManyField(CategoriaComercio,blank=True,related_name="comercios")
    presentacion = RedactorField()
    #imagen = FilerImageField("Imagen principal",help_text="Usada para representar al comercio en miniaturas, etc")
    #imagen = FilerImageField()
    
    facebook_url = models.URLField(u"Dirección de Facebook",blank=True,null=True)
    twitter_url = models.URLField(u"Dirección de Twitter",blank=True,null=True)
    googleplus_url = models.URLField(u"Dirección de Google+",blank=True,null=True)
    tuenti_url = models.URLField(u"Dirección de Tuenti",blank=True,null=True)
    instagram_url = models.URLField(u"Dirección de Instagram",blank=True,null=True)

    administradores = models.ManyToManyField(User,blank=True,related_name="mis_tiendas")
    visible = models.BooleanField(default=False)

    asociado = models.ForeignKey('asociacion.Asociado',related_name="microsite",blank=True,null=True)

    @classmethod
    def get_list(cls,exclude=None):
        return cls.objects.all().order_by('nombre')

    @property
    def logo(self):

        if self.fotos.count() > 0:
            return self.fotos.all()[0].imagen.url
        else:
            return '/static/img/ensanche-logo-verde-viejo.png'

    def save(self,*args,**kwargs):

        if not self.slug:
            self.slug = uuslug(self.nombre, instance=self)

        super(Comercio,self).save(*args,**kwargs)
        

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = "comercio"
        ordering = ('nombre',)

class Local(models.Model):
    comercio = models.ForeignKey(Comercio,related_name="locales",)
    nombre = models.CharField(max_length=100)
    direccion = RedactorField()
    telefono = models.CharField(max_length=10, null=True, blank=True)
    localizacion = GeopositionField(default='42.813127326939224,-1.6393232345581055')

    def __unicode__(self):
        return u"%s | %s" % (self.comercio.nombre,self.nombre)

ICONOS = (
    ('icon-file', u'Página'),
    ('icon-camera', u'Cámara'),
    ('icon-rss', 'RSS'),
    ('icon-list-ol', 'Lista'),
    ('icon-beaker', 'Laboratorio'),
    ('icon-calendar', 'Calendario'),
)

class Pagina(models.Model):
    comercio = models.ForeignKey(Comercio,related_name="paginas",)
    titulo = models.CharField(max_length=100)
    texto = RedactorField()
    visible = models.BooleanField(default=False)
    icono = models.CharField(max_length=50,blank=True,null=True, choices=ICONOS, default='icon-file')

    def __unicode__(self):
        return u"%s > %s" % (self.comercio.nombre,self.titulo)

class Imagen(models.Model):
    comercio = models.ForeignKey(Comercio,related_name="fotos",)
    imagen = models.ImageField(verbose_name=u"Imágen", null=True, blank=True, upload_to='slides', max_length=300)
    order = models.PositiveIntegerField('Orden en la galería',default=1)
    nombre = models.CharField(max_length=255,blank=True,null=True)
    presentacion = RedactorField(null=True, blank=True)
    visible = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s - %s" % (self.comercio.nombre, self.nombre)
    
    class Meta:
        verbose_name = u"Imágen de la galería"
        verbose_name_plural = u"Imágenes de la galería"
        ordering = ('order',)

class Propuesta(models.Model):
    comercio = models.ForeignKey(Comercio,related_name="propuestas",)
    imagen = models.ImageField(verbose_name="Imagen", null=True, blank=True, upload_to='propuestas/%Y/%m/%d', max_length=300)
    titulo = models.CharField(max_length=255,blank=True,null=True)
    presentacion = RedactorField(null=True, blank=True, verbose_name="Detalles de la propuesta")
    visible = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titulo

    @classmethod
    def get_list(cls,exclude=None):
        return cls.objects.filter(visible=True).exclude(imagen__exact='').order_by('?')

    @classmethod
    def get_last(cls,exclude=None):
        return cls.objects.filter(visible=True).exclude(imagen__exact='').order_by('?')[0:10]

    class Meta:
        verbose_name = "Propuesta comercial"
        verbose_name_plural = "Nuestras propuestas"
        ordering = ('titulo',)