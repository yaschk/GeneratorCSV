from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import os
from django.conf import settings
from django.http import HttpResponse, Http404


@login_required(login_url='/login')
def index(request):
    user_datasets = Dataset.objects.filter(schema__owner=request.user)
    len_user_datasets = len(user_datasets)
    len_user_schemas = len(Schema.objects.filter(owner=request.user))
    return render(request, 'landing/index.html', locals())


@login_required(login_url='/create-schema')
def schema(request):

    type_dict = {'1': IntegerField,
                 '2': FullnameField,
                 '3': EmailField,
                 '4': JobField,
                 '5': DateField}

    if request.method == 'POST':
        schema_form = SchemaForm(request.user, request.POST)
        form = TypeFieldForm(request.POST)

        if form.is_valid() and schema_form.is_valid():
            schema_obj = Schema.objects.create(title=form.data['schema_title'], owner_id=request.user.id)

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
            return redirect('index')
    else:
        schema_form = SchemaForm(request.user)
        form = TypeFieldForm()
    return render(request, 'landing/schema.html', locals())


@login_required(login_url='/create-dataset')
def dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, user=request.user)
        if form.is_valid():
            Dataset.objects.create(rows_counter=int(form.data['rows_count']), schema_id=int(form.data['schema_id']))
            return redirect('index')
    else:
        form = DatasetForm(user=request.user)
    return render(request, 'landing/dataset.html', locals())


@login_required(login_url='/')
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

