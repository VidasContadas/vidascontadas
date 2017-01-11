# coding=utf-8

from django.db import models
from redactor.fields import RedactorField
from filer.fields.image import FilerImageField, FilerFileField
from logicaldelete.models import Model as LogicalDeletableModel
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField

from categories.models import CategoryBase
from comercios.models import Comercio
from datetime import datetime

from django.core.urlresolvers import reverse

class CategoriaAsociado(CategoryBase):
    """
    A simple example
    """    

    @classmethod    
    def get_list(cls,exclude=None):
        return cls.objects.filter(parent=None, active=True).extra(order_by = ['name'])

    class Meta:
        verbose_name_plural = 'Categorías comercios'

class CategoriaConvenio(CategoryBase):
    """
    A simple example
    """    

    @classmethod    
    def get_list(cls,exclude=None):
        return cls.objects.filter(parent=None, active=True)

    class Meta:
        verbose_name_plural = 'Categorías convenios'

class Convenio(LogicalDeletableModel):
    name = models.CharField(max_length=255)
    descripcion = RedactorField()
    tipo = models.CharField(max_length=255)
    logo = FilerImageField(null=True, blank=True,related_name="convenio_logo")
    folleto = FilerFileField(null=True, blank=True,related_name="convenio_folleto")    
    categoria = models.ManyToManyField(CategoriaConvenio,blank=False,related_name="convenios")

    def __unicode__(self):
        return self.name

    @classmethod
    def get_list(cls, categoria=None, exclude=None):
        if categoria:
            mycat = CategoriaConvenio.objects.get(slug = categoria)
            return mycat.convenios.all().order_by('name')
        else:
            return cls.objects.all().order_by('name')

class Asociado(LogicalDeletableModel):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    categorias = models.ManyToManyField(CategoriaAsociado, blank=False, related_name="asociados")
    location = GeopositionField()

    def __unicode__(self):
        return self.nombre + ' ' + self.direccion

    @classmethod
    def get_list(cls):
        return cls.objects.all().order_by('nombre')

class Evento(LogicalDeletableModel):
    #comercio = models.ForeignKey(Comercio,related_name="noticias",)
    titulo = models.CharField(max_length=255)
    slug = models.SlugField(blank=True,null=True)    
    fecha_inicio = models.DateTimeField(blank=True,null=True)
    fecha_fin = models.DateTimeField(blank=True,null=True)
    lugar = models.CharField(max_length=255)
    mapa = GeopositionField()
    imagen = FilerImageField()
    #imagen = models.ImageField(upload_to='eventos')
    texto = RedactorField()
    boton_txt = models.CharField(max_length=20,blank=True,null=True)
    boton_url = models.URLField(u"URL",blank=True,null=True)    
    visible = models.BooleanField(default=False)
    participantes = models.ManyToManyField(Comercio, blank=False, related_name="eventos")

    @models.permalink
    def get_absolute_url(self):
        #return ('noticia', (), {'year':self.fecha.year,'month':self.fecha.month, 'slug': self.slug,})
        #return ('evento', (), {'year':self.fecha_inicio.year,'month':self.fecha_inicio.month,'slug': self.slug,})
        #return reverse('evento', kwargs={'year':self.fecha_inicio.year,'month':self.fecha_inicio.month,'slug': self.slug,})
        return reverse('evento', kwargs={'year':self.fecha_inicio.year,'month':self.fecha_inicio.month,'slug': self.slug,})

    @classmethod
    def get_list(cls):
        #qs = cls.objects.filter(visible=True, fecha_fin__gte=datetime.now())
        qs = cls.objects.filter(visible=True).exclude(fecha_inicio__isnull=True).order_by('fecha_inicio')
        return qs

    @classmethod
    def get_anteriores(cls):
        #qs = cls.objects.filter(visible=True, fecha_fin__lte=datetime.now())
        qs = cls.objects.filter(visible=True).exclude(fecha_inicio__isnull=True)
        return qs

    @classmethod
    def get_fijos(cls):
        #qs = cls.objects.filter(visible=True, fecha_fin__lte=datetime.now())
        qs = cls.objects.filter(visible=True,fecha_inicio__isnull=True)[:3]
        #qs = cls.objects.filter(visible=True)[:3]
        return qs

    @property
    def pretty_date(self):
        from dateutil import relativedelta
        import locale
        locale.setlocale(locale.LC_TIME, "es_ES")
        d = relativedelta.relativedelta(self.fecha_fin, self.fecha_inicio)

        if (d.months > 0):
            fmt = '%d de %B de %Y'
            fecha = 'Del ' + self.fecha_inicio.strftime('%d de %B') + ' al ' + self.fecha_fin.strftime('%d de %B')
        elif (d.days > 1):
            fecha = 'Del ' + self.fecha_inicio.strftime('%d') + ' al ' + self.fecha_fin.strftime('%d') + ' de ' + self.fecha_inicio.strftime('%B') 
        else:
            fmt = '%d de %B de %Y a las %H:%M'
            fecha = self.fecha_inicio.strftime(fmt)

        return fecha

    def __unicode__(self):
        return self.titulo

