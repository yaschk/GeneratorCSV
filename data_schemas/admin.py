from django.contrib import admin
from .models import *


class FullnameInline(admin.TabularInline):
    model = FullnameField
    extra = 0


class EmailInline(admin.TabularInline):
    model = EmailField
    extra = 0


class JobInline(admin.TabularInline):
    model = JobField
    extra = 0


class IntegerInline(admin.TabularInline):
    model = IntegerField
    fields = ['title', 'min_value_range', 'max_value_range', 'numeration']
    extra = 0


class DateInline(admin.TabularInline):
    model = DateField
    extra = 0


class SchemaAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created', 'updated']
    inlines = [FullnameInline, EmailInline, JobInline, IntegerInline, DateInline]

    class Meta:
        model = Schema


admin.site.register(Schema, SchemaAdmin)


class DataSchemaAdmin(admin.ModelAdmin):
    list_display = ['schema', 'rows_counter', 'csv_file', 'created', 'updated']

    class Meta:
        model = Dataset


admin.site.register(Dataset, DataSchemaAdmin)
