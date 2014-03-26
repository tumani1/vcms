# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Topics'
        db.create_table('topics', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('release_date', self.gf('django.db.models.fields.DateField')()),
            ('s_status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_scheme', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('person_scheme', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_scheme', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('topics', ['Topics'])

        # Adding model 'TopicsExtras'
        db.create_table('topics_extras', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media_content', self.gf('django.db.models.fields.related.ForeignKey')(related_name='media_content_topics', to=orm['media_contents.MediaContents'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['topics.Topics'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('topics', ['TopicsExtras'])

        # Adding model 'TopicsPersonsExtend'
        db.create_table('topics_persons_extend', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.Persons'], max_length=255)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['topics.Topics'], max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value_int', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
            ('value_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('topics', ['TopicsPersonsExtend'])


    def backwards(self, orm):
        # Deleting model 'Topics'
        db.delete_table('topics')

        # Deleting model 'TopicsExtras'
        db.delete_table('topics_extras')

        # Deleting model 'TopicsPersonsExtend'
        db.delete_table('topics_persons_extend')


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
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tags'", 'symmetrical': 'False', 'to': "orm['contents.Tags']"}),
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
        'topics.topics': {
            'Meta': {'object_name': 'Topics', 'db_table': "'topics'"},
            'content_scheme': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'person_scheme': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'release_date': ('django.db.models.fields.DateField', [], {}),
            's_status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_scheme': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'topics.topicsextras': {
            'Meta': {'object_name': 'TopicsExtras', 'db_table': "'topics_extras'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media_content_topics'", 'to': "orm['media_contents.MediaContents']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['topics.Topics']"}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'topics.topicspersonsextend': {
            'Meta': {'object_name': 'TopicsPersonsExtend', 'db_table': "'topics_persons_extend'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Persons']", 'max_length': '255'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['topics.Topics']", 'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value_int': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'value_text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['topics']