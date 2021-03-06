# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-08-22 00:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sisyphus', '0013_auto_20180808_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='dlpanalysisinformation',
            name='verified',
            field=models.CharField(blank=True, choices=[('T', 'True'), ('F', 'False')], default='F', max_length=50, null=True, verbose_name='Verified'),
        ),
        migrations.AddField(
            model_name='pbalanalysisinformation',
            name='verified',
            field=models.CharField(blank=True, choices=[('T', 'True'), ('F', 'False')], default='F', max_length=50, null=True, verbose_name='Verified'),
        ),
        migrations.AddField(
            model_name='tenxanalysisinformation',
            name='verified',
            field=models.CharField(blank=True, choices=[('T', 'True'), ('F', 'False')], default='F', max_length=50, null=True, verbose_name='Verified'),
        ),
    ]
