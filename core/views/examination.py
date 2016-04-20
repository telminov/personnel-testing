# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from collections import defaultdict
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from core.views.base import ListView, DetailView, TemplateView

from core.models import (
    UserExamination, UserExaminationQuestionLog, UserExaminationAnswerLog, Department, User, Question, Answer
)
from random import random, shuffle


def user_examination_list_view(request):
    context = {
        'user_examinations': UserExamination.get_for_user(request.user.id).filter(finished_at__isnull=True),
        'user_examinations_finished': UserExamination.get_for_user(request.user).filter(finished_at__isnull=False),
        'title': 'Список персональных аттестаций'
    }

    return render(request, 'core/examinations.html', context)


class UserExaminationProcessView(TemplateView):
    _user_examination = None
    _user_examination_question_log = None
    template_name = 'core/examination.html'

    def get_right_answers_count(self):
        user_examination_question_log = self.get_user_examination_question_log()
        question_answers = json.loads(user_examination_question_log.question_answers_data)

        question_right_answers_ids = [qa['id'] for qa in question_answers if qa['is_right'] is True]
        return len(question_right_answers_ids)

    def get_user_examination(self):
        if not self._user_examination:
            self._user_examination = UserExamination.get_for_user(
                self.request.user, id=self.kwargs['user_examination_id'], finished_at__isnull=True
            ).get()
        return self._user_examination

    def get_user_examination_question_log(self):
        if not self._user_examination_question_log:
            user_examination_question_log_id = self.kwargs.get('user_examination_question_log_id')
            if not user_examination_question_log_id:
                raise AttributeError('user_examination_question_log_id kwarg not found')
            self._user_examination_question_log = self.get_user_examination().logs.get(id=user_examination_question_log_id)
        return self._user_examination_question_log

    def dispatch(self, request, *args, **kwargs):
        user_examination_question_log_id = kwargs.get('user_examination_question_log_id')

        user_examination = self.get_user_examination()

        if user_examination.started_at is None:
            user_examination.start()

        if user_examination_question_log_id is None:
            next_log_id = UserExaminationQuestionLog.get_next_id(user_examination=user_examination)

            if next_log_id is None:
                user_examination.finish()
                messages.success(request, 'Тестирование %s завершено.' % user_examination.examination.name)
                redirect_to = redirect(reverse('user_examination_list_view'))
            else:
                redirect_to = redirect(reverse(user_examination_process_view, args=[user_examination.id, next_log_id]))

            return redirect_to

        if datetime.datetime.now() > user_examination.must_finished_at:
            user_examination.finish()
            messages.success(request, 'Тестирование %s завершено. Закончилось время.' % user_examination.examination.name)
            return redirect(reverse('user_examination_list_view'))

        user_examination_question_log = self.get_user_examination_question_log()
        if user_examination_question_log.user_examination_answer_logs.exists():
            return redirect(reverse(user_examination_process_view, args=[user_examination.id]))

        if user_examination_question_log.started_at is None:
            user_examination_question_log.started_at = datetime.datetime.now()
            user_examination_question_log.save()

        return super(UserExaminationProcessView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_examination_question_log = self.get_user_examination_question_log()
        redirect_to = reverse(user_examination_process_view, args=[self.get_user_examination().id])

        if request.POST.get('skip'):
            user_examination_question_log.skipped_at = datetime.datetime.now()
            user_examination_question_log.save()
            return redirect(redirect_to)

        answers_ids = [int(answer_id) for answer_id in request.POST.getlist('answer_id')]

        if len(answers_ids) < 1:
            return redirect(redirect_to)

        question_answers = json.loads(user_examination_question_log.question_answers_data)

        question_answers_ids = [qa['id'] for qa in question_answers]
        question_right_answers_ids = [qa['id'] for qa in question_answers if qa['is_right'] is True]

        invalid_answers_ids = [answer_id for answer_id in answers_ids if answer_id not in question_answers_ids]
        if invalid_answers_ids:
            return redirect(redirect_to)

        if len(answers_ids) > len(question_answers):
            return redirect(redirect_to)

        if len(question_right_answers_ids) == 1 and len(answers_ids) > 1:
            return redirect(redirect_to)

        if len(question_right_answers_ids) > 1 and len(answers_ids) > len(question_right_answers_ids):
            return redirect(redirect_to)

        for answer_id in answers_ids:
            answer_backuped_data = [
                question_answer for question_answer in question_answers if question_answer['id'] == answer_id
            ][0]

            try:
                answer_obj = Answer.objects.get(id=answer_id)
            except Answer.DoesNotExist:
                answer_obj = None

            UserExaminationAnswerLog.objects.create(
                answer=answer_obj, is_right=answer_id in question_right_answers_ids,
                user_examination_question_log=user_examination_question_log, answer_data=answer_backuped_data
            )

        user_examination_question_log.finished_at = datetime.datetime.now()
        user_examination_question_log.save()

        return redirect(redirect_to)

    def get_title(self):
        user_examination = self.get_user_examination()
        return 'Тестирование %s, необходимо закончить до %s, осталось %s мин, осталось вопросов: %s' % (
            user_examination.examination, user_examination.must_finished_at.strftime('%d.%m.%Y %H:%M:%S'),
            user_examination.get_remaining_minutes(), UserExaminationQuestionLog.get_remains_for_user_examination(user_examination)
        )

    def get_context_data(self, **kwargs):
        context = super(UserExaminationProcessView, self).get_context_data(**kwargs)
        user_examination = self.get_user_examination()
        user_examination_question_log = self.get_user_examination_question_log()
        context.update({
            'user_examination_question_log': user_examination_question_log,
            'user_examination': user_examination,
            'question': json.loads(user_examination_question_log.question_data),
            'answers': json.loads(user_examination_question_log.question_answers_data),
            'input_type': 'radio' if user_examination_question_log.get_right_answers_count() == 1 else 'checkbox',
            'right_answers_count': self.get_right_answers_count()
        })
        return context
user_examination_process_view = UserExaminationProcessView.as_view()


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
                ql_qs.question_answers_data = json.loads(ql_qs.question_answers_data)
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

    def get_title(self):
        user_examination = self.get_object()
        return 'Пользователь %s, тестирование %s' % (user_examination.user, user_examination.examination)

    def get_context_data(self, **kwargs):
        context = super(UserExaminationDetailView, self).get_context_data(**kwargs)
        context['question_log'] = self.get_question_log()
        context['answer_log'] = self.get_answer_log_for_question_log()
        context['user_examinations_stats'] = self.get_answers_stats()
        context['can_view_logs'] = self.object.can_view_logs(self.request.user)
        return context

user_examination_detail_view = UserExaminationDetailView.as_view()
