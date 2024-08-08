# app.backends.py
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password, check_password, identify_hasher, get_hasher
from django.db.models import Q


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
