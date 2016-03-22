# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.forms import SchedulerCreateForm, SchedulerSearchForm, SchedulerUpdateForm
from core.models import Scheduler
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView


class SchedulerListView(ListView):
    model = Scheduler
    context_object_name = 'users'
    template_name = 'core/management/users.html'

    def get_queryset(self):
        qs = super(SchedulerListView, self).get_queryset()
        if self.request.GET.get('department'):
            qs = qs.filter(departments__in=[self.request.GET['department']])
        return qs

    def get_context_data(self, **kwargs):
        context = super(SchedulerListView, self).get_context_data(**kwargs)
        context['form'] = SchedulerSearchForm(self.request.GET or None)
        return context
scheduler_list_view = SchedulerListView.as_view()


class SchedulerCreateView(CreateView):
    model = User
    form_class = SchedulerCreateForm
    template_name = 'core/management/user_create.html'
    success_url = reverse_lazy('scheduler_list_view')

    def form_valid(self, form):
        redirect = super(SchedulerCreateView, self).form_valid(form)
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.save()
        for department in form.cleaned_data['departments']:
            form.instance.departments.add(department)
        return redirect
scheduler_create_view = SchedulerCreateView.as_view()


class SchedulerUpdateView(UpdateView):
    model = Scheduler
    form_class = SchedulerUpdateForm
    template_name = 'core/management/user_create.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('scheduler_list_view')

    def form_valid(self, form):
        redirect = super(SchedulerUpdateView, self).form_valid(form)
        form.instance.departments.clear()
        for department in form.cleaned_data['departments']:
            form.instance.departments.add(department)
        return redirect
scheduler_update_view = SchedulerUpdateView.as_view()
