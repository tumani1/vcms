# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comments'
        db.create_table('comments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ctext', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
            ('obj_id', self.gf('django.db.models.fields.IntegerField')()),
            ('obj_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('obj_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('comments', ['Comments'])

        # Adding model 'UsersComments'
        db.create_table('users_comments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user', to=orm['users.Users'])),
            ('uc_status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uc_rating', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
        ))
        db.send_create_signal('comments', ['UsersComments'])


    def backwards(self, orm):
        # Deleting model 'Comments'
        db.delete_table('comments')

        # Deleting model 'UsersComments'
        db.delete_table('users_comments')


    models = {
        'comments.comments': {
            'Meta': {'object_name': 'Comments', 'db_table': "'comments'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ctext': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obj_id': ('django.db.models.fields.IntegerField', [], {}),
            'obj_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'obj_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'max_length': '255'})
        },
        'comments.userscomments': {
            'Meta': {'object_name': 'UsersComments', 'db_table': "'users_comments'"},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uc_rating': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'uc_status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user'", 'to': "orm['users.Users']"})
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

    complete_apps = ['comments']