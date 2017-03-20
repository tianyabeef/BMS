# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-26 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0005_experiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='status',
            field=models.CharField(choices=[('WAI', '等待实验'), ('EXT', '提取完成'), ('QC', '质检完成'), ('LIB', '建库完成')], default='WAI', max_length=3, verbose_name='进度'),
        ),
    ]
