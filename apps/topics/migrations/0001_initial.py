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

        # Adding model 'PersonsTopics'
        db.create_table('persons_topics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person_topics', max_length=255, to=orm['persons.Persons'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['topics.Topics'], max_length=255)),
            ('t_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('t_character', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('topics', ['PersonsTopics'])

        # Adding model 'UsersPersons'
        db.create_table('users_persons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.Persons'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['topics.Topics'])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')()),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('topics', ['UsersPersons'])


    def backwards(self, orm):
        # Deleting model 'Topics'
        db.delete_table('topics')

        # Deleting model 'TopicsExtras'
        db.delete_table('topics_extras')

        # Deleting model 'TopicsPersonsExtend'
        db.delete_table('topics_persons_extend')

        # Deleting model 'PersonsTopics'
        db.delete_table('persons_topics')

        # Deleting model 'UsersPersons'
        db.delete_table('users_persons')


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
        'topics.personstopics': {
            'Meta': {'object_name': 'PersonsTopics', 'db_table': "'persons_topics'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_topics'", 'max_length': '255', 'to': "orm['persons.Persons']"}),
            't_character': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            't_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['topics.Topics']", 'max_length': '255'})
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
        },
        'topics.userspersons': {
            'Meta': {'object_name': 'UsersPersons', 'db_table': "'users_persons'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Persons']"}),
            'rating': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['topics.Topics']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"})
        },
        'users.users': {
            'Meta': {'object_name': 'Users', 'db_table': "'users'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'time_zone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'userpic_id': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['users.UsersPics']", 'null': 'True', 'blank': 'True'}),
            'userpic_type': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'users.userspics': {
            'Meta': {'object_name': 'UsersPics', 'db_table': "'users_pics'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"})
        }
    }

    complete_apps = ['topics']