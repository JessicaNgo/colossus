# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-26 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20170628_1502'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sublibraryinformation',
            old_name='spot_class',
            new_name='condition'
        ),
        migrations.AlterField(
            model_name='sublibraryinformation',
            name='condition',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Condition'),
        ),
    ]