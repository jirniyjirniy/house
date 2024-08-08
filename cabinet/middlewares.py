import sys
from datetime import datetime, timedelta

from django.urls import resolve
from django.utils import timezone

from admin_panel.models import *


def user_info(request):
    app_name = sys.modules[resolve(request.path_info).func.__module__].__package__
    data = {}
    if app_name == 'cabinet':
        data = {
            'flats': Flat.objects.filter(flat_owner_id=request.user.client.id),
            'notifications': MailBox.objects.filter(flat_owners__user_id=request.user.id, unread=True),
        }
    elif app_name == 'admin_panel.views':
        target_date = datetime.today() - timedelta(days=3)
        user = Personal.objects.get(user_id=request.user.id)
        user_permission = Role.objects.get(name=user.role)
        data = {
            'new_clients': FlatOwner.objects.filter(user__date_joined__gt=target_date),
            'user_permission': user_permission,
        }
    elif app_name == 'website':
        pass
    elif app_name == 'registration':
        pass
    return data
