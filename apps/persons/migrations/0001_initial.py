# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Persons'
        db.create_table('persons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('p_status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bio', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('persons', ['Persons'])

        # Adding M2M table for field media_content on 'Persons'
        m2m_table_name = db.shorten_name('persons_media_content')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('persons', models.ForeignKey(orm['persons.persons'], null=False)),
            ('mediacontents', models.ForeignKey(orm['media_contents.mediacontents'], null=False))
        ))
        db.create_unique(m2m_table_name, ['persons_id', 'mediacontents_id'])

        # Adding model 'PersonsExtras'
        db.create_table('persons_extras', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.Persons'], max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cdn_name', self.gf('django.db.models.fields.TextField')()),
            ('location', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('persons', ['PersonsExtras'])


    def backwards(self, orm):
        # Deleting model 'Persons'
        db.delete_table('persons')

        # Removing M2M table for field media_content on 'Persons'
        db.delete_table(db.shorten_name('persons_media_content'))

        # Deleting model 'PersonsExtras'
        db.delete_table('persons_extras')


    models = {
        'contents.tags': {
            'Meta': {'object_name': 'Tags', 'db_table': "'tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'media_contents.mediacontents': {
            'Meta': {'object_name': 'MediaContents', 'db_table': "'media_contents'"},
            'allow_external': ('django.db.models.fields.BooleanField', [], {}),
            'allow_mobile': ('django.db.models.fields.BooleanField', [], {}),
            'allow_smarttv': ('django.db.models.fields.BooleanField', [], {}),
            'bio': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mc_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'p_status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contents_tags'", 'symmetrical': 'False', 'to': "orm['contents.Tags']"}),
            'views_cnt': ('django.db.models.fields.IntegerField', [], {})
        },
        'persons.persons': {
            'Meta': {'object_name': 'Persons', 'db_table': "'persons'"},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'media_content': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'media_content_persons'", 'symmetrical': 'False', 'to': "orm['media_contents.MediaContents']"}),
            'p_status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'persons.personsextras': {
            'Meta': {'object_name': 'PersonsExtras', 'db_table': "'persons_extras'"},
            'cdn_name': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Persons']", 'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['persons']