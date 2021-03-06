# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-08-03 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20180705_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dlpsequencingdetail',
            name='sequencing_center',
            field=models.CharField(choices=[('BCCAGSC', 'BCCAGSC'), ('UBCBRC', 'UBCBRC')], default='BCCAGSC', max_length=50, null=True, verbose_name='Sequencing center'),
        ),
        migrations.AlterField(
            model_name='pbalsequencingdetail',
            name='sequencing_center',
            field=models.CharField(choices=[('BCCAGSC', 'BCCAGSC'), ('UBCBRC', 'UBCBRC')], default='BCCAGSC', max_length=50, null=True, verbose_name='Sequencing center'),
        ),
        migrations.AlterField(
            model_name='tenxsequencingdetail',
            name='sequencing_center',
            field=models.CharField(choices=[('BCCAGSC', 'BCCAGSC'), ('UBCBRC', 'UBCBRC')], default='BCCAGSC', max_length=50, null=True, verbose_name='Sequencing center'),
        ),
    ]
