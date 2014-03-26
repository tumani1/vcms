# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CDN'
        db.create_table('cdn', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('has_mobile', self.gf('django.db.models.fields.BooleanField')()),
            ('has_auth', self.gf('django.db.models.fields.BooleanField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('location_regexp', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('media_contents', ['CDN'])

        # Adding model 'MediaContents'
        db.create_table('media_contents', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('allow_mobile', self.gf('django.db.models.fields.BooleanField')()),
            ('allow_smarttv', self.gf('django.db.models.fields.BooleanField')()),
            ('allow_external', self.gf('django.db.models.fields.BooleanField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('views_cnt', self.gf('django.db.models.fields.IntegerField')()),
            ('mc_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('p_status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bio', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('media_contents', ['MediaContents'])

        # Adding M2M table for field tags on 'MediaContents'
        m2m_table_name = db.shorten_name('media_contents_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mediacontents', models.ForeignKey(orm['media_contents.mediacontents'], null=False)),
            ('tags', models.ForeignKey(orm['contents.tags'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mediacontents_id', 'tags_id'])

        # Adding model 'MediaContentLocations'
        db.create_table('media_content_locations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cdnname', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media_contents.CDN'])),
            ('media_content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media_contents.MediaContents'])),
            ('ltype', self.gf('django.db.models.fields.IntegerField')()),
            ('allow_mobile', self.gf('django.db.models.fields.BooleanField')()),
            ('allow_smarttv', self.gf('django.db.models.fields.BooleanField')()),
            ('allow_external', self.gf('django.db.models.fields.BooleanField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('views_cnt', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('media_contents', ['MediaContentLocations'])


    def backwards(self, orm):
        # Deleting model 'CDN'
        db.delete_table('cdn')

        # Deleting model 'MediaContents'
        db.delete_table('media_contents')

        # Removing M2M table for field tags on 'MediaContents'
        db.delete_table(db.shorten_name('media_contents_tags'))

        # Deleting model 'MediaContentLocations'
        db.delete_table('media_content_locations')


    models = {
        'contents.tags': {
            'Meta': {'object_name': 'Tags', 'db_table': "'tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'media_contents.cdn': {
            'Meta': {'object_name': 'CDN', 'db_table': "'cdn'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'has_auth': ('django.db.models.fields.BooleanField', [], {}),
            'has_mobile': ('django.db.models.fields.BooleanField', [], {}),
            'location_regexp': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'media_contents.mediacontentlocations': {
            'Meta': {'object_name': 'MediaContentLocations', 'db_table': "'media_content_locations'"},
            'allow_external': ('django.db.models.fields.BooleanField', [], {}),
            'allow_mobile': ('django.db.models.fields.BooleanField', [], {}),
            'allow_smarttv': ('django.db.models.fields.BooleanField', [], {}),
            'cdnname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media_contents.CDN']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ltype': ('django.db.models.fields.IntegerField', [], {}),
            'media_content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media_contents.MediaContents']"}),
            'views_cnt': ('django.db.models.fields.IntegerField', [], {})
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
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tags'", 'symmetrical': 'False', 'to': "orm['contents.Tags']"}),
            'views_cnt': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['media_contents']