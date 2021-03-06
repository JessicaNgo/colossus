# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-18 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20180918_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='dlpsequencingdetail',
            name='lanes_received',
            field=models.BooleanField(default=False, verbose_name='Lanes Received'),
        ),
        migrations.AddField(
            model_name='dlpsequencingdetail',
            name='lanes_requested',
            field=models.BooleanField(default=False, verbose_name='Lanes Requested'),
        ),
        migrations.AddField(
            model_name='pbalsequencingdetail',
            name='lanes_received',
            field=models.BooleanField(default=False, verbose_name='Lanes Received'),
        ),
        migrations.AddField(
            model_name='pbalsequencingdetail',
            name='lanes_requested',
            field=models.BooleanField(default=False, verbose_name='Lanes Requested'),
        ),
        migrations.AddField(
            model_name='tenxsequencingdetail',
            name='lanes_received',
            field=models.BooleanField(default=False, verbose_name='Lanes Received'),
        ),
        migrations.AddField(
            model_name='tenxsequencingdetail',
            name='lanes_requested',
            field=models.BooleanField(default=False, verbose_name='Lanes Requested'),
        ),
        migrations.AlterField(
            model_name='dlplane',
            name='path_to_archive',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Path to archive'),
        ),
        migrations.AlterField(
            model_name='pballane',
            name='path_to_archive',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Path to archive'),
        ),
        migrations.AlterField(
            model_name='tenxlane',
            name='path_to_archive',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Path to archive'),
        ),
    ]
