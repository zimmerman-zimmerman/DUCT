# Generated by Django 2.1.11 on 2019-09-04 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0007_auto_20190612_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='tags',
        ),
        migrations.DeleteModel(
            name='FileTags',
        ),
    ]
