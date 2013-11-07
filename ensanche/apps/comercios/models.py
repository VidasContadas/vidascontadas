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

	verbose_name = "marca"

class Comercio(LogicalDeletableModel):
	nombre = models.CharField(max_length=255,unique=True)
	slug = models.SlugField("URL",blank=True,unique=True,help_text=u"Si lo deja en blanco se generará a partir del nombre")
	presentacion = RedactorField()
	#imagen = FilerImageField("Imagen principal",help_text="Usada para representar al comercio en miniaturas, etc")
	imagen = FilerImageField()

	marcas = models.ManyToManyField(Marca,blank=True,null=True)

	facebook_url = models.URLField(u"Dirección de Facebook",blank=True,null=True)
	twitter_url = models.URLField(u"Dirección de Twitter",blank=True,null=True)
	googleplus_url = models.URLField(u"Dirección de Google+",blank=True,null=True)
	tuenti_url = models.URLField(u"Dirección de Tuenti",blank=True,null=True)
	instagram_url = models.URLField(u"Dirección de Instagram",blank=True,null=True)

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
	comercio = models.ForeignKey(Comercio,related_name="noticias",)
	fecha = models.DateField()
	titulo = models.CharField(max_length=255)
	imagen = FilerImageField()
	texto = RedactorField()

	def __unicode__(self):
		return self.titulo

	class Meta:
		verbose_name = "noticia"
		ordering = ('titulo',)
