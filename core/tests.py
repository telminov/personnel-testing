# -*- coding: utf-8 -*-
import datetime
import json

from core.models import Department, Examination, Scheduler, User, UserExamination, Question, Answer, UserExaminationQuestionLog, UserExaminationAnswerLog
from django.core.urlresolvers import reverse
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
            examination=examination, count=1, period=1,
            unit=Scheduler.WEEK_UNIT_CHOICE, is_active=True
        )
        scheduler.departments.add(department)

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

        question = Question.objects.create(examination=examination)
        answer = Answer.objects.create(question=question, is_right=True, body='write')

        user_examination = UserExamination.objects.create(
            examination=examination, user=user, available_from=available_from, complete_until=complete_until,
            finished_at=now
        )

        user_examination.calculate_points()

        self.assertEqual(user_examination.points, 0)

        # user_examination_question_log = UserExaminationQuestionLog.objects.get(
        #     user_examination=user_examination, question=question
        # )
        # user_examination_answer_log = UserExaminationAnswerLog.objects.create(
        #     user_examination_question_log=user_examination_question_log, answer=answer, is_right=True
        # )
        #
        # user_examination.calculate_points()
        #
        # self.assertEqual(user_examination.points, 100)
        #
        # user_examination_answer_log.is_right = False
        # user_examination_answer_log.save()
        #
        # user_examination.calculate_points(force=True)
        #
        # self.assertEqual(user_examination.points, 0)
        #
        # question2 = Question.objects.create(examination=examination)
        # answer2 = Answer.objects.create(question=question2, is_right=True, body='write')
        # user_examination_question_log2 = UserExaminationQuestionLog.objects.create(
        #     user_examination=user_examination, question=question2
        # )
        # user_examination_answer_log2 = UserExaminationAnswerLog.objects.create(
        #     user_examination_question_log=user_examination_question_log2, answer=answer2, is_right=False
        # )
        #
        # user_examination.calculate_points(force=True)
        #
        # self.assertEqual(user_examination.points, 0)
        #
        # user_examination_answer_log2.is_right = True
        # user_examination_answer_log2.save()
        # user_examination.calculate_points(force=True)
        #
        # self.assertEqual(user_examination.points, 50)
        #
        # user_examination_answer_log.is_right = True
        # user_examination_answer_log.save()
        # user_examination.calculate_points(force=True)
        #
        # self.assertEqual(user_examination.points, 100)

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

    # def test_department_import(self):
    #     url_path = reverse('department_import')
    #     response = self.client.get(url_path)
    #     self.assertEqual(response.status_code, 422)
    #     response_error = json.loads(str(response.content, encoding='utf8'))
    #     self.assertEqual(response_error['errors'], "Empty POST")
    #
    #     response = self.client.post(url_path)
    #     self.assertEqual(response.status_code, 422)
    #
    #     name = "Vasa"
    #     response = self.client.post(url_path, data={'name': name})
    #     self.assertEqual(response.status_code, 200)
    #     response_data = json.loads(str(response.content, encoding='utf8'))
    #     self.assertEqual(response_data['name'], name)
    #     self.assertEqual(response_data['id'], 1)
    #
    #     self.assertTrue(Department.objects.filter(name=response_data['name']).exists())
    #
    # def test_user_import(self):
    #     url_path = reverse('user_import')
    #     response = self.client.get(url_path)
    #
    #     self.assertEqual(response.status_code, 422)
    #     response_data = json.loads(str(response.content, encoding='utf8'))
    #     self.assertEqual(response_data['errors'], "Empty POST")
    #
    #     response = self.client.post(url_path)
    #     self.assertEqual(response.status_code, 422)
    #
    #     new_department = Department.objects.create(name='new_department')
    #     response = self.client.post(url_path, {
    #         'department': new_department.id,
    #         'username': 'Petya',
    #         'email': 'Petya@koze.ru',
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     response_data = json.loads(str(response.content, encoding='utf8'))
    #     new_user = User.objects.get(username='Petya')
    #     self.assertEqual(response_data['username'], new_user.username)
    #     self.assertEqual(response_data['email'], new_user.email)
    #     self.assertTrue(new_user.check_password(response_data['password']))

    def test_user_list_view(self):
        url = reverse('user_list_view')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        user = User.objects.create(username="TestUser", email='test@test.ru')
        user.set_password('123')
        user.save()

        self.client.login(username=user.username, password='123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        user.is_staff = True
        user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        user2 = User.objects.create(username="TestUser2")
        department = Department.objects.create(name='Test')

        response = self.client.get(url)
        self.assertIn(user, response.context['users'])
        self.assertIn(user2, response.context['users'])

        p = {
            'department': department.id
        }

        response = self.client.get(url, p)

        self.assertNotIn(user, response.context['users'])
        self.assertNotIn(user2, response.context['users'])

        user.departments.add(department)
        response = self.client.get(url, p)
        self.assertIn(user, response.context['users'])
        self.assertNotIn(user2, response.context['users'])

    def test_user_create_view(self):
        url = reverse('user_create_view')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        user = User.objects.create(username="TestUser", email='test@test.ru')
        user.set_password('123')
        user.save()

        self.client.login(username=user.username, password='123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        user.is_staff = True
        user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        p = {}

        response = self.client.post(url, p)
        self.assertTrue(response.context['form'].errors)

        p = {
            'username': 'test'
        }

        response = self.client.post(url, p)
        self.assertTrue(response.context['form'].errors)

        p = {
            'username': 'TestUser',  # Этот юзер уже создан.
            'password': '123'
        }

        response = self.client.post(url, p)
        self.assertTrue(response.context['form'].errors)

        p = {
            'username': 'Test',
            'password': '123'
        }

        response = self.client.post(url, p)
        self.assertIsNone(response.context)
        user = User.objects.latest('id')
        self.assertEqual(user.username, p['username'])
        self.assertTrue(user.check_password(p['password']))

        p = {
            'username': 'Test1',
            'password': '123',
            'email': 'test.ru'
        }

        response = self.client.post(url, p)
        self.assertTrue(response.context['form'].errors)

        p = {
            'username': 'Test1',
            'password': '123',
            'email': 'test@test.ru'
        }

        response = self.client.post(url, p)
        self.assertTrue(response.context['form'].errors)

        p = {
            'username': 'Test1',
            'password': '123',
            'email': 'test@test.com'
        }

        response = self.client.post(url, p)
        self.assertIsNone(response.context)
        user = User.objects.latest('id')
        self.assertEqual(user.email, p['email'])

        department = Department.objects.create(name='Test')

        p = {
            'username': 'Test2',
            'password': '123',
            'email': 'test1@test.com',
            'departments': [department.id]
        }

        response = self.client.post(url, p)
        self.assertIsNone(response.context)
        user = User.objects.latest('id')
        self.assertIn(department, user.departments.all())

        p = {
            'username': 'Test3',
            'password': '123',
            'email': 'test2@test.com',
            'departments': [department.id],
            'is_staff': True
        }

        response = self.client.post(url, p)
        self.assertIsNone(response.context)
        user = User.objects.latest('id')
        self.assertTrue(user.is_staff)

    def test_user_update_view(self):
        user = User.objects.create(username="TestUser", email='test@test.ru')
        user.set_password('123')
        user.save()
        url = reverse('user_update_view', args=[user.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=user.username, password='123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        user.is_staff = True
        user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        department = Department.objects.create(name='Test')
        p = {
            'username': 'Test1',
            'email': 'test2@test.com',
            'departments': [department.id]
        }

        response = self.client.post(url, p)
        self.assertIsNone(response.context)
        user = User.objects.latest('id')
        self.assertEqual(user.username, p['username'])
        self.assertEqual(user.email, p['email'])
        self.assertIn(department, user.departments.all())

        p = {
            'is_staff': False
        }
        response = self.client.post(url, p)
        self.assertEqual(response.status_code, 302)
        user = User.objects.latest('id')
        self.assertFalse(user.is_staff)














