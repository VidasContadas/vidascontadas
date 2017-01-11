from django.contrib import admin

import models

class Person(admin.ModelAdmin):
    pass 

class Dataset(admin.ModelAdmin):
    pass 

class Project(admin.ModelAdmin):
    pass 

class CategoriaRepresiva(admin.ModelAdmin):
    pass 

# Register your models here.
admin.site.register(models.Person,Person)
admin.site.register(models.Dataset,Dataset)
admin.site.register(models.Project,Project)
admin.site.register(models.CategoriaRepresiva,CategoriaRepresiva)