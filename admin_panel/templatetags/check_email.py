import json
import os

from django import template
from admin_panel.models import *
import re

register = template.Library()


@register.filter
def accept_email(value):
    result = True
    receipt = Receipt.objects.get(pk=value)
    if receipt.flat.flat_owner is None:
        result = False
    return result