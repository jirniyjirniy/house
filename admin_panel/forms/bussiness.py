import django.forms as forms
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from ..models import *


class PersonalAccountForm(forms.ModelForm):
    number = forms.CharField(label='',
                             widget=forms.TextInput(attrs={'class': 'number', 'placeholder': ''}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label='Секция', required=False,
                                     widget=forms.Select(attrs={'class': 'form-section-select'}))
    house = forms.ModelChoiceField(queryset=House.objects.all(), label='Дом', required=False,
                                   widget=forms.Select(attrs={'class': 'form-house-select'}))
    flat = forms.ModelChoiceField(queryset=Flat.objects.all(), label='Квартира', required=False,
                                  widget=forms.Select(attrs={'class': 'form-flat-select'}))

    def __init__(self, *args, **kwargs):
        super(PersonalAccountForm, self).__init__(*args, **kwargs)
        self.fields['house'].empty_label = "Выберите..."
        self.fields['section'].empty_label = "Выберите..."
        self.fields['flat'].empty_label = "Выберите..."

    class Meta:
        model = PersonalAccount
        fields = '__all__'
        exclude = ('balance',)


class IndicationForm(forms.ModelForm):
    number = forms.CharField(label='',
                             widget=forms.TextInput(attrs={'class': 'number ignore', 'placeholder': ''}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label='Секция', required=False,
                                     widget=forms.Select(attrs={'class': 'form-section-select'}))
    house = forms.ModelChoiceField(queryset=House.objects.all(), label='Дом', required=False,
                                   widget=forms.Select(attrs={'class': 'form-house-select'}))
    service = forms.ModelChoiceField(queryset=Service.objects.filter(show_in_indication=True), label='Счётчик',
                                     widget=forms.Select(attrs={'class': 'form-service-select'}))
    flat = forms.ModelChoiceField(queryset=Flat.objects.all(), label='Квартира',
                                  widget=forms.Select(attrs={'class': 'form-flat-select'}))
    date_published = forms.DateField(label='',
                                     widget=forms.DateInput(attrs={'class': 'publishing-date ignore', 'placeholder': ''}))

    def __init__(self, *args, **kwargs):
        super(IndicationForm, self).__init__(*args, **kwargs)
        self.fields['house'].empty_label = "Выберите..."
        self.fields['section'].empty_label = "Выберите..."
        self.fields['flat'].empty_label = "Выберите..."
        self.fields['service'].empty_label = "Выберите..."
        self.fields['date_published'].initial = timezone.now().date()

    class Meta:
        model = Indication
        fields = '__all__'
        widgets = {
            'indication_val': forms.NumberInput(attrs={'placeholder': ''})
        }


class PersonalChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.application_label()


class FlatChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.application_label()


class ApplicationForm(forms.ModelForm):
    ROLE_CHOICE = (
        ('', 'Любой специалист'),
        ('director', 'Директор'),
        ('manager', 'Управляющий'),
        ('accountant', 'Бухгалтер'),
        ('electrician', 'Электрик'),
        ('plumber', 'Сантехник'),
    )
    date_published = forms.DateField(label='',
                                     widget=forms.DateInput(attrs={'class': 'publishing-date', 'placeholder': ''}))
    time_published = forms.TimeField(label='',
                                     widget=forms.TimeInput(attrs={'class': 'publishing-time', 'placeholder': ''}))
    flat_owner = forms.ModelChoiceField(queryset=FlatOwner.objects.all(), label='Владелец квартиры ', required=False,
                                        widget=forms.Select(attrs={'class': 'form-flat_owner-select select2'}))

    flat = FlatChoiceField(queryset=Flat.objects.filter(house__isnull=False), label='Квартира',
                           widget=forms.Select(attrs={'class': 'form-flat-select select2'}))

    user = PersonalChoiceField(queryset=Personal.objects.all(), label='Мастер', required=False,
                               widget=forms.Select(attrs={'class': 'form-master-select'}))

    user_type = forms.ChoiceField(choices=ROLE_CHOICE, label='Тип мастера', required=False, )
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '', 'rows': 8}), label='Описание')

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['status'].empty_label = "Выберите..."
        self.fields['flat'].empty_label = "Выберите..."
        self.fields['flat_owner'].empty_label = "Выберите..."
        self.fields['user'].empty_label = "Выберите..."

    class Meta:
        model = Application
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': '', 'rows': 8, 'class': 'summernote'})
        }


class CreateApplicationForm(ApplicationForm):
    def __init__(self, *args, **kwargs):
        ApplicationForm.__init__(self, *args, **kwargs)
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = "Выберите..."
        self.fields['date_published'].initial = timezone.now().date()
        self.fields['time_published'].initial = datetime.now().time()


