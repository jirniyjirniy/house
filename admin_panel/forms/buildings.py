import django.forms as forms
from django.db.models import Q
from django.forms import modelformset_factory

from ..models import *


class HouseForm(forms.ModelForm):
    title = forms.CharField(label='Название', max_length=100,required=False,
                            widget=forms.TextInput(attrs={'placeholder': ''}))
    address = forms.CharField(label='Адрес', max_length=100,required=False,
                              widget=forms.TextInput(attrs={'placeholder': ''}))

    class Meta:
        model = House
        fields = ('title', 'address')


class HouseUserForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Personal.objects.all(), label='ФИО',
                                  widget=forms.Select(attrs={'class': 'form-role-select'}))

    class Meta:
        model = HouseUser
        fields = ('user',)


HouseUserFormset = forms.modelformset_factory(model=HouseUser, form=HouseUserForm, can_delete=True, extra=0)


class SectionForm(forms.ModelForm):
    title = forms.CharField(label='Название', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': ''}))

    class Meta:
        model = Section
        fields = ('title',)


SectionFormset = forms.modelformset_factory(model=Section, form=SectionForm, can_delete=True, extra=0)


class FloorForm(forms.ModelForm):
    title = forms.CharField(label='Название', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': ''}))

    class Meta:
        model = Floor
        fields = ('title',)


FloorFormset = forms.modelformset_factory(model=Floor, form=FloorForm, can_delete=True, extra=0)


class FlatForm(forms.ModelForm):
    number = forms.CharField(label='Номер квартиры',
                             widget=forms.TextInput(attrs={'class': 'number', 'placeholder': ''}))
    square = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': ''}),required=False,label='Площадь')
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label='Секция', required=False,
                                     widget=forms.Select(attrs={'class': 'form-section-select'}))
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), label='Этаж', required=False,
                                   widget=forms.Select(attrs={'class': 'form-floor-select'}))
    house = forms.ModelChoiceField(queryset=House.objects.all(), label='Дом',
                                   widget=forms.Select(attrs={'class': 'form-house-select'}))
    personal_account_res = forms.CharField(label='Лицевой счёт', required=False, widget=forms.TextInput(
        attrs={'class': 'personal_account-res', 'placeholder': ''}))
    personal_account = forms.ModelChoiceField(queryset=PersonalAccount.objects.filter(flat__isnull=True),
                                              widget=forms.Select(attrs={'class': 'personal_account-select'}), label='',
                                              required=False)

    def __init__(self, *args, **kwargs):
        super(FlatForm, self).__init__(*args, **kwargs)

        self.fields['personal_account'].queryset = PersonalAccount.objects.filter(flat__isnull=True)

        self.fields['house'].empty_label = "Выберите..."
        self.fields['section'].empty_label = "Выберите..."
        self.fields['floor'].empty_label = "Выберите..."
        self.fields['flat_owner'].empty_label = "Выберите..."
        self.fields['tariff'].empty_label = "Выберите..."
        self.fields['personal_account'].empty_label = "или выберите из списка..."
        if self.instance.pk:
            if hasattr(self.instance, 'personal_account'):
                self.fields['personal_account_res'].initial = self.instance.personal_account
                self.fields['personal_account'].queryset = PersonalAccount.objects.filter(
                    Q(flat__isnull=True) | Q(flat=self.instance.personal_account.flat))
                self.fields['personal_account'].initial = self.instance.personal_account
            else:
                self.fields['personal_account'].queryset = PersonalAccount.objects.filter(
                    Q(flat__isnull=True))

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if instance.pk:
            if self.cleaned_data['personal_account_res'] == '':
                if hasattr(instance, 'personal_account'):
                    pa = instance.personal_account
                    pa.flat = None
                    pa.section = None
                    pa.house = None
                    pa.save()
                    instance.personal_account = None
                    instance.save()
            else:
                if hasattr(instance, 'personal_account'):
                    pa = instance.personal_account
                    pa.flat = None
                    pa.section = None
                    pa.house = None
                    pa.save()
                number = self.cleaned_data['personal_account_res']
                personal_account, created = PersonalAccount.objects.get_or_create(number=number)
                personal_account.flat = instance
                personal_account.section = instance.section
                personal_account.house = instance.house
                personal_account.save()
        return instance

    class Meta:
        model = Flat
        fields = '__all__'
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': ''}),
        }
