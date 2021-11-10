from GeneratorCSV.celery import celery_app
from django.apps import apps
import csv


@celery_app.task()
def generate_data(instance_id):

    # loading models
    Dataset = apps.get_model(app_label='data_schemas', model_name='Dataset')
    FullnameField = apps.get_model(app_label='data_schemas', model_name='FullnameField')
    EmailField = apps.get_model(app_label='data_schemas', model_name='EmailField')
    JobField = apps.get_model(app_label='data_schemas', model_name='JobField')
    IntegerField = apps.get_model(app_label='data_schemas', model_name='IntegerField')
    DateField = apps.get_model(app_label='data_schemas', model_name='DateField')
    FieldTemplate = apps.get_model(app_label='data_schemas', model_name='FieldTemplate')
    Schema = apps.get_model(app_label='data_schemas', model_name='Schema')

    instance = Dataset.objects.get(id=instance_id)

    schema_obj = Schema.objects.get(id=instance.schema_id)

    schema_fields = [FullnameField, EmailField, JobField, IntegerField, DateField]
    fields = []
    csv_title = 'static/media/csv_files/{}.csv'.format(instance_id)

    for _field in schema_fields:
        for _instance in _field.objects.filter(schema_id=instance.schema_id):
            if FieldTemplate in _instance.__class__.__bases__:
                fields.append((_instance.title, _instance.numeration,
                               _field.generate_random_data(instance.rows_counter)))
            else:  # FieldWithRangeTemplate
                fields.append((_instance.title, _instance.numeration,
                               _field.generate_random_data(_instance, instance.rows_counter)))
    fields.sort(key=lambda x: x[1])
    headers = [x[0] for x in fields]

    with open(csv_title, 'w', encoding='UTF8') as f:
        print(schema_obj.get_separator_value)
        writer = csv.writer(f, delimiter=schema_obj.get_separator_value, quotechar=schema_obj.get_string_char,
                            quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)

        for row_index in range(instance.rows_counter):
            data = [x[2][row_index] for x in fields]
            writer.writerow(data)
    instance.csv_file = csv_title.replace('static/media', '')
    instance.status = "RD"
    instance.save()
