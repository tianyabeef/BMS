# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-04 02:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-timestamp',), 'verbose_name': '通知管理', 'verbose_name_plural': '通知管理'},
        ),
    ]
