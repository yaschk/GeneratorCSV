# Generated by Django 3.2.9 on 2021-11-06 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Column title')),
                ('numeration', models.IntegerField(verbose_name='Order number')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Field template',
                'verbose_name_plural': 'Field templates',
            },
        ),
        migrations.CreateModel(
            name='EmailField',
            fields=[
                ('fieldtemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_schemas.fieldtemplate')),
            ],
            options={
                'verbose_name': 'Email field',
                'verbose_name_plural': 'Email fields',
            },
            bases=('data_schemas.fieldtemplate',),
        ),
        migrations.CreateModel(
            name='FullnameField',
            fields=[
                ('fieldtemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_schemas.fieldtemplate')),
            ],
            options={
                'verbose_name': 'Fullname field',
                'verbose_name_plural': 'Fullname fields',
            },
            bases=('data_schemas.fieldtemplate',),
        ),
        migrations.CreateModel(
            name='JobField',
            fields=[
                ('fieldtemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_schemas.fieldtemplate')),
            ],
            options={
                'verbose_name': 'Job field',
                'verbose_name_plural': 'Job fields',
            },
            bases=('data_schemas.fieldtemplate',),
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Schema',
                'verbose_name_plural': 'Schemas',
            },
        ),
        migrations.AddField(
            model_name='fieldtemplate',
            name='schema',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_schemas.schema', verbose_name='Schema'),
        ),
        migrations.CreateModel(
            name='DataSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rows_counter', models.BigIntegerField(blank=True, default=None, null=True, verbose_name='Raws counter')),
                ('status', models.CharField(choices=[('PR', 'Processing'), ('RD', 'Ready'), ('ER', 'Error')], default='PR', max_length=2, verbose_name='Status')),
                ('csv_file', models.FileField(blank=True, default=None, null=True, upload_to='csv_files/', verbose_name='CSV file')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_schemas.schema', verbose_name='Schema')),
            ],
            options={
                'verbose_name': 'Data schema',
                'verbose_name_plural': 'Data schemas',
            },
        ),
    ]
