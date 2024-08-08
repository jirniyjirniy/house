import json
import urllib
from urllib.request import urlopen

from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.contrib.auth.views import *
from django.urls import reverse_lazy
from django.views import View

from admin_panel.models import Personal
# Create your views here.
from users.forms import *

# class LoginHouse24(LoginView):
#     authentication_form = LoginForm
#     template_name = 'registration/login.html'
#
#     def form_valid(self, form):
#         user = authenticate(
#             username=form.cleaned_data['username'],
#             password=form.cleaned_data['password'],
#         )
#         if user is not None:
#             login(self.request, user)
#             # if not form.cleaned_data['remember_me']:
#             #     self.request.session.set_expiry(0)
#             if user.is_staff:
#                 return redirect('statistic')
#             else:
#                 return redirect('profile')


from django.views.generic import View


class LoginHouse24(View):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(data=request.POST)
        # recaptcha_response = request.POST.get('g-recaptcha-response')
        # url = 'https://www.google.com/recaptcha/api/siteverify'
        # values = {
        #     'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        #     'response': recaptcha_response
        # }
        # data = urllib.parse.urlencode(values).encode()
        # req = urllib.request.Request(url, data=data)
        # response = urllib.request.urlopen(req)
        # result = json.loads(response.read().decode())
        # ''' End reCAPTCHA validation '''
        # if result['success']:
        if form.is_valid():

            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                if not form.cleaned_data['remember_me']:
                    self.request.session.set_expiry(0)
                if user.is_staff:
                    user_permission = Role.objects.get(name=user.personal.role)
                    if user_permission.statistics:
                        return redirect('statistic')
                    else:
                        url = f"/admin/personals/update/{self.request.user.id}"
                        return HttpResponseRedirect(url)

                else:
                    return redirect('profile')
        messages.error(request, 'Неправильно указана почта или пароль')
        return render(request, self.template_name, context={'form': form})
        # messages.error(request, 'ReCaptcha не пройдена')
        # return render(request, self.template_name, context={'form': form})

