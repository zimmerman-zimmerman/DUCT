# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-19 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0004_filedtypes_dtype_dict_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='mapping_used',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
