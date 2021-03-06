# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-26 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170517_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsequencing',
            name='index_read_type',
            field=models.CharField(blank=True, default='Dual Index (i7 and i5)', max_length=50, null=True, verbose_name='Index read type'),
        ),
        migrations.AlterField(
            model_name='sequencing',
            name='index_read_type',
            field=models.CharField(blank=True, default='Dual Index (i7 and i5)', max_length=50, null=True, verbose_name='Index read type'),
        ),
    ]
