import datetime

from django.db import models

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^logicaldelete\.fields\.LastModifiedDateField"])

class LastModifiedDateField(models.DateTimeField):
    
    def pre_save(self, model_instance, add):
        setattr(model_instance, self.attname, datetime.datetime.now())
        return getattr(model_instance, self.attname)
