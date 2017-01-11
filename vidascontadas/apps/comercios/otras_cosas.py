class Marca(models.Model):
    nombre = models.CharField(max_length=255,unique=True)
    logo = FilerImageField()

    def __unicode__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(unique=True)

    @classmethod
    def get_list(cls,categoria=None,):
        return cls.objects.exclude(comercios=None)

    def __unicode__(self):
        return self.nombre

    def save(self,*args,**kwargs):

        self.slug = slugify(self.nombre)

        super(Categoria,self).save(*args,**kwargs)

    class Meta:
        ordering = ('nombre',)


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

class Evento(LogicalDeletableAdmin):
    exclude = ('date_created','date_modified','date_removed','deleted',"slug")
    list_filter = ('deleted','visible')
    list_display=("__unicode__","visible")

class Oferta(LogicalDeletableAdmin):
    pass
        