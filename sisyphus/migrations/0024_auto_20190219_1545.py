# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-02-19 23:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sisyphus', '0023_auto_20190131_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dlpanalysisinformation',
            name='lanes',
            field=models.ManyToManyField(blank=True, to='core.DlpLane'),
        ),
    ]