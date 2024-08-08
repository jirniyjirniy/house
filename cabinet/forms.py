from datetime import datetime
from django.utils import timezone

from django import forms
from django.template.context_processors import request

from admin_panel.forms import FlatChoiceField
from admin_panel.models import Flat, Application


class ReceiptFilterForm(forms.Form):
    STATUS_CHOICE = (
        ('', ''),
        ('paid', 'Оплачена'),
        ('partially_paid', 'Частично оплачена'),
        ('unpaid', 'Не оплачена'),
    )

    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    daterange = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': '', 'class': 'daterange', 'value': ''}))


class CreateApplicationForm(forms.ModelForm):
    ROLE_CHOICE = (
        ('', 'Любой специалист'),
        ('director', 'Директор'),
        ('manager', 'Управляющий'),
        ('accountant', 'Бухгалтер'),
        ('electrician', 'Электрик'),
        ('plumber', 'Сантехник'),
    )
    date_published = forms.DateField(label='',
                                     widget=forms.DateInput(
                                         attrs={'class': 'publishing-date rounded-0', 'placeholder': ''}))
    time_published = forms.TimeField(label='',
                                     widget=forms.TimeInput(
                                         attrs={'class': 'publishing-time rounded-0', 'placeholder': ''}))

    flat = FlatChoiceField(queryset=Flat.objects.filter(house__isnull=False), label='Квартира',
                           widget=forms.Select(attrs={'class': 'form-flat-select select2 rounded-0'}))
    user_type = forms.ChoiceField(choices=ROLE_CHOICE, label='Тип мастера', required=False, widget=forms.Select(attrs={'class':'rounded-0  shadow-none'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'rounded-0', 'placeholder': '', 'rows': 8}),
                                  label='Описание')

    def __init__(self, *args, **kwargs):
        super(CreateApplicationForm, self).__init__(*args, **kwargs)
        self.fields['date_published'].initial = timezone.now().date()
        self.fields['time_published'].initial = datetime.now().time()
        self.fields['flat'].empty_label = "Выберите..."

    class Meta:
        model = Application
        fields = '__all__'
        exclude = ['comment', 'status', 'user']
