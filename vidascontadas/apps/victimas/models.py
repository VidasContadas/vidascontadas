# coding=utf-8

from django.db import models

from redactor.fields import RedactorField
from filer.fields.image import FilerImageField, FilerFileField
from logicaldelete.models import Model as LogicalDeletableModel
from vidascontadas.settings import MEDIA_ROOT
from categories.models import CategoryBase
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User
from uuslug import uuslug
from filer.models.foldermodels import Folder

# Create your models here.

class Licencia(models.Model):

    nombre = models.CharField(max_length=255)
    resumen = models.TextField(help_text=u"Pequeño resumen de la licencia para mostrar en los listados")
    uso = models.BooleanField(default=True)
    difusion = models.BooleanField(default=True)
    explotacion = models.BooleanField(default=True)
    distribucion = models.BooleanField(default=True)

TIPOLOGIA_DOCUMENTO = (
    ('publico', 'Documento público'),
    ('privado', 'Documento privado'),
)

TIPO_DOCUMENTO = (
    ('carta', 'Carta'),
    ('registro', 'Registro'),
    ('sentencia', 'Sentencia'), 
    ('foto', 'Fotografía'),   
)

FORMATO_DOCUMENTO = (
    ('texto', 'Texto'),
    ('imagen', 'Imagen'),
    ('video', 'Video'),  
)

class Document(LogicalDeletableModel):
    nombre = models.CharField(max_length=255,unique=True)
    descripcion = RedactorField()
    archivo = FilerFileField(null=True, blank=True)

    tipologia = models.CharField(max_length=255, choices=TIPOLOGIA_DOCUMENTO)
    tipo = models.CharField(max_length=255, choices=TIPO_DOCUMENTO)
    formato = models.CharField(max_length=255, choices=FORMATO_DOCUMENTO)

    licencia = models.ForeignKey(Licencia, related_name="documents",)

class Dataset(LogicalDeletableModel):

    nombre = models.CharField(max_length=255,unique=True)
    slug = models.SlugField("URL",blank=True,unique=True,help_text=u"Si lo deja en blanco se generará a partir del nombre")
    imagen = models.ImageField(verbose_name="Imagen principal", null=True, blank=True, upload_to='%Y/%m/%d', max_length=300)
    descripcion = RedactorField()
    carpeta = models.ForeignKey(Folder, related_name="carpeta",)
    original_url = models.URLField(u"Dirección de los datos originales",blank=True,null=True)
    csv_file = FilerFileField(null=True, blank=True)

    openrefine = models.CharField(max_length=255,unique=True)
    github = models.URLField(u"Github scrapy project",blank=True,null=True)

    administradores = models.ManyToManyField(User,blank=True,related_name="mis_datasets")
    procesado = models.BooleanField(default=False)
    num_records = models.PositiveIntegerField('Número de registros',default=0)
    porcentaje = models.PositiveIntegerField('Porcentaje procesado',default=10)

    licencia = models.ForeignKey(Licencia, related_name="datasets",)

    @classmethod
    def get_list(cls,exclude=None):
        return cls.objects.all().order_by('nombre')

    @property
    def procesado(self):
        if self.porcentaje == 100:
            return True
        else:
            return False

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
        verbose_name = "dataset"
        ordering = ('nombre',)

class Project(LogicalDeletableModel):

    nombre = models.CharField(max_length=255,unique=True)
    slug = models.SlugField("URL",blank=True,unique=True,help_text=u"Si lo deja en blanco se generará a partir del nombre")
    imagen = models.ImageField(verbose_name="Imagen principal", null=True, blank=True, upload_to='%Y/%m/%d', max_length=300)
    descripcion = RedactorField()
    administradores = models.ManyToManyField(User,blank=True,related_name="mis_proyectos")
    visible = models.BooleanField(default=False)

    @classmethod
    def get_list(cls,exclude=None):
        return cls.objects.all().order_by('nombre')

    @property
    def logo(self):

        if self.fotos.count() > 0:
            return self.fotos.all()[0].imagen.url
        else:
            return '/static/img/logo-vidascontadas.png'

    def save(self,*args,**kwargs):

        if not self.slug:
            self.slug = uuslug(self.nombre, instance=self)

        super(Comercio,self).save(*args,**kwargs)
        

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = "proyecto"
        ordering = ('nombre',)



class PlaceGeo(models.Model):
    nombre = models.CharField(max_length=100)
    geojson = FilerFileField(null=True, blank=True)

OPCIONES_LUGAR = (
    ('fosa', 'Fosa común'),
    ('cementerio', 'Cementerio'),
    ('lugar', 'Lugar'),
    ('hospital', 'Hospital'),
    ('campo_concentracion', 'Campo de concetración'),
    ('campo_trabajo', 'Campo de trabajo'),
)

class Place(models.Model):
    nombre = models.CharField(max_length=100)
    geo = models.ForeignKey(PlaceGeo,related_name="lugares",)
    tipo = models.CharField(max_length=100, choices=OPCIONES_LUGAR, default='lugar')
    direccion = RedactorField()
    localizacion = GeopositionField(default='42.813127326939224,-1.6393232345581055')
    datasets = models.ManyToManyField(Dataset,blank=True, related_name="mis_lugares")
    parent = models.ForeignKey('self',related_name="mas_lugares",)

    def __unicode__(self):
        return u"%s" % (self.nombre)

