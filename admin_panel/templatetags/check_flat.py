import json
import os

from django import template
from admin_panel.models import *
import re

register = template.Library()


@register.filter
def accept_flat_payment(value):
    result = True
    flat = Flat.objects.get(pk=value)

    if hasattr(flat, 'personal_account'):
        if flat.personal_account == '' or flat.personal_account is None:
            result = False
    else:
        result = False
    return result
