# Generated by Django 2.1.3 on 2019-01-10 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0005_auto_20190110_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='iso2',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='geolocation',
            name='iso2',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
