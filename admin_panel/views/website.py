from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import *
from admin_panel.forms import *
from admin_panel.views import StaffRequiredMixin


class MainPageView(StaffRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        main_page = MainPage.objects.prefetch_related('gallery__photo_set', 'gallery__infophoto_set').first()
        seo_form = SeoForm(instance=Seo.objects.get(id=main_page.seo_id), prefix='seo')

        photo_formset = PhotoFormset(queryset=main_page.gallery.photo_set.all(), prefix="photo")
        info_photo_formset = InfoPhotoFormset(queryset=main_page.gallery.infophoto_set.all(), prefix="info_photo")
        main_form = MainPageForm(instance=main_page, prefix='main')
        data = {
            'main_form': main_form,
            'photo_formset': photo_formset,
            'info_photo_formset': info_photo_formset,
            'seo_form': seo_form,
        }
        return render(request, 'admin_panel/manage_site/main_page.html', context=data)

    def post(self, request, *args, **kwargs):
        main_form = MainPageForm(request.POST, request.FILES, instance=MainPage.objects.first(), prefix='main')
        seo = Seo.objects.get(id=MainPage.objects.first().seo_id)
        seo_form = SeoForm(request.POST, request.FILES, instance=seo, prefix='seo')
        photo_formset = PhotoFormset(request.POST, request.FILES, prefix="photo")
        info_photo_formset = InfoPhotoFormset(request.POST, request.FILES, prefix="info_photo")
        if main_form.is_valid() and photo_formset.is_valid() and info_photo_formset.is_valid() and seo_form.is_valid():
            main_form.save()
            seo_form.save()
            photo_formset.save()
            info_photo_formset.save()
        else:
            data = {
                'main_form': main_form,
                'photo_formset': photo_formset,
                'info_photo_formset': info_photo_formset,
                'seo_form': seo_form,

            }
            return render(request, 'admin_panel/manage_site/main_page.html', context=data)
        return redirect('main_page')


class AboutUsView(StaffRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        about_us = AboutUs.objects.prefetch_related('gallery__photo_set', 'extra_gallery__photo_set').first()
        seo_form = SeoForm(instance=Seo.objects.get(id=about_us.seo_id), prefix='seo')
        photo_formset = ExtraPhotoFormset(queryset=about_us.gallery.photo_set.all(), prefix="photo")
        extra_photo_formset = ExtraPhotoFormset(queryset=about_us.extra_gallery.photo_set.all(), prefix="extra_photo")
        about_us_form = AboutUsForm(instance=about_us, prefix='about')
        docs_formset = AboutUsDocumentFormset(prefix='docs')

        data = {
            "about_us_form": about_us_form,
            'photo_formset': photo_formset,
            'extra_photo_formset': extra_photo_formset,
            'docs_formset': docs_formset,
            'seo_form': seo_form,
        }
        return render(request, 'admin_panel/manage_site/about_us.html', context=data)

    def post(self, request, *args, **kwargs):
        about_us = AboutUs.objects.first()
        about_us_form = AboutUsForm(request.POST, request.FILES, instance=about_us, prefix='about')
        seo = Seo.objects.get(id=about_us.seo_id)
        docs_formset = AboutUsDocumentFormset(request.POST, request.FILES, prefix='docs')
        seo_form = SeoForm(request.POST, request.FILES, instance=seo, prefix='seo')
        photo_formset = ExtraPhotoFormset(request.POST, request.FILES, prefix="photo")
        extra_photo_formset = ExtraPhotoFormset(request.POST, request.FILES, prefix="extra_photo")
        if about_us_form.is_valid() and photo_formset.is_valid() and extra_photo_formset.is_valid() and seo_form.is_valid() and docs_formset.is_valid():
            about_us_form.save()
            seo_form.save()
            docs_formset.save()
            instances = photo_formset.save(commit=False)
            for instance in instances:
                instance.gallery_id = about_us.gallery.id
                instance.save()
            extra_instances = extra_photo_formset.save(commit=False)
            for instance in extra_instances:
                instance.gallery_id = about_us.extra_gallery.id
                instance.save()
        else:
            data = {
                'about_us_form': about_us_form,
                'photo_formset': photo_formset,
                'extra_photo_formset': extra_photo_formset,
                'seo_form': seo_form,
                'docs_formset': docs_formset,

            }
            return render(request, 'admin_panel/manage_site/about_us.html', context=data)
        return redirect('about_us')


class SiteServicesView(StaffRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        service_site = SeviceSite.objects.prefetch_related('gallery__infophoto_set').first()
        seo_form = SeoForm(instance=Seo.objects.get(id=service_site.seo_id), prefix='seo')
        info_photo_formset = InfoPhotoFormset(queryset=service_site.gallery.infophoto_set.all(), prefix="info_photo")
        data = {
            "info_photo_formset": info_photo_formset,
            "seo_form": seo_form
        }
        return render(request, 'admin_panel/manage_site/services.html', context=data)

    def post(self, request, *args, **kwargs):
        seo_form = SeoForm(request.POST, instance=Seo.objects.get(id=SeviceSite.objects.first().seo_id), prefix='seo')
        info_photo_formset = InfoPhotoFormset(request.POST, request.FILES, prefix="info_photo")
        service_site = SeviceSite.objects.first()

        if info_photo_formset.is_valid() and seo_form.is_valid():
            instances = info_photo_formset.save()

            for instance in instances:
                instance.gallery_id = service_site.gallery.id
                instance.save()
            seo_form.save()
        else:
            data = {
                "info_photo_formset": info_photo_formset,
                "seo_form": seo_form
            }
            return render(request, 'admin_panel/manage_site/services.html', context=data)
        return redirect('services')


class DeletePhotoView(StaffRequiredMixin, FormView):
    def get(self, request, pk, *args, **kwargs):
        obj = Photo.objects.get(id=pk)
        obj.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class DeleteDocView(StaffRequiredMixin, FormView):
    def get(self, request, pk, *args, **kwargs):
        obj = AboutUsDocument.objects.get(id=pk)
        obj.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class SiteTariffsView(StaffRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        tariff_site = TariffSite.objects.prefetch_related('gallery__infophoto_set').first()
        tariff_site_form = TariffSiteForm(instance=tariff_site)
        seo_form = SeoForm(instance=Seo.objects.get(id=tariff_site.seo_id), prefix='seo')
        info_photo_formset = InfoPhotoLiteFormset(queryset=tariff_site.gallery.infophoto_set.all(), prefix="info_photo")
        data = {
            "tariff_site_form": tariff_site_form,
            "info_photo_formset": info_photo_formset,
            "seo_form": seo_form
        }
        return render(request, 'admin_panel/manage_site/tariffs.html', context=data)

    def post(self, request, *args, **kwargs):
        seo_form = SeoForm(request.POST, instance=Seo.objects.get(id=TariffSite.objects.first().seo_id), prefix='seo')
        info_photo_formset = InfoPhotoLiteFormset(request.POST, request.FILES, prefix="info_photo")
        tariff_site = TariffSite.objects.first()
        tariff_site_form = TariffSiteForm(request.POST, instance=tariff_site)
        if info_photo_formset.is_valid() and seo_form.is_valid() and tariff_site_form.is_valid():
            tariff_site_form.save()
            instances = info_photo_formset.save()

            for instance in instances:
                instance.gallery_id = tariff_site.gallery.id
                instance.save()
            seo_form.save()
        else:
            data = {
                "tariff_site_form": tariff_site_form,
                "info_photo_formset": info_photo_formset,
                "seo_form": seo_form
            }
            return render(request, 'admin_panel/manage_site/tariffs.html', context=data)
        return redirect('tariffs')


class ContactsView(StaffRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        contacts = Contacts.objects.first()
        contacts_form = ContactForm(instance=contacts, prefix="contact")
        seo_form = SeoForm(instance=Seo.objects.get(id=contacts.seo_id), prefix='seo')

        data = {
            "contacts_form": contacts_form,
            "seo_form": seo_form,
        }
        return render(request, 'admin_panel/manage_site/contacts.html', context=data)

    def post(self, request, *args, **kwargs):
        contacts_form = ContactForm(request.POST, instance=Contacts.objects.first(), prefix="contact")
        seo_form = SeoForm(request.POST, instance=Seo.objects.get(id=Contacts.objects.first().seo_id), prefix='seo')
        if contacts_form.is_valid() and seo_form.is_valid():
            contacts_form.save()
            seo_form.save()
        else:
            data = {
                "contacts_form": contacts_form,
                "seo_form": seo_form,
            }
            return render(request, 'admin_panel/manage_site/contacts.html', context=data)
        return redirect('contacts')