class Noticia(LogicalDeletableModel):
    #comercio = models.ForeignKey(Comercio,related_name="noticias",)
    autor = models.ForeignKey(User)
    fecha = models.DateField()
    slug = models.SlugField(max_length=255)
    titulo = models.CharField(max_length=255)
    imagen = FilerImageField()
    texto = RedactorField()
    resumen = models.TextField(help_text=u"Pequeño resumen de la noticia para mostrar en los listados")
    visible = models.BooleanField(default=False)

    @classmethod
    def get_list(cls,exclude=None):
        qs = cls.objects.filter(visible=True)

        if exclude:
            qs = qs.exclude(id=exclude.id)

        return qs

    def __unicode__(self):
        return self.titulo

    #def save(self,*args,**kwargs):
    #    self.slug = slugify(self.titulo)
    #    self.autor = request.user
    #    super(Noticia,self).save(*args,**kwargs)

    @models.permalink
    def get_absolute_url(self):
        #return ('noticia', (), {'year':self.fecha.year,'month':self.fecha.month, 'slug': self.slug,})
        return ('noticia', (), {'slug': self.slug,})

    class Meta:
        verbose_name = "noticia"
        ordering = ('-fecha','titulo',)

class Foto(models.Model):
    noticia = models.ForeignKey('Noticia')
    imagen = models.ImageField(upload_to='slideshow', max_length=500)
    titulo = models.CharField(max_length=50, blank=True,null=True)
    descripcion = models.TextField(blank=True)

    def __unicode__(self):
        return self.titulo

class Colaborador(LogicalDeletableModel):
    name = models.CharField(max_length=255)
    descripcion = RedactorField()
    tipo = models.CharField(max_length=255)
    logo = FilerImageField(null=True, blank=True,related_name="logo_colaborador")
    folleto = FilerFileField(null=True, blank=True,related_name="folleto_colaborador")        

PAGINAS = (
    ('agenda', 'Agenda'),
    ('asociados', 'Guía establecimientos'),
    ('convenios', 'Asóciate'),
)

class Banner(models.Model):
    imagen = models.ImageField(upload_to='banners', max_length=500, help_text=u'Tamaño de la imagen: 1920x700px')
    pagina = models.CharField(max_length=10, choices=PAGINAS, blank=True, null=True)

    def __unicode__(self):
        return self.pagina

from adminsortable.models import Sortable

CAPTION_POSITIONS = (
    ('top-left', 'Arriba a la izquierda'),
    ('center-left', 'Izquierda'),
    ('bottom-left', 'Abajo a la izquierda'),
    ('top-right', 'Arriba a la derecha'),
    ('center-right', 'Derecha'),
    ('bottom-right', 'Abajo a la derecha'),
)

class Slides(Sortable):
    class Meta(Sortable.Meta):
        pass

    #order = models.PositiveIntegerField('Orden en la galería',default=1)
    titulo = models.CharField(max_length=50,blank=True,null=True)
    subtitulo = models.CharField(max_length=100,blank=True,null=True)
    boton_txt = models.CharField(max_length=20,blank=True,null=True)
    boton_url = models.URLField(u"URL",blank=True,null=True)
    presentacion = RedactorField(null=True, blank=True)    
    imagen = models.ImageField(verbose_name="Imagen", help_text=u"Tamaño 1920x900px", null=True, blank=True, upload_to='%Y/%m/%d', max_length=300)
    visible = models.BooleanField(default=False) 
    position = models.CharField(max_length=50,blank=True,null=True, choices=CAPTION_POSITIONS, default='center-left')

    def __unicode__(self):
        return self.titulo
    
    @property
    def caption_class(self):
        if self.position.endswith("right"):
            return u"span6 offset5 text-right"
        else:
            return u"span6"

    class Meta:
        verbose_name = u"Imagen de la página principal"
        verbose_name_plural = u"Imágenes de la página principal"
        ordering = ('order',)

from watson import search as watson

watson.register(Asociado,fields=("nombre", "direccion", "categorias"))
#watson.register(CategoriaAsociado)