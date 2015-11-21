# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
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


class Organization(models.Model):
    """ Организация, MobilMed """
    name = models.CharField(max_length=255)
    director = models.ForeignKey(User, related_name='organizations')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'организацию'
        verbose_name_plural = 'Организации'


class Department(MPTTModel):
    """ Отдел, MPTT """
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', verbose_name='Родительский отдел')
    responsible = models.ForeignKey(User, verbose_name='Ответственный')  # TODO m2m
    organization = models.ForeignKey(Organization, related_name='departments')
    employees = models.ManyToManyField(User, related_name='departments', blank=True, verbose_name='Сотрудники отдела')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'подразделение'
        verbose_name_plural = 'Подразделения'


class Examination(models.Model):
    name = models.CharField(max_length=255)

    department = models.ForeignKey(Department, related_name='examinations')

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
    right_answer = models.ForeignKey('Answer', related_name='questions')  # TODO убрать, ответов много
    time_limit = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='choices')
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

    started_at = models.DateTimeField(verbose_name='Начат')
    finished_at = models.DateTimeField(verbose_name='Закончен')

    class Meta:
        verbose_name = 'тестирование пользователя'
        verbose_name_plural = 'Тестирования пользователей'


class UserExaminationAnswer(models.Model):
    user_examination = models.ForeignKey(UserExamination, related_name='user_answers')
    question = models.ForeignKey(Question, related_name='user_answers')
    answer = models.ForeignKey(Answer, related_name='user_answers')
    is_right = models.BooleanField()

    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()

    class Meta:
        verbose_name = 'ответы пользователей'
        verbose_name_plural = 'Ответы пользователей'


