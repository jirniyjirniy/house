from django.shortcuts import render
from django.views.generic import TemplateView
from admin_panel.models import *


class Main(TemplateView):
    template_name = "website/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main = MainPage.objects.prefetch_related('gallery__photo_set', 'gallery__infophoto_set').first()
        seo = Seo.objects.get(pk=main.seo_id)
        contacts = Contacts.objects.first()
        context["main"] = main
        context["photos"] = main.gallery.photo_set.all()
        context["contacts"] = contacts
        context["info_photos"] = main.gallery.infophoto_set.all()
        context["seo"] = seo
        return context


class AboutUsSite(TemplateView):
    template_name = "website/about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_us = AboutUs.objects.prefetch_related('gallery__photo_set', 'extra_gallery__photo_set','aboutusdocument_set').first()
        context["about_us"] = about_us
        context["photos"] = about_us.gallery.photo_set.all()
        context["extra_photos"] = about_us.extra_gallery.photo_set.all()
        context["docs"] = about_us.aboutusdocument_set.all()
        return context


class ContactsSite(TemplateView):
    template_name = "website/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts"] = Contacts.objects.first()
        return context


class Services(TemplateView):
    template_name = "website/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = SeviceSite.objects.prefetch_related('gallery__infophoto_set').first()
        context["services"] = services.gallery.infophoto_set.all()
        return context
