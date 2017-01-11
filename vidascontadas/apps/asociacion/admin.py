from django.contrib import admin
from logicaldelete.admin import ModelAdmin as LogicalDeletableAdmin
from django.template.defaultfilters import slugify
from categories.admin import CategoryBaseAdmin
from adminsortable.admin import SortableAdmin
from datetimewidget.widgets import DateTimeWidget
from django.db.models import DateTimeField

from cicu.models import *
from categories.models import *
from minicms.models import *

from cicu.widgets import CicuUploaderInput

import models

class ConvenioAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    pass

class CategoriaConvenioAdmin(CategoryBaseAdmin):
    pass

class NoticiaAdmin(LogicalDeletableAdmin):
    exclude = ('date_created','date_modified','date_removed','deleted',"slug","autor")
    list_filter = ('deleted','visible')
    list_display=("__unicode__","visible")

    #formfield_overrides = {
    #    DateTimeField: {'widget': DateTimeWidget }
    #}

    def save_model(self, request, obj, form, change):
        obj.slug = slugify('%s' % (obj.titulo))
        if not obj.id:
            obj.autor = request.user
        obj.save()


class CategoriaAsociadoAdmin(CategoryBaseAdmin):
    pass

class AsociadoAdmin(admin.ModelAdmin):
    search_fields = ['nombre',]
    pass

class SlidesAdmin(SortableAdmin):
    pass

class BannerAdmin(admin.ModelAdmin):
    pass

class EventosAdmin(admin.ModelAdmin):

    cicuOptions = {
            'ratioWidth': '460',       #fix-width ratio, default 0
            'ratioHeight':'590',       #fix-height ratio , default 0
            'sizeWarning': 'False',    #if True the crop selection have to respect minimal ratio size defined above. Default 'False'
        }
    widgets = {
            'imagen': CicuUploaderInput(options=cicuOptions)
        }

    filter_horizontal = ('participantes',)

admin.site.register(models.Evento, EventosAdmin)
admin.site.register(models.Slides, SlidesAdmin)
admin.site.register(models.CategoriaAsociado, CategoriaAsociadoAdmin)
admin.site.register(models.Asociado,AsociadoAdmin)
admin.site.register(models.CategoriaConvenio, CategoriaConvenioAdmin)
admin.site.register(models.Convenio, ConvenioAdmin)
admin.site.register(models.Noticia, NoticiaAdmin)
admin.site.register(models.Banner, BannerAdmin)

admin.site.unregister(UploadedFile)
admin.site.unregister(Category)
admin.site.unregister(Page)
