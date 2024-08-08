from captcha import fields, widgets
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from admin_panel.models import Role


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    remember_me = forms.BooleanField(required=False)  # and add the remember_me field


class RoleForm(forms.ModelForm):
    statistics = forms.BooleanField(label=" ", required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none'}))
    paybox = forms.BooleanField(label=" ", required=False,
                                widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    receipt = forms.BooleanField(label=" ", required=False,
                                 widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    personal_account = forms.BooleanField(label=" ", required=False,
                                          widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    flat = forms.BooleanField(label=" ", required=False,
                              widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    flat_owner = forms.BooleanField(label=" ", required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    house = forms.BooleanField(label=" ", required=False,
                               widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    mailbox = forms.BooleanField(label=" ", required=False,
                                 widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    application = forms.BooleanField(label=" ", required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    indication = forms.BooleanField(label=" ", required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    manage_site = forms.BooleanField(label=" ", required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    service = forms.BooleanField(label=" ", required=False,
                                 widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    tariff = forms.BooleanField(label=" ", required=False,
                                widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    role = forms.BooleanField(label=" ", required=False,
                              widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    users = forms.BooleanField(label=" ", required=False,
                               widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    payment_detail = forms.BooleanField(label=" ", required=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))
    payment_article = forms.BooleanField(label=" ", required=False,
                                         widget=forms.CheckboxInput(attrs={'class': 'rounded-0 shadow-none '}))

    class Meta:
        model = Role
        exclude = ('name',)
        widgets = {

        }


RoleFormset = forms.modelformset_factory(model=Role, form=RoleForm, extra=0)
