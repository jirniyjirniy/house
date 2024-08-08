import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import *
from admin_panel.forms import *
from admin_panel.views import StaffRequiredMixin
from users.forms import RoleFormset


class ServicesView(StaffRequiredMixin, FormView):

    def get(self, request, *args, **kwargs):
        service_formset = ServiceFormset(prefix='service_formset')
        measure_formset = MeasureFormset(prefix='measure_formset')
        data = {
            'service_formset': service_formset,
            'measure_formset': measure_formset,
        }
        return render(request, 'admin_panel/system_settings/services.html', context=data)

    def post(self, request, *args, **kwargs):
        service_formset = ServiceFormset(request.POST, prefix='service_formset')
        measure_formset = MeasureFormset(request.POST, prefix='measure_formset')
        if measure_formset.is_valid():
            instances = measure_formset.save(commit=False)

            for obj in measure_formset.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.save()

        if service_formset.is_valid():
            instances = service_formset.save(commit=False)
            for obj in service_formset.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.save()
        else:
            data = {
                'service_formset': service_formset,
                'measure_formset': measure_formset,
            }
            return render(request, 'admin_panel/system_settings/services.html', context=data)
        return redirect('system_services')


class TariffsListView(StaffRequiredMixin, ListView):
    template_name = 'admin_panel/system_settings/tariffs.html'
    model = TariffSystem


class TariffDetail(StaffRequiredMixin, DetailView):
    model = TariffSystem
    template_name = 'admin_panel/system_settings/read_tariff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tariff = TariffSystem.objects.get(pk=self.kwargs['pk'])

        context['tariff'] = tariff
        context['tariffservices'] = tariff.tariffservice_set.all()
        return context


class DeleteTariffView(StaffRequiredMixin, DeleteView):
    success_url = reverse_lazy('system_tariffs')
    queryset = TariffSystem.objects.all()

    def post(self, request, pk, *args, **kwargs):
        TariffService.objects.filter(tariff_id=pk).delete()
        return super().post(request, *args, **kwargs)


class UpdateTariffView(StaffRequiredMixin, FormView):
    def get(self, request, pk, *args, **kwargs):
        tariff = TariffSystem.objects.get(pk=pk)
        tariff_form = TariffForm(instance=tariff)
        tariff_service_formset = TariffServiceFormset(queryset=TariffService.objects.filter(tariff_id=pk),
                                                      prefix='tariff_service')
        service_formset = ServiceFormset(prefix='service')
        data = {
            'tariff_form': tariff_form,
            'tariff_service_formset': tariff_service_formset,
            'service_formset': service_formset,
        }
        return render(request, 'admin_panel/system_settings/update_tariff.html', context=data)

    def post(self, request, pk, *args, **kwargs):
        tariff_form = TariffForm(request.POST, instance=TariffSystem.objects.get(pk=pk))
        tariff_service_formset = TariffServiceFormset(request.POST, prefix='tariff_service')
        service_formset = ServiceFormset(prefix='service')
        if tariff_form.is_valid() and tariff_service_formset.is_valid():
            tariff = tariff_form.save()
            instances = tariff_service_formset.save(commit=False)
            for obj in tariff_service_formset.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.tariff_id = tariff.id
                instance.save()
        else:

            data = {
                'tariff_form': tariff_form,
                'tariff_service_formset': tariff_service_formset,
                'service_formset': service_formset,
            }
            return render(request, 'admin_panel/system_settings/get_tariff_form.html', context=data)
        return redirect('system_tariffs')


class GetMeasureView(StaffRequiredMixin, View):
    def get(self, request, pk):
        service = Service.objects.get(pk=pk)

        data = {
            'measure': service.measure.title,
        }

        return HttpResponse(json.dumps(data), content_type='application/json')


class CopyTariffView(StaffRequiredMixin, FormView):
    def get(self, request, pk, *args, **kwargs):
        copy = TariffSystem.objects.get(pk=pk)
        tariff_form = TariffForm(instance=copy)

        tariff_service_formset = TariffServiceFormset(queryset=TariffService.objects.filter(tariff_id=pk),
                                                      prefix='tariff_service')
        service_formset = ServiceFormset(prefix='service')
        data = {
            'tariff_form': tariff_form,
            'tariff_service_formset': tariff_service_formset,
            'service_formset': service_formset,
        }
        return render(request, 'admin_panel/system_settings/copy_tariff.html', context=data)

    def post(self, request, *args, **kwargs):
        tariff_form = TariffForm(request.POST)
        tariff_service_formset = TariffServiceFormset(request.POST, prefix='tariff_service')
        service_formset = ServiceFormset(prefix='service')
        if tariff_form.is_valid() and tariff_service_formset.is_valid():
            obj = tariff_form.save()
            instances = tariff_service_formset.save(commit=False)

            for instance in instances:
                instance.pk = None
                instance.tariff_id = obj.id
                instance.save()
        else:

            data = {
                'tariff_form': tariff_form,
                'tariff_service_formset': tariff_service_formset,
                'service_formset': service_formset,
            }
            return render(request, 'admin_panel/system_settings/get_tariff_form.html', context=data)
        return redirect('system_tariffs')


