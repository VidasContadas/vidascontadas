# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table(u'minicms_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_removed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('contenido', self.gf('redactor.fields.RedactorField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
            ('orden', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='es', max_length=255, db_index=True)),
            ('meta_keywords', self.gf('django.db.models.fields.TextField')()),
            ('meta_description', self.gf('django.db.models.fields.TextField')()),
            ('updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'minicms', ['Page'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table(u'minicms_page')


    models = {
        u'minicms.page': {
            'Meta': {'ordering': "('orden',)", 'object_name': 'Page'},
            'contenido': ('redactor.fields.RedactorField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'es'", 'max_length': '255', 'db_index': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {}),
            'orden': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['minicms']