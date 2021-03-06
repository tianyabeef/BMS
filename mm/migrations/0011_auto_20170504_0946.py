# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-04 01:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mm', '0010_auto_20170111_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='total',
        ),
        migrations.AddField(
            model_name='contract',
            name='all_amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='总款额'),
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_file',
            field=models.FileField(blank=True, upload_to='uploads/%Y/%m', verbose_name='附件'),
        ),
        migrations.AddField(
            model_name='contract',
            name='fin_amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='尾款额'),
        ),
        migrations.AddField(
            model_name='contract',
            name='fin_date',
            field=models.DateField(blank=True, null=True, verbose_name='尾款到款日'),
        ),
        migrations.AddField(
            model_name='contract',
            name='fis_amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='首款额'),
        ),
        migrations.AddField(
            model_name='contract',
            name='fis_date',
            field=models.DateField(blank=True, null=True, verbose_name='首款到款日'),
        ),
        migrations.AddField(
            model_name='contract',
            name='type',
            field=models.IntegerField(choices=[(1, '16S/ITS'), (2, '宏基因组'), (3, '单菌'), (4, '转录组'), (5, '其它')], null=True, verbose_name='类型'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='content',
            field=models.TextField(null=True, verbose_name='发票内容'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='issuingUnit',
            field=models.CharField(max_length=25, null=True, verbose_name='开票单位'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='type',
            field=models.CharField(choices=[('CC', '普票'), ('SC', '专票')], default='CC', max_length=3, verbose_name='发票类型'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='contract_number',
            field=models.CharField(max_length=15, unique=True, verbose_name='合同号'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='name',
            field=models.CharField(max_length=100, verbose_name='合同名'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, verbose_name='单价'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='range',
            field=models.IntegerField(blank=True, choices=[(1, '高于销售底价'), (2, '总监底价'), (3, '低于总监底价')], verbose_name='价格区间'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='receive_date',
            field=models.DateField(blank=True, null=True, verbose_name='合同寄到日'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='salesman',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='业务员'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='send_date',
            field=models.DateField(blank=True, null=True, verbose_name='合同寄出日'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='note',
            field=models.TextField(null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='title',
            field=models.CharField(max_length=25, null=True, verbose_name='发票抬头'),
        ),
    ]
