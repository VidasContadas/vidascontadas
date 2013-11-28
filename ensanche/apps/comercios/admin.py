# coding=utf-8
from django.contrib import admin
from logicaldelete.admin import ModelAdmin as LogicalDeletableAdmin

import models

class Imagen(admin.TabularInline):
    model = models.Imagen
    max_num = 10
    extra = 0

class Comercio(LogicalDeletableAdmin):
    filter_horizontal = ('marcas','categorias',)
    inlines = (Imagen,)
    fieldsets = [
        ('', {'fields': ('nombre','slug','categorias')}),
        (u'Presentación', {'classes': ('full-width',), 'fields': ('presentacion',)}),
        ('', {'fields': ('imagen','marcas')}),
        ('Social', {'fields': ('facebook_url','twitter_url','googleplus_url','tuenti_url','instagram_url')}),
    ]

class Noticia(LogicalDeletableAdmin):
    exclude = ('date_created','date_modified','date_removed','deleted',"slug")
    list_filter = ('deleted','visible')
    list_display=("__unicode__","visible")

class Evento(LogicalDeletableAdmin):
    exclude = ('date_created','date_modified','date_removed','deleted',"slug")
    list_filter = ('deleted','visible')
    list_display=("__unicode__","visible")

class Oferta(LogicalDeletableAdmin):
	pass

class Categoria(admin.ModelAdmin):
    exclude = ('slug',)

#admin.site.register_app_label("swingtime", "Eventos")

admin.site.register(models.Comercio,Comercio)
admin.site.register(models.Noticia,Noticia)
admin.site.register(models.Oferta,Oferta)
admin.site.register(models.Categoria,Categoria)
admin.site.register(models.Evento,Evento)


