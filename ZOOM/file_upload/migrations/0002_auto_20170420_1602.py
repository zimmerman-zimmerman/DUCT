# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-20 16:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='source',
            new_name='data_source',
        ),
    ]
