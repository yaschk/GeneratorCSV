# Generated by Django 3.2.9 on 2021-11-07 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_schemas', '0004_datefield'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DataSchema',
            new_name='CSVData',
        ),
    ]