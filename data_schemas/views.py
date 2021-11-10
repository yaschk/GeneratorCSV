from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import os
from django.conf import settings
from django.http import HttpResponse, Http404


@login_required(login_url='/login')
def index(request):
    """Schema list view"""
    user_schemas = Schema.objects.filter(owner=request.user)
    len_user_schemas = len(user_schemas)
    return render(request, 'landing/index.html', locals())


@login_required()
def create_schema(request):
    """Create schema view"""

    type_dict = {'1': IntegerField,
                 '2': FullnameField,
                 '3': EmailField,
                 '4': JobField,
                 '5': DateField}

    if request.method == 'POST':
        schema_form = SchemaForm(request.user, request.POST)
        form = TypeFieldForm(request.POST)

        if form.is_valid() and schema_form.is_valid():
            schema_obj = Schema.objects.create(title=form.data['schema_title'], owner_id=request.user.id,
                                               separator=form.data['separator'],
                                               string_char=form.data['string_char'])

            for ind, el in enumerate(request.POST.getlist('type')):
                type_model = type_dict.get(el)
                if el in ['1']:
                    type_model.objects.create(title=request.POST.getlist('title')[ind],
                                              numeration=request.POST.getlist('order_nmb')[ind],
                                              min_value_range=request.POST.getlist('min_value_range')[ind],
                                              max_value_range=request.POST.getlist('max_value_range')[ind],
                                              schema_id=schema_obj.id)
                else:
                    type_model.objects.create(title=request.POST.getlist('title')[ind],
                                              numeration=request.POST.getlist('order_nmb')[ind],
                                              schema_id=schema_obj.id)
            return redirect('create-datasets', schema_id=schema_obj.id)
    else:
        schema_form = SchemaForm(request.user)
        form = TypeFieldForm()
    return render(request, 'landing/schema.html', locals())


@login_required()
def delete_schema(request, schema_id):
    """Delete schema view"""
    schema_obj = get_object_or_404(Schema, id=schema_id, owner_id=request.user.id)
    schema_obj.delete()
    return redirect('index')


@login_required()
def datasets(request, schema_id):
    """Create dataset view"""
    if request.method == 'POST':
        form = DatasetForm(request.POST)
        if form.is_valid():
            Dataset.objects.create(rows_counter=int(form.data['rows_counter']), schema_id=schema_id)
    else:
        form = DatasetForm()

    schema_datasets = Dataset.objects.filter(schema_id=schema_id)
    len_schema_datasets = len(schema_datasets)

    return render(request, 'landing/dataset.html', locals())


@login_required()
def download(request, path):
    """Download CSV file view"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

