# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db.models import SET_NULL, DO_NOTHING
from django_extensions.db.fields.json import JSONField
from mptt.models import MPTTModel


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField()

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'пользоватя'
        verbose_name_plural = 'Пользователи'


class Department(MPTTModel):
    """ Отдел, MPTT """
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', verbose_name='Родительский отдел')
    responsible = models.ManyToManyField(User, related_name='departments_owner', verbose_name='Ответственные')
    employees = models.ManyToManyField(User, related_name='departments', blank=True, verbose_name='Сотрудники отдела')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'подразделение'
        verbose_name_plural = 'Подразделения'


class Examination(models.Model):
    name = models.CharField(max_length=255)

    department = models.ForeignKey(Department, related_name='examinations')

    repeat_every = models.PositiveIntegerField(help_text='В днях')
    duration = models.PositiveIntegerField(help_text='В днях')

    started_at = models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата начала тестирования')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания тестирования')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'тестирование'
        verbose_name_plural = 'Тестирования'


class Question(models.Model):
    examination = models.ForeignKey(Examination, related_name='questions')
    name = models.CharField(max_length=255)
    time_limit = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'Вопросы'

    @classmethod
    def get_next_in_examination(cls, examination_id, user_id):
        return Question.objects.filter(examination=examination_id).exclude(
            id__in=UserExaminationAnswer.get_for_user(user_id)
        )

    @classmethod
    def get_next_id_in_examination(cls, examination_id, user_id):
        try:
            return cls.get_next_in_examination(examination_id, user_id).values_list('id', flat=True)[0]
        except Exception as e:
            return None


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    name = models.CharField(max_length=255)
    is_right = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'Ответы на вопросы'


class UserExamination(models.Model):
    examination = models.ForeignKey(Examination, related_name='user_examinations')
    user = models.ForeignKey(User, related_name='user_examinations')

    available_from = models.DateTimeField(verbose_name='Тест доступен для прохождения от')
    complete_until = models.DateTimeField(verbose_name='Надо выполнить до')

    is_finished = models.BooleanField(default=False)

    started_at = models.DateTimeField(verbose_name='Начат')
    finished_at = models.DateTimeField(null=True, verbose_name='Закончен')

    class Meta:
        verbose_name = 'тестирование пользователя'
        verbose_name_plural = 'Тестирования пользователей'

    def __unicode__(self):
        return self.name

    @classmethod
    def get_for_user(cls, user):
        return cls.objects.filter(user=user)


class UserExaminationQuestionLog(models.Model):
    user_examination = models.ForeignKey(UserExamination)
    question = models.ForeignKey(Question)
    name = models.CharField()

    question_data = JSONField()

    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)


class UserExaminationAnswerLog(models.Model):
    user_examination_question_log = models.ForeignKey(UserExaminationQuestionLog)
    name = models.CharField(max_length=255)
    is_right = models.BooleanField()

    answer = models.ForeignKey(Answer, on_delete=DO_NOTHING)