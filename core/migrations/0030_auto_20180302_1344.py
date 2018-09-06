# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-03-02 21:44
from __future__ import unicode_literals

from django.db import migrations

def update_spotting_location(apps, schema_editor):

    DlpLibraryConstructionInformation = apps.get_model('core', 'DlpLibraryConstructionInformation')
    DlpLibraryConstructionInformation.objects.filter(spotting_location='A').update(spotting_location='AD')

    DlpLibrarySampleDetail = apps.get_model('core', 'DlpLibrarySampleDetail')
    DlpLibrarySampleDetail.objects.filter(spotting_location='A').update(spotting_location='AD')

    PbalLibrarySampleDetail = apps.get_model('core', 'PbalLibrarySampleDetail')
    PbalLibrarySampleDetail.objects.filter(spotting_location='A').update(spotting_location='AD')

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20180302_1003'),
    ]

    operations = [
        migrations.RunPython(update_spotting_location),
    ]
