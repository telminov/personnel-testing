# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.forms import SchedulerCreateForm, SchedulerSearchForm
from core.models import Scheduler
from core.views.base import CreateOrUpdateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView


class SchedulerListView(ListView):
    model = Scheduler
    context_object_name = 'schedulers'
    template_name = 'core/management/schedulers.html'

    def get_queryset(self):
        qs = super(SchedulerListView, self).get_queryset()
        if self.request.GET.get('departments'):
            qs = qs.filter(departments__in=[self.request.GET['departments']])
        if self.request.GET.get('users'):
            qs = qs.filter(users__in=[self.request.GET['users']])
        if self.request.GET.get('examination'):
            qs = qs.filter(examination=self.request.GET['examination'])
        return qs

    def get_context_data(self, **kwargs):
        context = super(SchedulerListView, self).get_context_data(**kwargs)
        context['form'] = SchedulerSearchForm(self.request.GET or None)
        return context
scheduler_list_view = SchedulerListView.as_view()


class SchedulerCreateOrUpdateView(CreateOrUpdateView):
    model = Scheduler
    form_class_create = SchedulerCreateForm
    form_class_update = SchedulerCreateForm
    template_name = 'core/management/scheduler_edit.html'
    pk_url_kwarg = 'scheduler_id'
    success_url = reverse_lazy('scheduler_list_view')
scheduler_create_or_update_view = SchedulerCreateOrUpdateView.as_view()
