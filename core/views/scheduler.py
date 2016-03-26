# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from core.forms import SchedulerEditForm, SchedulerSearchForm
from core.models import Scheduler, UserExamination
from core.views.base import CreateOrUpdateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView


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
    form_class_create = SchedulerEditForm
    form_class_update = SchedulerEditForm
    template_name = 'core/base/base_edit.html'
    pk_url_kwarg = 'scheduler_id'
    success_url = reverse_lazy('scheduler_list_view')
scheduler_create_or_update_view = SchedulerCreateOrUpdateView.as_view()


class SchedulerDetailView(DetailView):
    model = Scheduler
    template_name = 'core/management/scheduler_detail.html'
    pk_url_kwarg = 'scheduler_id'
    context_object_name = 'scheduler'

    def get_context_data(self, **kwargs):
        context = super(SchedulerDetailView, self).get_context_data(**kwargs)
        scheduler = self.get_object()

        user_examinations = {}
        user_next_examinations = {}
        for user in scheduler.get_users():
            user_examinations_list = list(user.user_examinations.filter(scheduler=scheduler).order_by('-created_at'))
            if user_examinations_list:
                user_examinations[user.id] = user_examinations_list
                last_user_examination = user_examinations_list[0]
                user_next_examinations[user.id] = last_user_examination.get_next(scheduler)
        context['user_examinations'] = user_examinations
        context['user_next_examinations'] = user_next_examinations

        return context
scheduler_detail_view = SchedulerDetailView.as_view()
