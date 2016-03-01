# -*- coding: utf-8 -*-
import datetime

from core.models import Department, Examination, Scheduler, User, UserExamination, Question, Answer, UserExaminationQuestionLog, UserExaminationAnswerLog
from django.test import TestCase


class MainTestCase(TestCase):

    def test_user_examination_calculate_points(self):
        department = Department.objects.create(name='test dep')
        examination = Examination.objects.create(name='test exam', department=department)
        user = User.objects.create(username='test', email='admin@admin.com')
        department.employees.add(user)

        now = datetime.datetime.now()
        available_from = now - datetime.timedelta(days=2)
        complete_until = now + datetime.timedelta(days=2)

        user_examination = UserExamination.objects.create(
            examination=examination, user=user, available_from=available_from, complete_until=complete_until,
            finished_at=now
        )

        question = Question.objects.create(examination=examination)
        answer = Answer.objects.create(question=question, is_right=True, body='write')

        user_examination.calculate_points()

        self.assertEqual(user_examination.points, 0)

        user_examination_question_log = UserExaminationQuestionLog.objects.create(
            user_examination=user_examination, question=question
        )
        user_examination_answer_log = UserExaminationAnswerLog.objects.create(
            user_examination_question_log=user_examination_question_log, answer=answer, is_right=True
        )

        user_examination.calculate_points()

        self.assertEqual(user_examination.points, 100)

        user_examination_answer_log.is_right = False
        user_examination_answer_log.save()

        user_examination.calculate_points(force=True)

        self.assertEqual(user_examination.points, 0)

        question2 = Question.objects.create(examination=examination)
        answer2 = Answer.objects.create(question=question2, is_right=True, body='write')
        user_examination_question_log2 = UserExaminationQuestionLog.objects.create(
            user_examination=user_examination, question=question2
        )
        user_examination_answer_log2 = UserExaminationAnswerLog.objects.create(
            user_examination_question_log=user_examination_question_log2, answer=answer2, is_right=False
        )

        user_examination.calculate_points(force=True)

        self.assertEqual(user_examination.points, 0)

        user_examination_answer_log2.is_right = True
        user_examination_answer_log2.save()
        user_examination.calculate_points(force=True)

        self.assertEqual(user_examination.points, 50)

        user_examination_answer_log.is_right = True
        user_examination_answer_log.save()
        user_examination.calculate_points(force=True)

        self.assertEqual(user_examination.points, 100)
