# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-08-08 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sisyphus', '0012_auto_20180803_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dlpanalysisinformation',
            name='blob_path',
        ),
        migrations.RemoveField(
            model_name='dlpanalysisinformation',
            name='sftp_path',
        ),
        migrations.RemoveField(
            model_name='pbalanalysisinformation',
            name='blob_path',
        ),
        migrations.RemoveField(
            model_name='pbalanalysisinformation',
            name='sftp_path',
        ),
        migrations.RemoveField(
            model_name='tenxanalysisinformation',
            name='blob_path',
        ),
        migrations.RemoveField(
            model_name='tenxanalysisinformation',
            name='sftp_path',
        ),
        migrations.AddField(
            model_name='analysisrun',
            name='blob_path',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Blob path'),
        ),
        migrations.AddField(
            model_name='analysisrun',
            name='sftp_path',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='sftp path'),
        ),
    ]