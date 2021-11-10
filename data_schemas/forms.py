from django import forms
from .models import Schema, Dataset


TYPE_CHOICES = (
    (1, "Integer"),
    (2, "Fullname"),
    (3, "Email"),
    (4, "Job"),
    (5, "Date"),
)


class SchemaForm(forms.ModelForm):
    schema_title = forms.CharField(label='Schema title', required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    separator = forms.ChoiceField(choices=Schema.Separator.choices, initial='', label='Column separator', required=True,
                                  widget=forms.Select(attrs={'class': 'type_dropdown form-select'}))
    string_char = forms.ChoiceField(choices=Schema.StringCharacter.choices, initial='', label='String character',
                                    required=True,
                                    widget=forms.Select(attrs={'class': 'type_dropdown form-select'}))

    class Meta:
        model = Schema
        fields = ['schema_title', 'separator', 'string_char']

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
    title = forms.CharField(label='Title', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(choices=TYPE_CHOICES, label="Field type", initial='',
                             widget=forms.Select(attrs={'class': 'type_dropdown form-select'}), required=True)
    min_value_range = forms.IntegerField(label="From", required=False,
                                         widget=forms.NumberInput(attrs={'class': 'form-control min_range_input'}))
    max_value_range = forms.IntegerField(label="To", required=False,
                                         widget=forms.NumberInput(attrs={'class': 'form-control max_range_input'}))
    order_nmb = forms.IntegerField(label="Order number", required=True,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))


class DatasetForm(forms.ModelForm):
    rows_counter = forms.IntegerField(label="Rows", required=True,
                                      widget=forms.TextInput(attrs={'class': 'form-control rows-form'}, ))

    class Meta:
        model = Dataset
        fields = ['rows_counter']
