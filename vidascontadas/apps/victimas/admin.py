from django.contrib import admin

import models

class Person(admin.ModelAdmin):
    pass 

admin.site.register(models.Person,Person)
# Register your models here.
