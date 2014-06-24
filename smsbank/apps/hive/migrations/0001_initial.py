# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table(u'hive_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('online', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal(u'hive', ['Device'])

        # Adding model 'Sms'
        db.create_table(u'hive_sms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient', self.gf('django.db.models.fields.CharField')(max_length='100')),
            ('message', self.gf('django.db.models.fields.CharField')(max_length='10000')),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hive.Device'], null=True, blank=True)),
        ))
        db.send_create_signal(u'hive', ['Sms'])

        # Adding model 'DeviceList'
        db.create_table(u'hive_devicelist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='device_list', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'hive', ['DeviceList'])

        # Adding M2M table for field devices on 'DeviceList'
        m2m_table_name = db.shorten_name(u'hive_devicelist_devices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('devicelist', models.ForeignKey(orm[u'hive.devicelist'], null=False)),
            ('device', models.ForeignKey(orm[u'hive.device'], null=False))
        ))
        db.create_unique(m2m_table_name, ['devicelist_id', 'device_id'])


    def backwards(self, orm):
        # Deleting model 'Device'
        db.delete_table(u'hive_device')

        # Deleting model 'Sms'
        db.delete_table(u'hive_sms')

        # Deleting model 'DeviceList'
        db.delete_table(u'hive_devicelist')

        # Removing M2M table for field devices on 'DeviceList'
        db.delete_table(db.shorten_name(u'hive_devicelist_devices'))


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hive.device': {
            'Meta': {'object_name': 'Device'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'online': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'hive.devicelist': {
            'Meta': {'object_name': 'DeviceList'},
            'devices': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'profiles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['hive.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'device_list'", 'to': u"orm['auth.User']"})
        },
        u'hive.sms': {
            'Meta': {'object_name': 'Sms'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hive.Device']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': "'10000'"}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': "'100'"})
        }
    }

    complete_apps = ['hive']