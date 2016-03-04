# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import defaultdict
from core.forms import UserExaminationReportForm
from core.tables import UserExaminationTable
from django.contrib import messages

from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView

from core.models import *
from django_tables2 import RequestConfig


class UserExaminationListView(ListView):
    model = UserExamination
    template_name = 'core/examinations.html'
    context_object_name = 'user_examinations'

    def get_queryset(self):
        return self.model.get_for_user(self.request.user.id).filter(finished_at__isnull=True)

    def get_context_data(self, **kwargs):
        context = super(UserExaminationListView, self).get_context_data(**kwargs)
        context['user_examinations_finished'] = self.model.get_for_user(self.request.user).filter(finished_at__isnull=False)
        return context

user_examination_list_view = UserExaminationListView.as_view()


class UserExaminationQuestionDetailView(DetailView):
    model = UserExamination
    context_object_name = 'user_examination'
    pk_url_kwarg = 'user_examination_id'
    template_name = 'core/examination.html'
    question = None
    user_examination_question_log = None

    def dispatch(self, request, *args, **kwargs):

        user_examination = self.get_object()
        if user_examination.started_at is None:
            user_examination.started_at = datetime.datetime.now()
            user_examination.save()

        question_id = self.kwargs.get('question_id')

        if question_id:
            self.question = user_examination.examination.questions.get(id=question_id)
            self.user_examination_question_log, _ = UserExaminationQuestionLog.objects.get_or_create(
                user_examination=user_examination, question=self.question,
                defaults={'question_data': model_to_dict(self.question)}
            )

            if self.user_examination_question_log.user_examination_answer_logs.exists():
                raise Http404

            return super(UserExaminationQuestionDetailView, self).dispatch(request, *args, **kwargs)
        else:
            next_question_id = Question.get_next_id_in_examination(user_examination)

            if next_question_id is None:
                user_examination.finished_at = datetime.datetime.now()
                user_examination.calculate_points(commit=False)
                user_examination.save()
                messages.success(request, 'Тестирование %s завершено' % user_examination.examination.name)
                return redirect(reverse('user_examination_list_view'))
            else:
                return redirect(reverse(user_examination_question_detail_view, args=[user_examination.id, next_question_id]))

    def get_object(self, queryset=None):
        user_examination_qs = UserExamination.get_for_user(self.request.user).filter(finished_at__isnull=True)
        user_examination = super(UserExaminationQuestionDetailView, self).get_object(user_examination_qs)
        return user_examination

    def get_context_data(self, **kwargs):
        context = super(UserExaminationQuestionDetailView, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['answers'] = self.question.answers.all()
        context['input_type'] = 'radio' if self.question.answers.filter(is_right=True).count() == 1 else 'checkbox'
        context['remains_question_count'] = Question.get_remains_for_user_examination(self.object).count()
        return context
user_examination_question_detail_view = UserExaminationQuestionDetailView.as_view()


class UserExaminationDetailView(DetailView):
    model = UserExamination
    pk_url_kwarg = 'user_examination_id'
    context_object_name = 'user_examination'
    template_name = 'core/examination_detail.html'
    _question_log_qs = None
    _answer_log_qs = None

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:  # todo is_staff and department owner
            return super(UserExaminationDetailView, self).get_queryset()
        else:
            return UserExamination.get_for_user(self.request.user)

    def get_answer_log_qs(self):
        if self._answer_log_qs is None:
            self._answer_log_qs = UserExaminationAnswerLog.objects.filter(user_examination_question_log__in=self.get_question_log())
        return self._answer_log_qs

    def get_question_log(self):
        if self._question_log_qs is None:
            self._question_log_qs = UserExaminationQuestionLog.objects.filter(user_examination=self.object)
            for ql_qs in self._question_log_qs:
                ql_qs.question_data = json.loads(ql_qs.question_data)
        return self._question_log_qs

    def get_answer_log_for_question_log(self):
        answer_log_objects = defaultdict(list)
        answer_log_qs = self.get_answer_log_qs()
        for answer_log in answer_log_qs:
            answer_log.answer_data = json.loads(answer_log.answer_data)
            answer_log_objects[answer_log.user_examination_question_log_id].append(answer_log)
        return answer_log_objects

    def get_answers_stats(self):
        stats = {
            'right_answers_count': 0,
            'invalid_answers_count': 0
        }

        for answer_log in self.get_answer_log_qs():
            if answer_log.answer_data['is_right']:
                stats['right_answers_count'] += 1
            else:
                stats['invalid_answers_count'] += 1

        return stats

    def get_context_data(self, **kwargs):
        context = super(UserExaminationDetailView, self).get_context_data(**kwargs)
        context['question_log'] = self.get_question_log()
        context['answer_log'] = self.get_answer_log_for_question_log()
        context['user_examinations_stats'] = self.get_answers_stats()
        return context

user_examination_detail_view = UserExaminationDetailView.as_view()


def user_examination_answer_view(request, user_examination_id, question_id):
    answers_ids = [int(answer_id) for answer_id in request.POST.getlist('answer_id')]

    user_examination = UserExamination.get_for_user(request.user).get(finished_at__isnull=True, id=user_examination_id)
    user_examination_question = user_examination.examination.questions.get(id=question_id)

    user_examination_question_log = UserExaminationQuestionLog.objects.get(
        user_examination=user_examination, question=user_examination_question
    )

    if UserExaminationAnswerLog.objects.filter(user_examination_question_log=user_examination_question_log).exists():
        raise ValueError('Уже есть ответы на вопрос')

    if len(answers_ids) < 1:
        raise ValueError('Должен быть хотя бы один ответ')

    question_answers = user_examination_question.answers.all()
    question_answers_ids = [qa.id for qa in question_answers]
    question_right_answers_ids = [qa.id for qa in question_answers if qa.is_right is True]

    invalid_answers_ids = [answer_id for answer_id in answers_ids if answer_id not in question_answers_ids]
    if invalid_answers_ids:
        raise ValueError('Есть ответ, которого нет у вопроса')

    if len(answers_ids) > len(question_answers):
        raise ValueError('Вариантов ответа больше чем ответов')

    if len(question_right_answers_ids) == 1 and len(answers_ids) > 1:
        raise ValueError('Может быть только 1 правильный вариант, получено больше одного')

    for answer_id in answers_ids:
        answer = Answer.objects.get(id=answer_id)
        UserExaminationAnswerLog.objects.create(
            answer=answer, is_right=answer_id in question_right_answers_ids,
            user_examination_question_log=user_examination_question_log, answer_data=model_to_dict(answer)
        )

    user_examination_question_log.finished_at = datetime.datetime.now()
    user_examination_question_log.save()

    return redirect(reverse(user_examination_question_detail_view, args=[user_examination_id]))


class DepartmentsListView(ListView):
    model = Department
    template_name = 'core/departments.html'
    context_object_name = 'departments'

    def get_queryset(self):
        return self.request.user.departments_owner.all()
departments_list_view = DepartmentsListView.as_view()


class DepartmentUsersListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'core/department_users.html'

    def get_context_data(self, **kwargs):
        context = super(DepartmentUsersListView, self).get_context_data(**kwargs)
        context['department'] = self.request.user.departments_owner.get(id=self.kwargs['department_id'])
        return context

    def get_queryset(self):
        return self.model.objects.filter(departments__in=[self.kwargs['department_id']])

department_users_list_view = DepartmentUsersListView.as_view()


class DepartmentUserExaminationsListView(ListView):
    model = UserExamination
    context_object_name = 'user_examinations'
    template_name = 'core/department_user_examinations.html'
    _user = None
    _department = None

    def get_department(self):
        if not self._department:
            self._department = self.request.user.departments_owner.get(id=self.kwargs['department_id'])
        return self._department

    def get_user(self):
        if not self._user:
            department = self.get_department()
            self._user = department.employees.get(id=self.kwargs['user_id'])
        return self._user

    def get_context_data(self, **kwargs):
        context = super(DepartmentUserExaminationsListView, self).get_context_data(**kwargs)
        context['department'] = self.get_department()
        context['user'] = self.get_user()
        return context

    def get_queryset(self):
        return self.model.objects.filter(user=self.get_user())

department_user_examinations_list_view = DepartmentUserExaminationsListView.as_view()


class UserExaminationReportListView(ListView):
    model = UserExamination
    context_object_name = 'user_examinations'
    template_name = 'core/user_examination_report.html'

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
        table = UserExaminationTable(self.get_queryset())
        RequestConfig(self.request, paginate=False).configure(table)
        context['table'] = table
        return context
user_examination_report_list_view = UserExaminationReportListView.as_view()