class CreateTariffView(StaffRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        tariff_form = TariffForm()
        tariff_service_formset = TariffServiceFormset(queryset=TariffService.objects.none(), prefix='tariff_service')
        service_formset = ServiceFormset(prefix='service')
        data = {
            'tariff_form': tariff_form,
            'tariff_service_formset': tariff_service_formset,
            'service_formset': service_formset,
        }
        return render(request, 'admin_panel/system_settings/get_tariff_form.html', context=data)

    def post(self, request, *args, **kwargs):
        tariff_form = TariffForm(request.POST)
        tariff_service_formset = TariffServiceFormset(request.POST, prefix='tariff_service')
        service_formset = ServiceFormset(prefix='service')
        if tariff_form.is_valid() and tariff_service_formset.is_valid():
            obj = tariff_form.save()
            instances = tariff_service_formset.save(commit=False)
            for obj in tariff_service_formset.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.tariff_id = obj.id
                instance.save()
        else:

            data = {
                'tariff_form': tariff_form,
                'tariff_service_formset': tariff_service_formset,
                'service_formset': service_formset,
            }
            return render(request, 'admin_panel/system_settings/get_tariff_form.html', context=data)
        return redirect('system_tariffs')


class PersonalListView(StaffRequiredMixin, ListView):
    template_name = 'admin_panel/system_settings/personals.html'
    context_object_name = 'personals'
    queryset = Personal.objects.all()
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PersonalFilterForm()
        return context


class PersonalFilteredList(StaffRequiredMixin, ListView):
    template_name = 'admin_panel/system_settings/personals.html'
    context_object_name = 'personals'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PersonalFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        personals = Personal.objects.all()
        form_filter = PersonalFilterForm(self.request.GET)
        qs = []
        if form_filter.is_valid():
            if form_filter.cleaned_data['user']:
                result = form_filter.cleaned_data['user'].split(' ')
                qs.append(Q(Q(user__last_name__in=result) | Q(user__first_name__in=result)))

            if form_filter.cleaned_data['phone']:
                qs.append(Q(user__phone__icontains=form_filter.cleaned_data['phone']))
            if form_filter.cleaned_data['email']:
                qs.append(Q(user__phone__icontains=form_filter.cleaned_data['phone']))
            if form_filter.cleaned_data['role']:
                qs.append(Q(role=form_filter.cleaned_data['role']))
            if form_filter.cleaned_data['status']:
                qs.append(Q(user__status=form_filter.cleaned_data['status']))
            q = Q()
            for item in qs:
                q = q & item
            personals = Personal.objects.filter(q)
        return personals


class PersonalDetail(StaffRequiredMixin, DetailView):
    model = Personal
    template_name = 'admin_panel/system_settings/read_personal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal'] = Personal.objects.get(pk=self.kwargs['pk'])
        return context


class PersonalSignUpView(StaffRequiredMixin, CreateView):
    model = CustomUser
    form_class = PersonalSignUpForm
    template_name = 'admin_panel/system_settings/get_personal_form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('personals')


class UpdatePersonalView(StaffRequiredMixin, UpdateView):
    model = CustomUser
    form_class = PersonalUpdateForm
    template_name = 'admin_panel/system_settings/update_personal.html'
    success_url = reverse_lazy('personals')
    queryset = CustomUser.objects.all()

    def get(self, request, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        form = PersonalUpdateForm(instance=user, initial={'role': Personal.objects.get(user=user).role})
        data = {
            'form': form,
        }
        return render(request, 'admin_panel/system_settings/update_personal.html', context=data)


class UpdatePaymentDetailView(StaffRequiredMixin, UpdateView):
    template_name = 'admin_panel/system_settings/payment_details.html'
    form_class = PaymentDetailForm
    success_url = reverse_lazy('system_payment_details')

    def get_object(self, queryset=None):
        return PaymentDetail.objects.first()


class DeletePersonalView(StaffRequiredMixin, DeleteView):
    success_url = reverse_lazy('personals')
    queryset = CustomUser.objects.all()


class CreatePaymentArticleView(StaffRequiredMixin, CreateView):
    template_name = 'admin_panel/system_settings/get_payment_article_form.html'
    form_class = PaymentArticleForm
    success_url = reverse_lazy('system_payment_articles')


class UpdatePaymentArticleView(StaffRequiredMixin, UpdateView):
    template_name = 'admin_panel/system_settings/update_payment_article.html'
    form_class = PaymentArticleForm
    success_url = reverse_lazy('system_payment_articles')
    queryset = Article.objects.all()


class DeletePaymentArticleView(StaffRequiredMixin, DeleteView):
    success_url = reverse_lazy('system_payment_articles')
    queryset = Article.objects.all()


class PaymentArticlesListView(StaffRequiredMixin, ListView):
    template_name = 'admin_panel/system_settings/payment_articles.html'
    context_object_name = 'rows'
    queryset = Article.objects.all()


class Roles(StaffRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        roles_formset = RoleFormset(prefix='roles')
        data = {
            'roles_formset': roles_formset,

        }
        return render(request, 'admin_panel/system_settings/roles.html', context=data)

    def post(self, request, *args, **kwargs):
        roles_formset = RoleFormset(request.POST, prefix='roles')

        if roles_formset.is_valid():
            roles_formset.save()
        else:
            data = {
                'roles_formset': roles_formset,
            }
            return render(request, 'admin_panel/system_settings/roles.html', context=data)
        return redirect('roles')


