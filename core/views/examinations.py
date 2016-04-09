# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import redirect

from core.forms import ExaminationEditForm, ExaminationSearchForm, QuestionEditForm, AnswerEditForm
from core.models import Examination, Question, Answer
from core.views.base import CreateOrUpdateView, ListView, ParentListView, ParentCreateOrUpdateView
from django.core.urlresolvers import reverse_lazy, reverse


class ExaminationListView(ListView):
    model = Examination
    context_object_name = 'examinations'
    template_name = 'core/management/examinations.html'
    title = 'Управление тестированиями'

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

    def get_title(self):
        if self.is_create():
            return 'Создание тестирования'
        else:
            return 'Редактирование тестирования «%s»' % self.get_object()

    def get_success_url(self):
        return reverse('examination_update_view', args=[self.get_object().id])
examination_create_or_update_view = ExaminationCreateOrUpdateView.as_view()


class ExaminationQuestionListView(ParentListView):
    model = Question
    pk_url_kwarg = 'question_id'

    parent_model = Examination
    parent_pk_url_kwarg = 'examination_id'

    context_object_name = 'questions'
    context_parent_object_name = 'examination'

    template_name = 'core/management/questions.html'

    def get_title(self):
        return 'Управление вопросами тестирования «%s»' % self.get_parent_object()
examination_question_list_view = ExaminationQuestionListView.as_view()


class ExaminationQuestionCreateOrUpdateView(ParentCreateOrUpdateView):
    model = Question
    pk_url_kwarg = 'question_id'

    parent_model = Examination
    parent_pk_url_kwarg = 'examination_id'
    parent_field_name = 'examination'
    context_parent_object_name = 'examination'

    template_name = 'core/management/question_edit.html'

    form_class_create = QuestionEditForm
    form_class_update = QuestionEditForm

    def get_title(self):
        if self.is_create():
            return 'Создание вопроса для тестирования «%s»' % self.get_parent_object()
        else:
            return 'Редактирование вопроса для тестирования «%s»' % self.get_parent_object()

    def get_success_url(self):
        return reverse_lazy(examination_question_create_or_update_view, args=[self.get_parent_object().id, self.get_object().id])

    def get_context_data(self, **kwargs):
        context = super(ExaminationQuestionCreateOrUpdateView, self).get_context_data(**kwargs)
        context['answers'] = self.get_object().answers.all()
        return context

examination_question_create_or_update_view = ExaminationQuestionCreateOrUpdateView.as_view()


def examination_question_delete_view(request, examination_id, question_id):
    examination = Examination.objects.get(id=examination_id)
    Question.objects.get(id=question_id, examination=examination).delete()
    messages.success(request, 'Вопрос успешно удален')
    return redirect(reverse(examination_question_list_view, args=[examination.id]))


class QuestionAnswerCreateOrUpdateView(ParentCreateOrUpdateView):
    model = Answer
    pk_url_kwarg = 'answer_id'

    parent_model = Question
    parent_pk_url_kwarg = 'question_id'
    parent_field_name = 'question'
    context_parent_object_name = 'question'

    template_name = 'core/management/answer_edit.html'

    form_class_create = AnswerEditForm
    form_class_update = AnswerEditForm

    def get_success_url(self):
        return reverse_lazy('examination_question_update_view', args=[
            self.get_parent_object().examination_id, self.get_parent_object().id
        ])

    def get_title(self):
        if self.is_create():
            return 'Создание ответа на вопрос «%s»' % self.get_parent_object()
        else:
            return 'Редактирование ответа на вопрос «%s»' % self.get_parent_object()

question_answer_create_or_update_view = QuestionAnswerCreateOrUpdateView.as_view()


def question_answer_delete_view(request, examination_id, question_id, answer_id):
    question = Question.objects.get(id=question_id, examination_id=examination_id)
    Answer.objects.get(question=question, id=answer_id).delete()
    messages.success(request, 'Ответ успешно удален')
    return redirect(reverse('examination_question_update_view', args=[examination_id, question_id]))
