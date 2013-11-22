from django.db import models

class NonDeletedManager(models.Manager):
    def get_query_set(self):
        return super(NonDeletedManager, self).get_query_set().filter(deleted=False)

class DeletedManager(models.Manager):
    def get_query_set(self):
        return super(DeletedManager, self).get_query_set().filter(deleted=True)

class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(published=True)


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    
    objects = NonDeletedManager()
    deleted_objects = DeletedManager()
    
    class Meta:
        abstract = True
    
    def delete(self):
        self.deleted = True
        self.save()

class PublishedModel(BaseModel):
    published = models.BooleanField("Publicado",default=False)
    objects_published = PublishedManager()
    
    class Meta:
        abstract = True