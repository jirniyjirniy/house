import django.forms as forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.db import transaction

from House24 import settings
from ..models import *
from ..tasks import notification_password_changed

User = get_user_model()


class PersonalSignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Personal.ROLE_CHOICE, label='Роль')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': ''}), label='Email (логин)')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'password1'}),
                                label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'password2'}),
                                label='Повторить Пароль')
    phone = forms.CharField(max_length=19, label='Номер телефона',
                            validators=[
                                validators.MaxLengthValidator(19),
                                validators.MinLengthValidator(19),
                                validators.ProhibitNullCharactersValidator(),
                                validators.RegexValidator('^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$',
                                                          message='Неверно введён номер телефона.Пример ввода: +38 (098) 567-81-23')
                            ],
                            widget=forms.TextInput(attrs={'placeholder': ''})
                            )
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Имя')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Фамилия')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'status')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.is_staff = True
            user.save()
        Personal.objects.create(user=user, role=self.cleaned_data.get('role'))
        return user


class PersonalUpdateForm(UserChangeForm):
    role = forms.ChoiceField(choices=Personal.ROLE_CHOICE, label='Роль')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': ''}), label='Email (логин)')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'password1'}),
                                label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'password2'}),
                                label='Повторить Пароль')
    phone = forms.CharField(max_length=19, label='Номер телефона',
                            validators=[
                                validators.MaxLengthValidator(19),
                                validators.MinLengthValidator(19),
                                validators.ProhibitNullCharactersValidator(),
                                validators.RegexValidator('^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$',
                                                          message='Неверно введён номер телефона.Пример ввода: +38 (098) 567-81-23')
                            ],
                            widget=forms.TextInput(attrs={'placeholder': ''})
                            )
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Имя')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Фамилия')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'status')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        obj = Personal.objects.get(user=user)
        obj.role = self.cleaned_data.get('role')
        obj.save()
        if self.cleaned_data.get('password1') == self.cleaned_data.get('password2'):
            obj.user.set_password(self.cleaned_data.get('password1'))
            obj.user.save()
            notification_password_changed.delay(obj.user.email)
        return user


class ClientSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': ''}), label='Email (логин)')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'password1'}),
                                label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'password2'}),
                                label='Повторить Пароль')
    ID = forms.CharField(max_length=11, label='ID', widget=forms.TextInput(attrs={'placeholder': ''}))

    phone = forms.CharField(max_length=19, label='Номер телефона', required=False,
                            validators=[
                                validators.MaxLengthValidator(19),
                                validators.MinLengthValidator(19),
                                validators.ProhibitNullCharactersValidator(),
                                validators.RegexValidator('^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$',
                                                          message='Неверно введён номер телефона.Пример ввода: +38 (098) 567-81-23')
                            ],
                            widget=forms.TextInput(attrs={'placeholder': ''})
                            )
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Имя')
    patronymic = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Отчество')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Фамилия')
    viber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Viber', required=False, )
    telegram = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Telegram', required=False)

    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': ''}), label='О владельце (заметки)',
                          required=False)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'placeholder': '', 'class': 'birthday'}),
                               label='Дата рождения', required=False)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'avatar d-block'}), label='Сменить изображение',
                              required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('avatar', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'status')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
        FlatOwner.objects.create(user=user, ID=self.cleaned_data.get('ID'),
                                 patronymic=self.cleaned_data.get('patronymic'),
                                 birthday=self.cleaned_data.get('birthday'),
                                 bio=self.cleaned_data.get('bio'), viber=self.cleaned_data.get('viber'),
                                 telegram=self.cleaned_data.get('telegram'))
        return user


class ClientUpdateForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '', 'class': 'rounded-0'}),
                             label='Email (логин)')
    ID = forms.CharField(max_length=11, label='ID',
                         widget=forms.TextInput(attrs={'placeholder': '', 'class': 'rounded-0'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'password1 rounded-0'}),
                                label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'password2 rounded-0'}),
                                label='Повторить Пароль')
    phone = forms.CharField(max_length=19, label='Номер телефона', required=False,
                            validators=[
                                validators.MaxLengthValidator(19),
                                validators.MinLengthValidator(19),
                                validators.ProhibitNullCharactersValidator(),
                                validators.RegexValidator('^\+38 \(\d{3}\) \d{3}-?\d{2}-?\d{2}$',
                                                          message='Неверно введён номер телефона.Пример ввода: +38 (098) 567-81-23')
                            ],
                            widget=forms.TextInput(attrs={'placeholder': '', 'class': 'rounded-0'})
                            )
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'rounded-0'}), label='Имя')
    patronymic = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'rounded-0'}),
                                 label='Отчество')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'rounded-0'}),
                                label='Фамилия')
    viber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'rounded-0'}), label='Viber',
                            required=False, )
    telegram = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'class': 'rounded-0'}),
                               label='Telegram', required=False, )
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'avatar d-block rounded-0'}),
                              label='Сменить изображение',
                              required=False, )

    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '', 'class': 'rounded-0'}),
                          label='О владельце (заметки)',
                          required=False, )
    birthday = forms.DateField(widget=forms.DateInput(attrs={'placeholder': '', 'class': 'birthday rounded-0'}),
                               label='Дата рождения', required=False, )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('avatar', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'status')
        widgets = {
            'status': forms.Select(attrs={'class': 'rounded-0 shadow-none'})
        }

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        obj = FlatOwner.objects.get(user=user)
        obj.birthday = self.cleaned_data.get('birthday')
        obj.patronymic = self.cleaned_data.get('patronymic')
        obj.bio = self.cleaned_data.get('bio')
        obj.viber = self.cleaned_data.get('viber')
        obj.telegram = self.cleaned_data.get('telegram')
        obj.ID = self.cleaned_data.get('ID')
        obj.save()
        if self.cleaned_data.get('password1') == self.cleaned_data.get('password2'):
            obj.user.set_password(self.cleaned_data.get('password1'))
            obj.user.save()
            notification_password_changed.delay(obj.user.email)

        return user


class ClientsFilterForm(forms.Form):
    STATUS_CHOICE = (
        ('', ''),
        ('new', 'Новый'),
        ('active', 'Активен'),
        ('disabled', 'Отключен'),
    )
    DEBTS_CHOICE = (
        ('', ''),
        ('yes', 'Да'),
        ('no', 'Нет'),

    )
    ID = forms.CharField(label="", max_length=100, required=False,
                         widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    full_name = forms.CharField(label="", max_length=100, required=False,
                                widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    phone = forms.CharField(label="", max_length=11, required=False,
                            widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    email = forms.CharField(label="", max_length=100, required=False,
                            widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    house = forms.ModelChoiceField(label="", required=False, queryset=House.objects.all(), widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    flat = forms.CharField(label="", max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    date_added = forms.CharField(label="", max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': '', 'class': 'singledatepicker', }))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    have_debts = forms.ChoiceField(label="", required=False, choices=DEBTS_CHOICE, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))


class PersonalFilterForm(forms.Form):
    ROLE_CHOICE = (
        ('', ''),
        ('director', 'Директор'),
        ('manager', 'Управляющий'),
        ('accountant', 'Бухгалтер'),
        ('electrician', 'Электрик'),
        ('plumber', 'Сантехник'),
        ('locksmith', 'Слесарь'),
    )
    STATUS_CHOICE = (
        ('', ''),
        ('new', 'Новый'),
        ('active', 'Активен'),
        ('disabled', 'Отключен'),
    )
    user = forms.CharField(label="", max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    role = forms.ChoiceField(label="", required=False, choices=ROLE_CHOICE, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
    email = forms.CharField(label="", max_length=100, required=False,
                            widget=forms.EmailInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    phone = forms.CharField(label="", max_length=100, required=False,
                            widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control rounded-0'}))
    status = forms.ChoiceField(label="", choices=STATUS_CHOICE, required=False, widget=forms.Select(
        attrs={'placeholder': '', 'class': 'form-control select2-simple select2-success rounded-0'}))