class MailBoxForm(forms.ModelForm):
    to_debtors = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'to_debtors rounded-0 shadow-none'}),
                                    required=False,
                                    label='Владельцам с задолженностями')
    house = forms.ModelChoiceField(queryset=House.objects.all(), label='ЖК', required=False,
                                   widget=forms.Select(attrs={'class': 'form-house-select'}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label='Секция', required=False,
                                     widget=forms.Select(attrs={'class': 'form-section-select'}))
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), label='Этаж', required=False,
                                   widget=forms.Select(attrs={'class': 'form-floor-select'}))
    flat = forms.ModelChoiceField(queryset=Flat.objects.all(), label='Квартира', required=False,
                                  widget=forms.Select(attrs={'class': 'form-flat-select'}))

    def __init__(self, *args, **kwargs):
        super(MailBoxForm, self).__init__(*args, **kwargs)
        self.fields['house'].empty_label = "Всем..."
        self.fields['section'].empty_label = "Всем..."
        self.fields['floor'].empty_label = "Всем..."
        self.fields['flat'].empty_label = "Всем..."

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if instance.pk:
            flats = Flat.objects.filter(flat_owner__isnull=False)
            if self.cleaned_data['to_debtors']:
                flats = flats.filter(personal_account__balance__lt=0)
            q = []
            if self.cleaned_data['house']:
                q.append(Q(house=self.cleaned_data['house']))
                if self.cleaned_data['section']:
                    q.append(Q(section=self.cleaned_data['section']))
                if self.cleaned_data['floor']:
                    q.append(Q(floor=self.cleaned_data['floor']))
                if self.cleaned_data['flat']:
                    q.append(Q(id=self.cleaned_data['flat'].id))
                result = Q()
                for item in q:
                    result = result & item
                flats = flats.filter(result)
            for flat in flats:
                instance.flat_owners.add(flat.flat_owner)
        return instance

    class Meta:
        model = MailBox
        fields = ('title', 'description', 'house', 'section', 'floor', 'flat')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Тема сообщения'}),
            'description': forms.Textarea(attrs={'placeholder': 'Текст сообщения:'})
        }


class ReceiptForm(forms.ModelForm):
    date_published = forms.DateField(label='',
                                     widget=forms.DateInput(attrs={'class': 'publishing-date ignore', 'placeholder': ''}))
    start_date = forms.DateField(label='Период с',
                                 widget=forms.DateInput(attrs={'class': 'start-date ignore', 'placeholder': ''}))
    end_date = forms.DateField(label='Период по',
                               widget=forms.DateInput(attrs={'class': 'end-date ignore', 'placeholder': ''}))
    number = forms.CharField(label='',
                             widget=forms.TextInput(attrs={'class': 'number ignore', 'placeholder': ''}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label='Секция', required=False,
                                     widget=forms.Select(attrs={'class': 'form-section-select'}))
    house = forms.ModelChoiceField(queryset=House.objects.all(), label='Дом', required=False,
                                   widget=forms.Select(attrs={'class': 'form-house-select'}))
    flat = forms.ModelChoiceField(queryset=Flat.objects.all(), label='Квартира',
                                  widget=forms.Select(attrs={'class': 'form-flat-select'}))
    tariff = forms.ModelChoiceField(queryset=TariffSystem.objects.all(), label='Тариф',
                                    widget=forms.Select(attrs={'class': 'form-tariff-select'}))
    personal_account = forms.CharField(label='Лицевой счет', required=False,
                                       widget=forms.TextInput(attrs={'class': 'personal_account', 'placeholder': ''}))
    is_complete = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'shadow-none rounded-0'}),
                                     required=False,
                                     label='Проведена')
    total_price = forms.DecimalField(
        widget=forms.TextInput(attrs={'placeholder': '', 'class': 'total_price'}),
        required=False, label='')

    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        self.fields['house'].empty_label = "Выберите..."
        self.fields['section'].empty_label = "Выберите..."
        self.fields['flat'].empty_label = "Выберите..."
        self.fields['tariff'].empty_label = "Выберите..."
        self.fields['date_published'].initial = timezone.now().date()
        self.fields['start_date'].initial = timezone.now().date()
        self.fields['end_date'].initial = timezone.now().date()
        self.fields['total_price'].initial = 0
        self.fields['is_complete'].initial = True

    class Meta:
        model = Receipt
        fields = '__all__'
        exclude = ('service',)


class ReceiptExcelDocForm(forms.ModelForm):
    class Meta:
        model = ReceiptExcelDoc
        fields = '__all__'
        exclude = ('by_default',)
        widgets = {
            'file': forms.FileInput(attrs={'class': 'excel_file  d-block'}),
            'title': forms.TextInput(attrs={'placeholder': ''})
        }


