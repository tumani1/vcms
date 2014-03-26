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

        # Adding model 'PersonsTopics'
        db.create_table('persons_topics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.Persons'], max_length=255)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['topics.Topics'], max_length=255)),
            ('t_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('t_character', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('persons', ['PersonsTopics'])

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
        db.send_create_signal('persons', ['UsersPersons'])


    def backwards(self, orm):
        # Deleting model 'Persons'
        db.delete_table('persons')

        # Removing M2M table for field media_content on 'Persons'
        db.delete_table(db.shorten_name('persons_media_content'))

        # Deleting model 'PersonsExtras'
        db.delete_table('persons_extras')

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
        'persons.personsextras': {
            'Meta': {'object_name': 'PersonsExtras', 'db_table': "'persons_extras'"},
            'cdn_name': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Persons']", 'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'persons.personstopics': {
            'Meta': {'object_name': 'PersonsTopics', 'db_table': "'persons_topics'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Persons']", 'max_length': '255'}),
            't_character': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            't_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['topics.Topics']", 'max_length': '255'})
        },
        'persons.userspersons': {
            'Meta': {'object_name': 'UsersPersons', 'db_table': "'users_persons'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Persons']"}),
            'rating': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['topics.Topics']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"})
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

    complete_apps = ['persons']