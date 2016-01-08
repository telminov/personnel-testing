# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView
from core.models import UserExamination, Question, UserExaminationAnswer, Answer


def empty():
    pass


class UserExaminationListView(ListView):
    model = UserExamination
    template_name = 'core/examinations.html'

    def get_queryset(self):
        return self.model.get_for_user(self.request.user)


user_examination_list_view = UserExaminationListView.as_view()


class UserExaminationDetailView(DetailView):
    model = UserExamination
    template_name = 'core/examination.html'

    def get_context_data(self, **kwargs):
        context = super(UserExaminationDetailView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(examination=self.object.examination_id)
        return context

user_examination_detail_view = UserExaminationDetailView.as_view()


class UserExaminationQuestionDetailView(DetailView):
    model = UserExamination
    pk_url_kwarg = 'user_examination_id'

    def get_object(self, queryset=None):
        user_examination = super(UserExaminationQuestionDetailView, self).get_object(queryset)

        if not self.kwargs.get('question_id'):
            next_question_id = Question.objects.filter(examination=user_examination.examination_id).exclude(
                id__in=UserExaminationAnswer.get_for_user(self.request.user).values_list('question', flat=True)
            )[0]

            return redirect(reverse('random_question_from_examination', args=[user_examination.id, next_question_id]))

        return user_examination

    def get_context_data(self, **kwargs):
        context = super(UserExaminationQuestionDetailView, self).get_context_data(**kwargs)
        context['question'] = self.object.examination.question
        return context


def user_examination_answer_view(request, user_examination_id, question_pk):
    answers_ids = request.POST.getlist('answer_id')

    if len(answers_ids) < 1:
        raise ValueError('Должен быть хотя бы один ответ')

    user_examination = UserExamination.get_for_user(request.user).objects.get(id=user_examination_id)
    user_examination_question = user_examination.examination.questions.get(id=question_pk)

    if UserExaminationAnswer.filter(user_examination=user_examination, question=user_examination_question).exists():
        raise ValueError

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

    user_examination_answer_defaults = {'user_examination': user_examination, 'question': user_examination_question}

    UserExaminationAnswer.objects.bulk_create(
        [UserExaminationAnswer(
            answer=answer_id, is_right=answer_id in question_right_answers_ids, **user_examination_answer_defaults
        ) for answer_id in answers_ids]
    )