class CategoriaRepresiva(CategoryBase):
    """
    A simple example
    """    

    @classmethod    
    def get_list(cls,exclude=None):
        return cls.objects.filter(parent=None, active=True)

    class Meta:
        verbose_name_plural = u'Categorías represivas'


TIPO_ORGANIZACION = (
    ('P', 'Política'),
    ('S', 'Sindical'),
    ('R', 'Religiosa'),
    ('C', 'Cultural'),    
)

class Organizacion(LogicalDeletableModel):

    # identificacion
    nombre = models.CharField(max_length=255)
    descripcion = RedactorField()
    tipo = models.CharField(max_length=255, choices=TIPO_ORGANIZACION)

OPCIONES_SEXO = (
    ('H', 'Hombre'),
    ('M', 'Mujer'),
    ('U', 'Desconocido'),
)

OPCIONES_CIVIL = (
    ('S', 'Soltero'),
    ('C', 'Casado'),
    ('V', 'Viudo'),
    ('U', 'Desconocido'),
)

OPCIONES_PARENTESCO = (
    ('X', 'Cónyuge'),
    ('C', 'Hijo'),
    ('P', 'Progenitor'),
    ('H', 'Hermano'),    
    ('O', 'Otro'),
)

OPCIONES_FIABILIDAD = (
    ('A', 'Hecho documentado'),
    ('B', 'Testimonio directo'),
    ('C', 'Testimonio indirecto'),
    ('I', 'Indeterminado'),
)

class Person(LogicalDeletableModel):

    # identificacion
    nombre = models.CharField(max_length=255)
    apellido1 = models.CharField(max_length=255)
    apellido2 = models.CharField(max_length=255)

    sexo = models.CharField(max_length=100, choices=OPCIONES_SEXO, default='U')
    fecha_nacimiento = models.DateField(blank=True,null=True)
    fecha_muerte = models.DateField(blank=True,null=True)    
    a_nacimiento = models.PositiveIntegerField('Año de nacimiento', blank=True,null=True)
    a_muerte = models.PositiveIntegerField('Año de muerte', blank=True, null=True)
    lugar_nacimiento = models.ForeignKey(Place,related_name="nacidos_en", blank=True,null=True)
    lugar_residencia = models.ForeignKey(Place,related_name="residentes_en", blank=True,null=True)
    documento = models.CharField(verbose_name="Pasaporte, DNI, etc",  max_length=255, blank=True,null=True)

    # familia
    estado_civil = models.CharField(max_length=100, choices=OPCIONES_CIVIL, default='U')
    num_hijos = models.PositiveIntegerField('Número de hijos', blank=True, null=True, default='U')
    familiares = models.ManyToManyField('self', blank=True, related_name="parientes", through='Relaciones', symmetrical = False)

    # PERFIL SOCIODEMOGRAFICO
    estudios = models.CharField(max_length=255)
    oficio = models.CharField(max_length=255)
    nivel_socioeconomico = models.CharField(max_length=255)
    ideologia = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)

    # ADSCRIPCiÓN POLÍTICA
    afiliacion = models.ManyToManyField(Organizacion, blank=True, through='Afiliacion' ,related_name="afiliados")

    # MUERTE
    lugar_muerte = models.ForeignKey(Place,related_name="muertos_en",blank=True,null=True)
    lugar_enterramiento_muerte = models.ForeignKey(Place,related_name="enterrado_tras_muerte_en",blank=True,null=True)
    lugar_enterramiento_definitivo = models.ForeignKey(Place,related_name="enterrado_en",blank=True,null=True)

    # PERMISOS
    uso = models.BooleanField(default=True)
    difusion = models.BooleanField(default=False)
    explotacion = models.BooleanField(default=False)
    distribucion = models.BooleanField(default=False)

    datasets = models.ManyToManyField(Dataset, blank=True, related_name="mis_registros")

class Afiliacion(models.Model):

    # identificacion
    person = models.ForeignKey(Person, related_name="mis_organizaciones",)
    organizacion = models.ForeignKey(Organizacion,related_name="mis_afiliados",)
    cargo = models.CharField(max_length=255)
    
class Relaciones(models.Model):
    person1 = models.ForeignKey(Person, related_name="persona",)
    person2 = models.ForeignKey(Person, related_name="pariente",)
    parentesco = models.CharField(max_length=100, choices=OPCIONES_PARENTESCO, default='O')

class HechoRepresivo(models.Model):
    person = models.ForeignKey(Person,related_name="hechos",)
    categoria = models.ForeignKey(CategoriaRepresiva,related_name="categoria",)
    fecha_inicio = models.DateField(blank=True,null=True)
    fecha_fin = models.DateField(blank=True,null=True)
    lugar = models.ForeignKey(Place,related_name="sucesos",)
    victimario = models.ForeignKey(Person,related_name="victimario", blank=True,null=True)
    fuente = models.CharField(max_length=100)
    fiabilidad = models.CharField(max_length=100, choices=OPCIONES_FIABILIDAD, default='I')

    datasets = models.ManyToManyField(Dataset, blank=True, related_name="detalle_hechos")

    @property
    def edad(self):
        return 30 
    
class Biography(models.Model):
    person = models.ForeignKey(Person,related_name="biografias",)
    descripcion = RedactorField()



