# Generated by Django 3.2.9 on 2021-11-10 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_schemas', '0009_alter_dataset_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='separator',
            field=models.CharField(default=1, max_length=10, verbose_name='Separator'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schema',
            name='string_char',
            field=models.CharField(default=1, max_length=10, verbose_name='String character'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='rows_counter',
            field=models.BigIntegerField(default=None, verbose_name='Rows counter'),
        ),
    ]
