# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.forms import UserExaminationReportForm
from core.models import UserExamination
from core.views.base import ListView


class UserExaminationReportListView(ListView):
    model = UserExamination
    context_object_name = 'user_examinations'
    template_name = 'core/report/user_examinations.html'
    title = 'Полный список аттестаций пользователей'

    def get_queryset(self):
        qs = super(UserExaminationReportListView, self).get_queryset()
        if self.request.GET.get('user'):
            qs = qs.filter(user=self.request.GET['user'])
        if self.request.GET.get('examination'):
            qs = qs.filter(user=self.request.GET['examination'])
        return qs

    def get_context_data(self, **kwargs):
        context = super(UserExaminationReportListView, self).get_context_data(**kwargs)
        context['form'] = UserExaminationReportForm(self.request.GET or None)
        return context
user_examination_report_list_view = UserExaminationReportListView.as_view()
