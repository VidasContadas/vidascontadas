# coding=utf-8
from django.contrib import admin
from logicaldelete.admin import ModelAdmin as LogicalDeletableAdmin

import models

class Imagen(admin.TabularInline):
    model = models.Imagen
    max_num = 10
    extra = 0

class Comercio(LogicalDeletableAdmin):
	filter_horizontal = ('marcas',)
	inlines = (Imagen,)
	fieldsets = [
        ('', {'fields': ('nombre','slug',)}),
        (u'Presentación', {'classes': ('full-width',), 'fields': ('presentacion',)}),
        ('', {'fields': ('imagen','marcas')}),
        ('Social', {'fields': ('facebook_url','twitter_url','googleplus_url','tuenti_url','instagram_url')}),
    ]

class Noticia(LogicalDeletableAdmin):
	pass

class Oferta(LogicalDeletableAdmin):
	pass

#admin.site.register_app_label("swingtime", "Eventos")

admin.site.register(models.Comercio,Comercio)
admin.site.register(models.Noticia,Noticia)
admin.site.register(models.Oferta,Oferta)


