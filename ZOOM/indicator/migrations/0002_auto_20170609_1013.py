# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-09 10:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicatorcategory',
            name='child',
        ),
        migrations.AddField(
            model_name='indicatorcategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='indicator.IndicatorCategory'),
        ),
    ]
