# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contents'
        db.create_table('contents', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('obj_id', self.gf('django.db.models.fields.IntegerField')()),
            ('obj_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('obj_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
        ))
        db.send_create_signal('contents', ['Contents'])

        # Adding model 'ContentsExtends'
        db.create_table('contents_extends', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contents.Contents'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value_int', self.gf('django.db.models.fields.IntegerField')()),
            ('value_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('contents', ['ContentsExtends'])

        # Adding model 'Tags'
        db.create_table('tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('contents', ['Tags'])


    def backwards(self, orm):
        # Deleting model 'Contents'
        db.delete_table('contents')

        # Deleting model 'ContentsExtends'
        db.delete_table('contents_extends')

        # Deleting model 'Tags'
        db.delete_table('tags')


    models = {
        'contents.contents': {
            'Meta': {'object_name': 'Contents', 'db_table': "'contents'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obj_id': ('django.db.models.fields.IntegerField', [], {}),
            'obj_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'obj_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'contents.contentsextends': {
            'Meta': {'object_name': 'ContentsExtends', 'db_table': "'contents_extends'"},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contents.Contents']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value_int': ('django.db.models.fields.IntegerField', [], {}),
            'value_text': ('django.db.models.fields.TextField', [], {})
        },
        'contents.tags': {
            'Meta': {'object_name': 'Tags', 'db_table': "'tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['contents']