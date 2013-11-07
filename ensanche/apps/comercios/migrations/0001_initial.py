# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Marca'
        db.create_table(u'comercios_marca', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('logo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filer.Image'])),
        ))
        db.send_create_signal(u'comercios', ['Marca'])

        # Adding model 'Comercio'
        db.create_table(u'comercios_comercio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_removed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
            ('presentacion', self.gf('redactor.fields.RedactorField')()),
            ('imagen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filer.Image'])),
            ('facebook_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('twitter_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('googleplus_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('tuenti_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('instagram_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'comercios', ['Comercio'])

        # Adding M2M table for field marcas on 'Comercio'
        m2m_table_name = db.shorten_name(u'comercios_comercio_marcas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comercio', models.ForeignKey(orm[u'comercios.comercio'], null=False)),
            ('marca', models.ForeignKey(orm[u'comercios.marca'], null=False))
        ))
        db.create_unique(m2m_table_name, ['comercio_id', 'marca_id'])

        # Adding model 'Imagen'
        db.create_table(u'comercios_imagen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comercio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['comercios.Comercio'])),
            ('imagen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filer.Image'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal(u'comercios', ['Imagen'])

        # Adding model 'Oferta'
        db.create_table(u'comercios_oferta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_removed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comercio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ofertas', to=orm['comercios.Comercio'])),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('imagen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filer.Image'])),
            ('texto', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'comercios', ['Oferta'])

        # Adding model 'Noticia'
        db.create_table(u'comercios_noticia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_removed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comercio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='noticias', to=orm['comercios.Comercio'])),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('imagen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filer.Image'])),
            ('texto', self.gf('redactor.fields.RedactorField')()),
        ))
        db.send_create_signal(u'comercios', ['Noticia'])


    def backwards(self, orm):
        # Deleting model 'Marca'
        db.delete_table(u'comercios_marca')

        # Deleting model 'Comercio'
        db.delete_table(u'comercios_comercio')

        # Removing M2M table for field marcas on 'Comercio'
        db.delete_table(db.shorten_name(u'comercios_comercio_marcas'))

        # Deleting model 'Imagen'
        db.delete_table(u'comercios_imagen')

        # Deleting model 'Oferta'
        db.delete_table(u'comercios_oferta')

        # Deleting model 'Noticia'
        db.delete_table(u'comercios_noticia')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'comercios.comercio': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Comercio'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'googleplus_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Image']"}),
            'instagram_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'marcas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['comercios.Marca']", 'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'presentacion': ('redactor.fields.RedactorField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'tuenti_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'twitter_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'comercios.imagen': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Imagen'},
            'comercio': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['comercios.Comercio']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Image']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'comercios.marca': {
            'Meta': {'object_name': 'Marca'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Image']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'comercios.noticia': {
            'Meta': {'ordering': "('titulo',)", 'object_name': 'Noticia'},
            'comercio': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'noticias'", 'to': u"orm['comercios.Comercio']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Image']"}),
            'texto': ('redactor.fields.RedactorField', [], {}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'comercios.oferta': {
            'Meta': {'ordering': "('titulo',)", 'object_name': 'Oferta'},
            'comercio': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ofertas'", 'to': u"orm['comercios.Comercio']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Image']"}),
            'texto': ('django.db.models.fields.TextField', [], {}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'filer.file': {
            'Meta': {'object_name': 'File'},
            '_file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'all_files'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'has_all_mandatory_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_files'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_filer.file_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.folder': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Folder'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'filer_owned_folders'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.image': {
            'Meta': {'object_name': 'Image', '_ormbases': ['filer.File']},
            '_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_alt_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'default_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['filer.File']", 'unique': 'True', 'primary_key': 'True'}),
            'must_always_publish_author_credit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'must_always_publish_copyright': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['comercios']