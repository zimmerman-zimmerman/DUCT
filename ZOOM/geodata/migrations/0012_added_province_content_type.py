# Generated by Django 2.1.3 on 2019-02-20 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0011_removed_unique_from_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geolocation',
            name='type',
            field=models.CharField(choices=[('country', 'country'), ('region', 'region'), ('subnational', 'subnational'), ('city', 'city'), ('pointbased', 'pointbased'), ('province', 'province')], max_length=100),
        ),
    ]
