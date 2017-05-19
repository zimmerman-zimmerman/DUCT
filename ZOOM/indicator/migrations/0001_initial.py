# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-19 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('file_upload', '0001_initial'),
        ('geodata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IndicatorCategory',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=255)),
                ('code', models.CharField(max_length=50)),
                ('level', models.IntegerField(default=0)),
                ('child', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='indicator.IndicatorCategory')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicator.Indicator')),
            ],
        ),
        migrations.CreateModel(
            name='IndicatorDatapoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('unit_of_measure', models.CharField(blank=True, max_length=20, null=True)),
                ('date_value', models.CharField(blank=True, max_length=20, null=True)),
                ('measure_value', models.CharField(blank=True, max_length=40, null=True)),
                ('other', models.CharField(blank=True, max_length=600, null=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geodata.Country')),
            ],
        ),
        migrations.CreateModel(
            name='IndicatorSource',
            fields=[
                ('id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=50)),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicator.Indicator')),
            ],
        ),
        migrations.CreateModel(
            name='MeasureValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('value_type', models.CharField(max_length=50)),
                ('value', models.DecimalField(decimal_places=5, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('date_type', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='indicatordatapoint',
            name='date_format',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='indicator.Time'),
        ),
        migrations.AddField(
            model_name='indicatordatapoint',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_upload.File'),
        ),
        migrations.AddField(
            model_name='indicatordatapoint',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='indicator.Indicator'),
        ),
        migrations.AddField(
            model_name='indicatordatapoint',
            name='indicator_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='indicator.IndicatorCategory'),
        ),
        migrations.AddField(
            model_name='indicatordatapoint',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='indicator.IndicatorSource'),
        ),
    ]
