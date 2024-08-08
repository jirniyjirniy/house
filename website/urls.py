from django.urls import path
from .views import *

urlpatterns = [
    path('main/', Main.as_view(), name='main'),
    path('about_us/', AboutUsSite.as_view(), name='about_us_site'),
    path('contacts/', ContactsSite.as_view(), name='contacts_site'),
    path('services/', Services.as_view(), name='site_services'),
]
