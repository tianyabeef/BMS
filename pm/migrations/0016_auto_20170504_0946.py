# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-04 01:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mm', '0011_auto_20170504_0946'),
        ('pm', '0015_auto_20170111_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtSubmit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='任务号')),
                ('date', models.DateField(blank=True, null=True, verbose_name='提交时间')),
                ('is_submit', models.BooleanField(verbose_name='提交')),
            ],
            options={
                'verbose_name_plural': '1提取任务下单',
                'verbose_name': '1提取任务下单',
            },
        ),
        migrations.CreateModel(
            name='LibSubmit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='任务号')),
                ('date', models.DateField(blank=True, null=True, verbose_name='提交时间')),
                ('is_submit', models.BooleanField(verbose_name='提交')),
            ],
            options={
                'verbose_name_plural': '3建库任务下单',
                'verbose_name': '3建库任务下单',
            },
        ),
        migrations.CreateModel(
            name='QcSubmit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='任务号')),
                ('date', models.DateField(blank=True, null=True, verbose_name='提交时间')),
                ('is_submit', models.BooleanField(verbose_name='提交')),
            ],
            options={
                'verbose_name_plural': '2质检任务下单',
                'verbose_name': '2质检任务下单',
            },
        ),
        migrations.RemoveField(
            model_name='sample',
            name='project',
        ),
        migrations.RemoveField(
            model_name='sequenceinfo',
            name='index',
        ),
        migrations.RemoveField(
            model_name='sequenceinfo',
            name='library',
        ),
        migrations.RemoveField(
            model_name='sequenceinfo',
            name='primer',
        ),
        migrations.RemoveField(
            model_name='sequenceinfo',
            name='sample',
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': '0项目管理', 'verbose_name_plural': '0项目管理'},
        ),
        migrations.AddField(
            model_name='project',
            name='ana_cycle',
            field=models.PositiveIntegerField(null=True, verbose_name='分析周期'),
        ),
        migrations.AddField(
            model_name='project',
            name='ana_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='分析完成日'),
        ),
        migrations.AddField(
            model_name='project',
            name='ana_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='分析开始日'),
        ),
        migrations.AddField(
            model_name='project',
            name='data_amount',
            field=models.CharField(max_length=10, null=True, verbose_name='数据要求'),
        ),
        migrations.AddField(
            model_name='project',
            name='data_date',
            field=models.DateField(blank=True, null=True, verbose_name='释放数据日'),
        ),
        migrations.AddField(
            model_name='project',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='合同节点'),
        ),
        migrations.AddField(
            model_name='project',
            name='ext_cycle',
            field=models.PositiveIntegerField(null=True, verbose_name='提取周期'),
        ),
        migrations.AddField(
            model_name='project',
            name='ext_date',
            field=models.DateField(blank=True, null=True, verbose_name='提取完成日'),
        ),
        migrations.AddField(
            model_name='project',
            name='ext_task_cycle',
            field=models.PositiveIntegerField(null=True, verbose_name='提取周期'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_confirm',
            field=models.BooleanField(default=False, verbose_name='确认'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_ext',
            field=models.BooleanField(default=False, verbose_name='需提取'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_lib',
            field=models.BooleanField(default=False, verbose_name='需建库'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_qc',
            field=models.BooleanField(default=False, verbose_name='需质检'),
        ),
        migrations.AddField(
            model_name='project',
            name='lib_cycle',
            field=models.PositiveIntegerField(null=True, verbose_name='建库周期'),
        ),
        migrations.AddField(
            model_name='project',
            name='lib_date',
            field=models.DateField(blank=True, null=True, verbose_name='建库完成日'),
        ),
        migrations.AddField(
            model_name='project',
            name='lib_task_cycle',
            field=models.PositiveIntegerField(null=True, verbose_name='建库周期'),
        ),
        migrations.AddField(
            model_name='project',
            name='qc_cycle',
            field=models.PositiveIntegerField(null=True, verbose_name='质检周期'),
        ),
        migrations.AddField(
            model_name='project',
            name='qc_date',
            field=models.DateField(blank=True, null=True, verbose_name='质检完成日'),
        ),
        migrations.AddField(
            model_name='project',
            name='qc_task_cycle',
            field=models.PositiveIntegerField(null=True, verbose_name='质检周期'),
        ),
        migrations.AddField(
            model_name='project',
            name='report_date',
            field=models.DateField(blank=True, null=True, verbose_name='释放报告日'),
        ),
        migrations.AddField(
            model_name='project',
            name='result_date',
            field=models.DateField(blank=True, null=True, verbose_name='释放结果日'),
        ),
        migrations.AddField(
            model_name='project',
            name='seq_cycle',
            field=models.PositiveIntegerField(null=True, verbose_name='测序周期'),
        ),
        migrations.AddField(
            model_name='project',
            name='seq_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='测序完成日'),
        ),
        migrations.AddField(
            model_name='project',
            name='seq_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='测序开始日'),
        ),
        migrations.AddField(
            model_name='project',
            name='service_type',
            field=models.CharField(max_length=50, null=True, verbose_name='服务类型'),
        ),
        migrations.AlterField(
            model_name='project',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mm.Contract', verbose_name='合同号'),
        ),
        migrations.AlterField(
            model_name='project',
            name='customer',
            field=models.CharField(max_length=20, verbose_name='客户'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(blank=True, max_length=100, verbose_name='项目注解'),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('contract', 'name')]),
        ),
        migrations.DeleteModel(
            name='Library',
        ),
    ]