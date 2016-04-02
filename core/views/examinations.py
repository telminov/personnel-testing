# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.forms import ExaminationEditForm, ExaminationSearchForm
from core.models import Examination, Question
from core.views.base import CreateOrUpdateView, ListView
from django.core.urlresolvers import reverse_lazy


class ExaminationListView(ListView):
    model = Examination
    context_object_name = 'examinations'
    template_name = 'core/management/examinations.html'
    title = 'Управление аттестациями'

    def get_queryset(self):
        qs = super(ExaminationListView, self).get_queryset()
        if self.request.GET.get('departments'):
            qs = qs.filter(departments__in=[self.request.GET['departments']])
        if self.request.GET.get('users'):
            qs = qs.filter(users__in=[self.request.GET['users']])
        if self.request.GET.get('examination'):
            qs = qs.filter(examination=self.request.GET['examination'])
        return qs

    def get_context_data(self, **kwargs):
        context = super(ExaminationListView, self).get_context_data(**kwargs)
        context['form'] = ExaminationSearchForm(self.request.GET or None)
        return context
examination_list_view = ExaminationListView.as_view()


class ExaminationCreateOrUpdateView(CreateOrUpdateView):
    model = Examination
    form_class_create = ExaminationEditForm
    form_class_update = ExaminationEditForm
    template_name = 'core/management/examination_edit.html'
    pk_url_kwarg = 'examination_id'
    success_url = reverse_lazy('examination_list_view')

    def get_title(self):
        if self.is_create():
            return 'Создание тестирования'
        else:
            return 'Редактирование тестирования %s' % self.get_object()
examination_create_or_update_view = ExaminationCreateOrUpdateView.as_view()


class ExaminationQuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'core/management/questions.html'
    title = 'Управление вопросами'



class ExaminationQuestionCreateOrUpdateView(CreateOrUpdateView):
    pass
