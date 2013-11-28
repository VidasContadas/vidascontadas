# coding=utf-8

from django.db import models
from redactor.fields import RedactorField
from filer.fields.image import FilerImageField
from logicaldelete.models import Model as LogicalDeletableModel
from django.template.defaultfilters import slugify

class Marca(models.Model):
	nombre = models.CharField(max_length=255,unique=True)
	logo = FilerImageField()

	def __unicode__(self):
		return self.nombre

class Categoria(models.Model):
	nombre = models.CharField(max_length=255,unique=True)
	slug = models.SlugField(unique=True)

	@classmethod
	def get_list(cls):
		return cls.objects.exclude(comercios=None)

	def __unicode__(self):
		return self.nombre

	def save(self,*args,**kwargs):

		self.slug = slugify(self.nombre)

		super(Categoria,self).save(*args,**kwargs)

	class Meta:
		ordering = ('nombre',)



class Comercio(LogicalDeletableModel):
	nombre = models.CharField(max_length=255,unique=True)
	slug = models.SlugField("URL",blank=True,unique=True,help_text=u"Si lo deja en blanco se generará a partir del nombre")
	categorias = models.ManyToManyField(Categoria,blank=False,related_name="comercios")
	presentacion = RedactorField()
	#imagen = FilerImageField("Imagen principal",help_text="Usada para representar al comercio en miniaturas, etc")
	imagen = FilerImageField()

	marcas = models.ManyToManyField(Marca,blank=True,null=True)

	facebook_url = models.URLField(u"Dirección de Facebook",blank=True,null=True)
	twitter_url = models.URLField(u"Dirección de Twitter",blank=True,null=True)
	googleplus_url = models.URLField(u"Dirección de Google+",blank=True,null=True)
	tuenti_url = models.URLField(u"Dirección de Tuenti",blank=True,null=True)
	instagram_url = models.URLField(u"Dirección de Instagram",blank=True,null=True)

	@classmethod
	def get_list(cls,exclude=None):
		return cls.objects.all()

	def save(self,*args,**kwargs):

		if not self.slug:
			self.slug = slugify(self.nombre)

		super(Comercio,self).save(*args,**kwargs)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "comercio"
		ordering = ('nombre',)


class Imagen(models.Model):
    comercio = models.ForeignKey(Comercio,related_name="images",)
    imagen = FilerImageField()
    order = models.PositiveIntegerField('Orden en la galería',default=1)

    def __unicode__(self):
		return "%d :: %s" (self.order,self.comercio,)
    
    class Meta:
        verbose_name = "imagen de la galería"
        verbose_name_plural = "imagenes de la galería"
        ordering = ('order',)

class Oferta(LogicalDeletableModel):
	comercio = models.ForeignKey(Comercio,related_name="ofertas",)
	titulo = models.CharField(max_length=255)
	imagen = FilerImageField()
	texto = models.TextField()

	def __unicode__(self):
		return self.titulo

	class Meta:
		verbose_name = "oferta"
		ordering = ('titulo',)

class Noticia(LogicalDeletableModel):
	#comercio = models.ForeignKey(Comercio,related_name="noticias",)
	fecha = models.DateField()
	slug = models.SlugField()
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

	@models.permalink
	def get_absolute_url(self):
		return ('noticia', (), {'year':self.fecha.year,'month':self.fecha.month, 'slug': self.slug,})

	def save(self,*args,**kwargs):

		self.slug = slugify(self.titulo)

		super(Noticia,self).save(*args,**kwargs)


	class Meta:
		verbose_name = "noticia"
		ordering = ('-fecha','titulo',)


class Evento(LogicalDeletableModel):
	titulo = models.CharField(max_length=255)
	slug = models.SlugField()
	imagen = FilerImageField()
	descripcion = models.TextField()
	direccion = models.CharField(max_length=1024)
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField(blank=True,null=True)
	hora_inicio = models.TimeField(blank=True,null=True)
	hora_fin = models.TimeField(blank=True,null=True)
	visible = models.BooleanField(default=True)

	@classmethod
	def get_list(cls,exclude=None):
		qs = cls.objects.filter(visible=True)

		if exclude:
			qs = qs.exclude(id=exclude.id)

		return qs

	@models.permalink
	def get_absolute_url(self):
		return ('evento', (), {'year':self.fecha_inicio.year,'slug': self.slug,})

	def __unicode__(self):
		return self.titulo

	def save(self,*args,**kwargs):

		self.slug = slugify(self.titulo)

		super(Evento,self).save(*args,**kwargs)


	class Meta:
		verbose_name = "evento"
		ordering = ('-fecha_inicio','-hora_inicio','titulo',)
