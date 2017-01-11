# coding=utf-8
from django.contrib import admin
from logicaldelete.admin import ModelAdmin as LogicalDeletableAdmin
from geoposition.forms import GeopositionField

import models

class PropuestasInline(admin.TabularInline):
    model = models.Propuesta
    fields = ('titulo', 'visible')
    max_num = 10
    extra = 0

class LocalInline(admin.TabularInline):
    model = models.Local
    fields = ('nombre', 'localizacion')
    max_num = 10
    extra = 0

class ImagenInline(admin.TabularInline):
    model = models.Imagen
    fields = ('imagen', 'visible')
    max_num = 10
    extra = 0

class Comercio(LogicalDeletableAdmin):
    list_display = ('nombre', 'asociado', 'visible')
    search_fields= ('nombre', 'asociado', 'presentacion')
    inlines = (LocalInline, ImagenInline, PropuestasInline)

class CategoriaComercio(admin.ModelAdmin):
    exclude = ('slug',)

class Imagen(admin.ModelAdmin):
    exclude = ('slug',)

class Local(admin.ModelAdmin):
    localizacion = GeopositionField(initial='42.813127326939224,-1.6393232345581055')
    
class Pagina(admin.ModelAdmin):
    pass    

class Propuesta(admin.ModelAdmin):
    list_display = ('comercio', 'titulo', 'visible')  
    search_fields= ('comercio', 'titulo', 'presentacion')

admin.site.register(models.Propuesta,Propuesta)
admin.site.register(models.Pagina,Pagina)
admin.site.register(models.Local,Local)
admin.site.register(models.Imagen,Imagen)
admin.site.register(models.Comercio,Comercio)
admin.site.register(models.CategoriaComercio,CategoriaComercio)



