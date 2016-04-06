# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.forms import UserExaminationSearchForm, UserExaminationEditForm
from core.models import UserExamination, Examination
from core.views.base import CreateOrUpdateView, ListView
from django.core.urlresolvers import reverse_lazy


class UserExaminationListView(ListView):
    model = UserExamination
    context_object_name = 'user_examinations'
    template_name = 'core/management/user_examinations.html'
    title = 'Управление аттестациями пользователей'

    def get_queryset(self):
        qs = super(UserExaminationListView, self).get_queryset()
        if self.request.GET.get('user'):
            qs = qs.filter(user=self.request.GET['users'])
        if self.request.GET.get('examination'):
            qs = qs.filter(examination=self.request.GET['examination'])
        return qs

    def get_context_data(self, **kwargs):
        context = super(UserExaminationListView, self).get_context_data(**kwargs)
        context['form'] = UserExaminationSearchForm(self.request.GET or None)
        return context
user_examination_list_view = UserExaminationListView.as_view()


class UserExaminationCreateOrUpdateView(CreateOrUpdateView):
    model = UserExamination
    form_class_create = UserExaminationEditForm
    form_class_update = UserExaminationEditForm
    template_name = 'core/base/base_edit.html'
    pk_url_kwarg = 'user_examination_id'
    success_url = reverse_lazy('user_examination_list_view')

    def get_initial(self):
        initial = {}
        if self.is_create() and self.request.GET.get('examination'):
            initial['examination'] = Examination.objects.get(id=self.request.GET['examination'])
        return initial
user_examination_create_or_update_view = UserExaminationCreateOrUpdateView.as_view()
