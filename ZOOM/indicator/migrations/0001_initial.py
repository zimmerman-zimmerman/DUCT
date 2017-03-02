# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-23 15:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geodata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100)),
            ],
        ),
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
                ('code', models.CharField(max_length=50)),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicator.Indicator')),
            ],
        ),
        migrations.CreateModel(
            name='IndicatorDatapoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_value', models.CharField(blank=True, max_length=20, null=True)),
                ('measure_value', models.CharField(blank=True, max_length=20, null=True)),
                ('other', models.CharField(blank=True, max_length=500, null=True)),
                ('country_id', models.ForeignKey(blank=True, db_column=b'country_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='geodata.Country')),
            ],
        ),
        migrations.CreateModel(
            name='IndicatorSource',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
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
            name='ScatterData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=255)),
                ('Indicator_1', models.CharField(max_length=255)),
                ('Indicator_1_value', models.CharField(max_length=20)),
                ('Indicator_2', models.CharField(max_length=255)),
                ('Indicator_2_value', models.CharField(max_length=20)),
                ('Country', models.CharField(max_length=100)),
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
            name='date_format_id',
            field=models.ForeignKey(blank=True, db_column=b'date_format_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='indicator.Time'),
        ),
        migrations.AddField(
            model_name='indicatordatapoint',
            name='file_source_id',
            field=models.ForeignKey(db_column=b'file_source_id', on_delete=django.db.models.deletion.CASCADE, to='indicator.FileSource'),
        ),
        migrations.AddField(
            model_name='indicatordatapoint',
            name='indicator_category_id',
            field=models.ForeignKey(blank=True, db_column=b'indicator_category_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='indicator.IndicatorCategory'),
        ),
        migrations.AddField(
            model_name='indicatordatapoint',
            name='indicator_id',
            field=models.ForeignKey(blank=True, db_column=b'indicator_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='indicator.Indicator'),
        ),
        migrations.AddField(
            model_name='indicatordatapoint',
            name='source_id',
            field=models.ForeignKey(blank=True, db_column=b'source_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='indicator.IndicatorSource'),
        ),
    ]
