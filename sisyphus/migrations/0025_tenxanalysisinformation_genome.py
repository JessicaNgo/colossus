# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-03-08 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sisyphus', '0024_auto_20190219_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenxanalysisinformation',
            name='genome',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Genome'),
        ),
    ]