# -*- coding: utf-8 -*-
import datetime

from core.models import Department, Examination, Scheduler, User, UserExamination, Question, Answer, UserExaminationQuestionLog, UserExaminationAnswerLog
from django.test import TestCase


class MainTestCase(TestCase):

    def test_scheduler_get_datetime_for_check_period(self):
        department = Department.objects.create(name='test dep')
        examination = Examination.objects.create(name='test exam', department=department)
        scheduler = Scheduler.objects.create(
            examination=examination, count=1, period=1, unit=Scheduler.WEEK_UNIT_CHOICE
        )

        self.assertEqual(
            scheduler.get_datetime_for_check_period().date(),
            (datetime.datetime.now() - datetime.timedelta(days=7)).date()
        )

        scheduler.period = 2
        scheduler.save()

        self.assertEqual(
            scheduler.get_datetime_for_check_period().date(),
            (datetime.datetime.now() - datetime.timedelta(days=14)).date()
        )

    def test_scheduler_check_user_examinations(self):
        department = Department.objects.create(name='test dep')
        examination = Examination.objects.create(name='test exam', department=department)

        user = User.objects.create(username='test', email='admin@admin.com')
        department.employees.add(user)

        self.assertEqual(UserExamination.get_for_user(user).count(), 0)

        scheduler = Scheduler.objects.create(
            department=department, examination=examination, count=1, period=1,
            unit=Scheduler.WEEK_UNIT_CHOICE, is_active=True
        )

        scheduler.check_user_examinations()

        self.assertEqual(UserExamination.get_for_user(user).count(), 1)

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

    def test_user_examination_fixed_expired(self):
        department = Department.objects.create(name='test dep')
        examination = Examination.objects.create(name='test exam', department=department)
        user = User.objects.create(username='test', email='admin@admin.com')
        department.employees.add(user)

        available_from = datetime.datetime.now() - datetime.timedelta(days=2)
        complete_until = datetime.datetime.now() - datetime.timedelta(days=1)
        user_examination = UserExamination.objects.create(
            examination=examination, user=user, available_from=available_from, complete_until=complete_until,
        )

        UserExamination.fixed_expired()

        self.assertIsNotNone(UserExamination.objects.get(id=user_examination.id).finished_at)

    def test_user_examination_fixed_started_one(self):
        department = Department.objects.create(name='test dep')
        examination = Examination.objects.create(name='test exam', department=department)
        question = Question.objects.create(examination=examination)
        question1 = Question.objects.create(examination=examination)
        question2 = Question.objects.create(examination=examination)
        user = User.objects.create(username='test', email='admin@admin.com')
        department.employees.add(user)

        available_from = datetime.datetime.now() - datetime.timedelta(days=2)
        complete_until = datetime.datetime.now() - datetime.timedelta(days=1)
        user_examination = UserExamination.objects.create(
            examination=examination, user=user, available_from=available_from, complete_until=complete_until,
            started_at=available_from, must_finished_at=complete_until
        )

        UserExamination.fixed_started()

        self.assertIsNotNone(UserExamination.objects.get(id=user_examination.id).finished_at)
        self.assertEqual(UserExaminationQuestionLog.objects.count(), 3)

    def test_question_get_remains_for_user_examination(self):
        pass

    def test_question_get_next_in_examination(self):
        pass

    def test_question_get_next_id_in_examination(self):
        pass

    def test_user_examination_can_view_logs(self):
        department = Department.objects.create(name='test dep')
        examination = Examination.objects.create(name='test exam', department=department)
        user = User.objects.create(username='test', email='admin@admin.com')
        user2 = User.objects.create(username='test2', email='admin2@admin.com', is_staff=True)
        department.employees.add(user)

        available_from = datetime.datetime.now() - datetime.timedelta(days=2)
        complete_until = datetime.datetime.now() - datetime.timedelta(days=1)
        user_examination = UserExamination.objects.create(
            examination=examination, user=user,
            available_from=available_from,
            complete_until=complete_until,
            started_at=datetime.datetime.now(),
        )

        self.assertFalse(user_examination.can_view_logs())
        self.assertFalse(user_examination.can_view_logs(user))
        self.assertTrue(user_examination.can_view_logs(user2))

        user_examination.finished_at = datetime.datetime.now()
        user_examination.save()

        self.assertTrue(user_examination.can_view_logs())
        self.assertTrue(user_examination.can_view_logs(user))
        self.assertTrue(user_examination.can_view_logs(user2))

        user_examination.finished_at = datetime.datetime.now() - datetime.timedelta(days=1)
        user_examination.save()

        self.assertFalse(user_examination.can_view_logs())
        self.assertFalse(user_examination.can_view_logs(user))
        self.assertTrue(user_examination.can_view_logs(user2))



