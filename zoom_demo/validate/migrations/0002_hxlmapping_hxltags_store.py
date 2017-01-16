# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-16 10:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('validate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HXLmapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=50)),
                ('HXL_tag', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='HXLtags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HXL_tag', models.CharField(max_length=50)),
                ('value_type', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_source', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('indicator_type', models.CharField(max_length=50)),
                ('indicator', models.CharField(max_length=40)),
                ('unit', models.CharField(max_length=50)),
                ('subgroup', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('country_id', models.CharField(max_length=5)),
                ('date', models.DateField(verbose_name=b'Date')),
                ('source', models.CharField(max_length=5)),
                ('value', models.DecimalField(decimal_places=5, max_digits=20)),
                ('footnote', models.CharField(max_length=200)),
            ],
        ),
    ]
