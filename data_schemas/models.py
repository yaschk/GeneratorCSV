from .tasks import generate_data
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
import random
from django.contrib.staticfiles import finders
import string
import datetime


class Schema(models.Model):
    """User`s schema model instance"""

    title = models.CharField(max_length=50, unique=True, blank=False, null=False, verbose_name="Title")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, db_index=True,
                              verbose_name="Owner")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Created')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Updated')

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = "Schema"
        verbose_name_plural = "Schemas"


class Dataset(models.Model):
    """Dataset model instance"""
    class Status(models.TextChoices):
        """Data schema statuses"""
        Processing = 'PR', 'Processing'
        Ready = 'RD', 'Ready'

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Schema")
    rows_counter = models.BigIntegerField(blank=False, null=False, default=None, verbose_name="Rows counter")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.Processing, blank=False, null=False,
                              verbose_name="Status")
    csv_file = models.FileField(upload_to='csv_files/', blank=True, null=True, default=None, verbose_name="CSV file")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Created')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Updated')

    def __str__(self):
        return '%s - %s (%s)' % (self.schema, self.schema.owner, self.status)

    class Meta:
        verbose_name = "Dataset"
        verbose_name_plural = "Dataset"


class FieldTemplate(models.Model):
    """Field template model"""
    title = models.CharField(max_length=50, blank=False, null=False, verbose_name="Column title")
    numeration = models.IntegerField(blank=False, null=False, verbose_name="Order number")
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, blank=False, null=False, db_index=True,
                               verbose_name="Schema")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Created')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Updated')

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = "Field template"
        verbose_name_plural = "Field templates"


class FieldWithRangeTemplate(FieldTemplate):
    """Field with range template model"""
    min_value_range = models.BigIntegerField(blank=False, null=False, verbose_name="Min value range")
    max_value_range = models.BigIntegerField(blank=False, null=False, verbose_name="Max value range")

    def clean(self):
        if self.min_value_range >= self.max_value_range:
            raise ValidationError("The minimum value must be less than the maximum")

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = "Field with range template"
        verbose_name_plural = "Field with range templates"


class FullnameField(FieldTemplate):
    """Fullname field data model instance"""

    @staticmethod
    def generate_random_data(rows_count):
        data_arr = []
        for p in ['prepared_data/FirstNames.csv', 'prepared_data/LastNames.csv']:
            file_path = finders.find(p)
            with open(file_path, 'r') as f:
                data = f.read().splitlines()
            while len(data) < rows_count:
                data = data + data
            random.shuffle(data)
            data_arr.append(data)
        return ["{} {}".format(x[0].capitalize(), x[1].capitalize())
                for x in zip(data_arr[0][:rows_count], data_arr[1][:rows_count])]

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = "Fullname field"
        verbose_name_plural = "Fullname fields"


class EmailField(FieldTemplate):
    """Email field data model instance"""

    @staticmethod
    def generate_random_data(rows_count):
        def make_email():
            extensions = ['com', 'net', 'org', 'gov']
            domains = ['gmail', 'yahoo', 'comcast', 'verizon', 'charter', 'hotmail', 'outlook', 'frontier']
            winext = extensions[random.randint(0, len(extensions) - 1)]
            windom = domains[random.randint(0, len(domains) - 1)]
            acclen = random.randint(1, 20)
            winacc = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(acclen))
            finale = winacc + "@" + windom + "." + winext
            return finale

        return [make_email() for _ in range(rows_count)]

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = "Email field"
        verbose_name_plural = "Email fields"


class JobField(FieldTemplate):
    """Job field data model instance"""

    @staticmethod
    def generate_random_data(rows_count):
        file_path = finders.find('prepared_data/Jobs.csv')
        with open(file_path, 'r') as f:
            data = f.read().splitlines()
        while len(data) < rows_count:
            data = data + data
        random.shuffle(data)
        return [x.capitalize() for x in data]

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = "Job field"
        verbose_name_plural = "Job fields"


class IntegerField(FieldWithRangeTemplate):
    """Integer field data model instance"""

    def generate_random_data(self, rows_count):
        return [random.randint(self.min_value_range, self.max_value_range) for _ in range(rows_count)]

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = "Integer field"
        verbose_name_plural = "Integer fields"


class DateField(FieldTemplate):
    """Date field data model instance"""

    @staticmethod
    def generate_random_data(rows_count):
        def get_random_date(year):
            try:
                return datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), year), '%j %Y').date()

            except ValueError:
                get_random_date(year)
        return [get_random_date(random.randint(1900, datetime.datetime.now().year)) for _ in range(rows_count)]

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = "Date field"
        verbose_name_plural = "Date fields"


@receiver(post_save, sender=Dataset)
def data_schema_created(sender, instance, created, **kwargs):
    if created:
        generate_data.delay(instance.id)