class ReceiptServiceForm(forms.ModelForm):
    consumption = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'consumption'}),
                                      label='')
    unit_price = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'unit_price'}),
                                     label='')
    total_service_price = forms.DecimalField(
        widget=forms.TextInput(attrs={'placeholder': '', 'class': 'total_service_price'}),
        required=False, label='')
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='',
                                     widget=forms.Select(attrs={'class': 'form-service-select'}))
    measure = forms.ModelChoiceField(queryset=Measure.objects.all(), label='',
                                     widget=forms.Select(attrs={'class': 'form-measure-select'}))

    def __init__(self, *args, **kwargs):
        super(ReceiptServiceForm, self).__init__(*args, **kwargs)
        self.fields['service'].empty_label = "Выберите..."
        self.fields['measure'].empty_label = "Выберите..."

    class Meta:
        model = ReceiptService
        fields = '__all__'
        exclude = ('receipt',)


ReceiptServiceFormset = forms.modelformset_factory(model=ReceiptService, form=ReceiptServiceForm, can_delete=True,
                                                   extra=0)


class PayboxForm(forms.ModelForm):
    date_published = forms.DateField(label='',
                                     widget=forms.DateInput(attrs={'class': 'publishing-date ignore', 'placeholder': ''}))
    number = forms.CharField(label='',
                             widget=forms.TextInput(attrs={'class': 'number ignore', 'placeholder': ''}))
    personal_account = forms.ModelChoiceField(label='Лицевой счет', queryset=PersonalAccount.objects.all(),
                                              required=False,
                                              widget=forms.Select(
                                                  attrs={'class': 'personal_account-select select2',
                                                         'placeholder': ''}))
    flat_owner = forms.ModelChoiceField(label='Владелец квартиры', queryset=FlatOwner.objects.all(), required=False,
                                        widget=forms.Select(attrs={'class': 'form-flat_owner-select select2',
                                                                   'placeholder': ''}))
    user = PersonalChoiceField(label='Менеджер', required=False,
                               queryset=Personal.objects.filter(role__in=['director', 'accountant', 'manager']),
                               widget=forms.Select(attrs={'class': 'personal_account', 'placeholder': ''}))
    article = forms.ModelChoiceField(label='Статья', queryset=Article.objects.all(),
                                     widget=forms.Select(attrs={'class': 'personal_account', 'placeholder': ''}))
    is_complete = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'shadow-none rounded-0'}),
                                     required=False,
                                     label='Проведен')

    total = forms.DecimalField(label='Сумма', widget=forms.NumberInput(attrs={'placeholder': ''}))

    def __init__(self, *args, **kwargs):
        super(PayboxForm, self).__init__(*args, **kwargs)
        self.fields['article'].empty_label = 'Выберите...'
        self.fields['personal_account'].empty_label = 'Выберите...'
        self.fields['flat_owner'].empty_label = 'Выберите...'
        self.fields['user'].empty_label = 'Выберите...'

    class Meta:
        model = Paybox
        fields = '__all__'
        exclude = ('debit_credit',)
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': '', 'rows': 5, })
        }


