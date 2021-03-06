# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-26 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0011_auto_20161226_1709'),
        ('lims', '0004_auto_20161223_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('EXT', '提取完成'), ('QC', '质检完成'), ('LIB', '建库完成')], default=None, max_length=3, verbose_name='进度')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pm.Sample', verbose_name='样品')),
            ],
            options={
                'verbose_name': '1.实验管理',
                'verbose_name_plural': '1.实验管理',
            },
        ),
    ]
