import json
import os

from django import template
from admin_panel.models import *
import re

register = template.Library()


@register.filter
def disablingMeasure(value):
    return Service.objects.filter(measure_id=value).exists()

@register.filter
def disablingService(value):
    return Receipt.objects.filter(receiptservice__service_id=value).exists()



@register.filter
def intspace(value):
    orig = str(value)
    new = re.sub(r"^(-?\d+)(\d{3})", '\g<1> \g<2>', orig)
    if orig == new:
        return new
    else:
        return intspace(new)


@register.filter
def get_house_queryset(value):
    flats = FlatOwner.objects.get(id=value).flat_set.all().distinct('house')
    return flats

@register.filter
def get_flat_queryset(value):
    return FlatOwner.objects.get(id=value).flat_set.all()