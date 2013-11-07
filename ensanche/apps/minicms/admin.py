# coding=utf-8

import models

from django.contrib import admin
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
import os.path,re
from logicaldelete.admin import ModelAdmin as LogicalDeletableAdmin

from django.forms import ModelForm
from django.contrib.admin import ModelAdmin


class Page(LogicalDeletableAdmin):
    model = models.Page
    list_display = ('__unicode__','updated',)
    fieldsets = [
        ('', {'fields': ('titulo','slug','orden',)}),
        ('Contenido', {'classes': ('full-width',), 'fields': ('contenido',)}),
        ('Metadata', {'fields': ('meta_keywords','meta_description')}),
    ]
    #list_filter = ('language',)
    #list_display = ('__unicode__','language',)


admin.site.register(models.Page,Page)
#admin.site.register(models.Gallery,Gallery)