class PersonalAccountsFilterForm(forms.Form):
    STATUS_CHOICE = (
        ('', ''),
        ('active', 'Активен'),
        ('not active', 'Не активен'),
    )
    DEBTS_CHOICE = (
        ('', ''),
        ('yes', 'Есть долг'),
        ('no', 'Нет долга'),

    )
    number = forms.CharField(label="", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    flat = forms.CharField(label="", max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    house = forms.ModelChoiceField(label="", required=False, queryset=House.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0 form-house-select'}))
    section = forms.ModelChoiceField(label="", required=False, queryset=Section.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control select2-simple-section select2-success rounded-0 form-section-select'}))
    flat_owner = forms.ModelChoiceField(label="", required=False, queryset=FlatOwner.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    have_debts = forms.ChoiceField(label="", required=False, choices=DEBTS_CHOICE, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))


class FlatsFilterForm(forms.Form):
    DEBTS_CHOICE = (
        ('', ''),
        ('yes', 'Есть долг'),
        ('no', 'Нет долга'),

    )
    number = forms.CharField(label="", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    house = forms.ModelChoiceField(label="", required=False, queryset=House.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0 form-house-select'}))
    section = forms.ModelChoiceField(label="", required=False, queryset=Section.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control select2-simple-section select2-success rounded-0 form-section-select'}))
    floor = forms.ModelChoiceField(label="", required=False, queryset=Floor.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control select2-simple-floor select2-success rounded-0 form-floor-select'}))
    flat_owner = forms.ModelChoiceField(label="", required=False, queryset=FlatOwner.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    have_debts = forms.ChoiceField(label="", required=False, choices=DEBTS_CHOICE, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))


class HouseFilterForm(forms.Form):
    title = forms.CharField(label="", max_length=100, required=False,
                            widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    address = forms.CharField(label="", max_length=100, required=False,
                              widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))


class ApplicationsFilterForm(forms.Form):
    ROLE_CHOICE = (
        ('', ''),
        ('any_master', 'Любой специалист'),
        ('director', 'Директор'),
        ('manager', 'Управляющий'),
        ('accountant', 'Бухгалтер'),
        ('electrician', 'Электрик'),
        ('plumber', 'Сантехник'),
        ('locksmith', 'Слесарь'),
    )
    STATUS_CHOICE = (
        ('', ''),
        ('new', 'Новое'),
        ('in work', 'В работе'),
        ('complete', 'Выполнено'),
    )
    number = forms.CharField(label="", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    daterange = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': '', 'class': 'daterange', 'value': ''}))
    master_type = forms.ChoiceField(label="", required=False, choices=ROLE_CHOICE, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    description = forms.CharField(label="", max_length=100, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    flat = forms.CharField(label="", max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control  rounded-0'}))
    flat_owner = forms.ModelChoiceField(label="", required=False, queryset=FlatOwner.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    phone = forms.CharField(label="", max_length=100, required=False,
                            widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    master = PersonalChoiceField(label="", required=False, queryset=Personal.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))


class PayboxFilterForm(forms.Form):
    PLUS_MINUS = (
        ('', ''),
        ('plus', 'Приход'),
        ('minus', 'Расход'),
    )
    STATUS_CHOICE = (
        ('', ''),
        ('complete', 'Проведен'),
        ('no complete', 'Не проведен'),
    )
    number = forms.CharField(label="", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    daterange = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': '', 'class': 'daterange', 'value': ''}))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    article = forms.ModelChoiceField(label='', queryset=Article.objects.all(), required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    flat_owner = forms.ModelChoiceField(label="", required=False, queryset=FlatOwner.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    personal_account = forms.CharField(label="", max_length=100, required=False,
                                       widget=forms.TextInput(
                                           attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    debit_credit = forms.ChoiceField(label="", choices=PLUS_MINUS, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))


class ReceiptFilterForm(forms.Form):
    COMPLETE = (
        ('', ''),
        ('complete', 'Проведена'),
        ('no complete', 'Не проведена'),
    )
    STATUS_CHOICE = (
        ('', ''),
        ('paid', 'Оплачена'),
        ('partially_paid', 'Частично оплачена'),
        ('unpaid', 'Не оплачена'),
    )
    number = forms.CharField(label="", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    daterange = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': '', 'class': 'daterange', 'value': ''}))
    month = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': '', 'class': 'month-picker', 'value': '', 'style': 'background:white'}))
    flat = forms.CharField(label="", max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    flat_owner = forms.ModelChoiceField(label="", required=False, queryset=FlatOwner.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2 select2-success rounded-0'}))
    complete = forms.ChoiceField(label="", choices=COMPLETE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))


class CountersFilterForm(forms.Form):
    house = forms.ModelChoiceField(label="", required=False, queryset=House.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0 form-house-select'}))
    section = forms.ModelChoiceField(label="", required=False, queryset=Section.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control select2-simple-section select2-success rounded-0 form-section-select'}))

    flat = forms.CharField(label="", max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    service = forms.ModelChoiceField(label="", required=False, queryset=Service.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control select2-simple select2-success rounded-0 form-service-select'}))


class CounterIndicationsFilterForm(forms.Form):
    STATUS_CHOICE = (
        ('', ''),
        ('new', 'Новое'),
        ('considered', 'Учтено'),
        ('considered and paid', 'Учтено и оплачено'),
        ('null', 'Нулевое'),
    )
    number = forms.CharField(label="", max_length=100, required=False,
                             widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    daterange = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'placeholder': '', 'class': 'daterange', 'value': ''}))
    house = forms.ModelChoiceField(label="", required=False, queryset=House.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0 form-house-select'}))
    section = forms.ModelChoiceField(label="", required=False, queryset=Section.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control select2-simple-section select2-success rounded-0 form-section-select'}))
    flat = forms.CharField(label="", max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    service = forms.ModelChoiceField(label="", required=False, queryset=Service.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control select2-simple-service select2-success rounded-0 form-service-select'}))


class SearchMessageFilterForm(forms.Form):
    search_row = forms.CharField(label="", max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0 '}))


class InvitationForm(forms.Form):
    phone = forms.CharField(max_length=19, label='Телефон',
                            validators=[
                                validators.MaxLengthValidator(19),
                                validators.MinLengthValidator(19),
                                validators.ProhibitNullCharactersValidator(),
                                validators.RegexValidator('^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$',
                                                          message='Неверно введён номер телефона.Пример ввода: +38 (098) 567-81-23')
                            ],
                            widget=forms.TextInput(attrs={'placeholder': '+38 (098) 567-81-23'})
                            )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'info@example.com'}), label='Email')
