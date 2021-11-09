from django import forms
from .models import Schema, Dataset


TYPE_CHOICES = (
    (1, "Integer"),
    (2, "Fullname"),
    (3, "Email"),
    (4, "Job"),
    (5, "Date"),
)


class SchemaForm(forms.Form):
    schema_title = forms.CharField(label='Schema title', required=True)

    class Meta:
        model = Schema

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        all_user_schemes = Schema.objects.filter(owner_id=self.user.id).values_list('title')
        for i in all_user_schemes:
            if data['schema_title'] == i[0]:
                raise forms.ValidationError("Title should be unique")
        return data


class TypeFieldForm(forms.Form):
    type = forms.ChoiceField(choices=TYPE_CHOICES, label="Field type", initial='',
                             widget=forms.Select(attrs={'class': 'type_dropdown'}), required=True)
    title = forms.CharField(label='Title', required=True)
    order_nmb = forms.IntegerField(label="Order number", required=True)
    min_value_range = forms.IntegerField(label="Min range value", required=False,
                                         widget=forms.NumberInput(attrs={'class': 'min_range_input'}))
    max_value_range = forms.IntegerField(label="Max range value", required=False,
                                         widget=forms.NumberInput(attrs={'class': 'max_range_input'}))


class DatasetForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.fields['schema_id'] = forms.ModelChoiceField(queryset=Schema.objects.filter(owner=user))
        self.fields['rows_count'] = forms.IntegerField(label="Number of rows", required=True)

    class Meta:
        model = Dataset


