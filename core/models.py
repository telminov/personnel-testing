# -*- coding: utf-8 -*-
import datetime
import json
import string

import random
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import DO_NOTHING, Q
from core.managers import UserDefaultManager, UserExcludeDeletedManager, DefaultManager, ExcludeDeletedManager

from core.fields import JSONField
from django.forms import model_to_dict


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, verbose_name='Логин пользователя')
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False, verbose_name='Доступ в административную часть')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = UserExcludeDeletedManager()
    default_objects = UserDefaultManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        same_email_users_qs = User.objects.filter(email=self.email)
        if self.id:
            same_email_users_qs = same_email_users_qs.exclude(id=self.id)
        if self.email and same_email_users_qs.exists():
            raise ValueError('email уже занят')
        return super(User, self).save(*args, **kwargs)

    def set_random_password(self, commit=True):
        password = ''.join([random.choice(string.digits) for i in range(0, 10)])
        self.set_password(password)
        if commit:
            self.save()
        return password

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_expired_examinations(self):
        return self.user_examinations.filter(Q(points=0) | Q(started_at__isnull=True))


class Department(models.Model):
    """ Отдел """
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children',
                               verbose_name='Родительский отдел')
    responsible = models.ManyToManyField(User, related_name='departments_owner', blank=True,
                                         verbose_name='Ответственные')
    employees = models.ManyToManyField(User, related_name='departments', blank=True, verbose_name='Сотрудники отдела')
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = ExcludeDeletedManager()
    default_objects = DefaultManager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'подразделение'
        verbose_name_plural = 'Подразделения'


class Examination(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    minutes_to_pass = models.PositiveSmallIntegerField(default=30, verbose_name='Сколько минут дано на тест')
    department = models.ForeignKey(Department, related_name='examinations', verbose_name='Отдел')
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = ExcludeDeletedManager()
    default_objects = DefaultManager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тестирование'
        verbose_name_plural = 'Тестирования'


class Question(models.Model):
    examination = models.ForeignKey(Examination, related_name='questions', verbose_name='Тестирование')
    body = models.TextField(verbose_name='Текст')

    def __unicode__(self):
        return self.body

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', verbose_name='Вопрос')
    body = models.TextField(verbose_name='Текст')
    is_right = models.BooleanField(default=False, verbose_name='Правильный')

    def __unicode__(self):
        return '[%s] %s' % (self.id, self.body)

    def __str__(self):
        return '[%s] %s' % (self.id, self.body)

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'Ответы на вопросы'


class UserExamination(models.Model):
    examination = models.ForeignKey(Examination, related_name='user_examinations', verbose_name='Тестирование')
    user = models.ForeignKey(User, related_name='user_examinations', verbose_name='Пользователь')

    points = models.PositiveSmallIntegerField(default=0, verbose_name='Баллы')

    available_from = models.DateTimeField(verbose_name='Тест доступен для прохождения от')
    complete_until = models.DateTimeField(db_index=True, verbose_name='Надо выполнить до')

    scheduler = models.ForeignKey('Scheduler', null=True, blank=True, on_delete=DO_NOTHING, related_name='user_examinaions')
    created_by = models.ForeignKey('User', null=True, blank=True, on_delete=DO_NOTHING, related_name='user_examinaions')

    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Начат')
    must_finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Обязан закончить до')
    finished_at = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name='Закончен')

    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = ExcludeDeletedManager()
    default_objects = DefaultManager()

    class Meta:
        verbose_name = 'тестирование пользователя'
        verbose_name_plural = 'Тестирования пользователей'

    def __unicode__(self):
        return '[UserExamination] #%s' % self.id

    def __str__(self):
        return '#%s' % self.id

    def save(self, *args, **kwargs):
        instance = super(UserExamination, self).save(*args, **kwargs)
        if not self.logs.exists() and self.examination.questions.all():
            examination_questions = list(self.examination.questions.all())
            random.shuffle(examination_questions)

            objects_for_bulk = []

            for position, question in enumerate(examination_questions):
                question_answers_data = []
                for answer in question.answers.all():
                    question_answers_data.append(model_to_dict(answer))

                objects_for_bulk.append(UserExaminationQuestionLog(
                    position=position, user_examination=self, question=question,
                    question_data=model_to_dict(question), question_answers_data=question_answers_data
                ))

            UserExaminationQuestionLog.objects.bulk_create(objects_for_bulk)
        return instance


    @classmethod
    def get_for_user(cls, user, **kwargs):
        return cls.objects.filter(user=user, **kwargs)

    @classmethod
    def fixed_expired(cls):
        now = datetime.datetime.now()
        UserExamination.objects.filter(finished_at__isnull=True, complete_until__lt=now).update(finished_at=now)

    @classmethod
    def fixed_started(cls):
        for user_examination_id in UserExamination.objects.filter(finished_at__isnull=True).values_list('id', flat=True):
            cls.fixed_started_one(user_examination_id)

    @classmethod
    def fixed_started_one(cls, user_examination_id):
        user_examination = cls.objects.get(id=user_examination_id, finished_at__isnull=True)
        if datetime.datetime.now() > user_examination.must_finished_at:
            user_examination.finish()
            for question in user_examination.examination.questions.all():
                UserExaminationQuestionLog.objects.get_or_create(
                    user_examination=user_examination, question=question,
                    defaults={'question_data': model_to_dict(question)}
                )

    def get_remaining_minutes(self):
        if self.started_at is None:
            return None
        minutes = int((self.must_finished_at - datetime.datetime.now()).total_seconds() / 60)

        if minutes < 0:
            return 0
        return minutes

    def can_view_logs(self, user=None):
        if user and user.is_staff:
            return True

        if self.finished_at is None:
            return False

        deadline_dt = self.finished_at + datetime.timedelta(hours=1)  # TODO
        return datetime.datetime.now() < deadline_dt

    def finish(self, force=False):
        if not force:
            assert self.finished_at is None
            assert self.points == 0

        self.finished_at = datetime.datetime.now()
        self.calculate_points(commit=False)
        self.save()

    def start(self):
        started_at = datetime.datetime.now()
        must_finished_at = started_at + datetime.timedelta(minutes=self.examination.minutes_to_pass)

        self.started_at = started_at
        self.must_finished_at = must_finished_at
        self.save()

    def get_status_color(self):
        if not self.points and self.is_expired():
            return 'danger'
        elif self.is_not_passed():
            return 'warning'
        else:
            return 'success'

    def is_expired(self):
        return self.points == 0 and self.finished_at

    def is_not_passed(self):
        return self.points < 70

    def calculate_points(self, force=False, commit=True):
        assert self.finished_at

        # dont allow recalculate points, if already exists(user exam was finished)
        if not force:
            assert self.points == 0

        points = 0

        question_logs = self.logs.all()

        questions_count = len(question_logs)
        point_for_one_right_answer = float(100) / questions_count

        for question_log in question_logs:

            right_answers_count = question_log.get_right_answers_count()

            right_answers_user_count = 0
            for answer in question_log.user_examination_answer_logs.all():
                right_answers_user_count += answer.is_right

            if right_answers_user_count > 0:
                points += point_for_one_right_answer * (float(right_answers_user_count) / right_answers_count)

        self.points = points

        if commit:
            self.save()

        return self


class UserExaminationQuestionLog(models.Model):
    user_examination = models.ForeignKey(UserExamination, related_name='logs')
    question = models.ForeignKey(Question, on_delete=DO_NOTHING, related_name='logs')

    position = models.PositiveSmallIntegerField()

    question_data = JSONField(default={})
    question_answers_data = JSONField(default=[])

    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    skipped_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['skipped_at', 'position']
        verbose_name = 'Лог ответов'
        verbose_name_plural = 'Лог ответов'

    @classmethod
    def get_next_id(cls, user_examination):
        try:
            return cls.objects.filter(
                user_examination=user_examination, user_examination_answer_logs__isnull=True
            ).values_list('id', flat=True)[0]
        except Exception as e:
            return None

    @classmethod
    def get_remains_for_user_examination(cls, user_examination):
        qs = cls.objects.filter(user_examination=user_examination)

        return qs.count() - qs.filter(finished_at__isnull=False).count()

    def get_right_answers_count(self):
        return len(
            [qa['is_right'] for qa in json.loads(self.question_answers_data)
             if qa['is_right'] is True]
        )


class UserExaminationAnswerLog(models.Model):
    user_examination_question_log = models.ForeignKey(UserExaminationQuestionLog,
                                                      related_name='user_examination_answer_logs')
    is_right = models.BooleanField()

    answer = models.ForeignKey(Answer, null=True, on_delete=DO_NOTHING)
    answer_data = JSONField()

    class Meta:
        verbose_name = 'Лог ответов на вопросы'
        verbose_name_plural = 'Лог ответов на вопросы'


class Scheduler(models.Model):
    WEEK_UNIT_CHOICE = 'week'
    MONTH_UNIT_CHOICE = 'month'

    UNIT_CHOICES = (
        (WEEK_UNIT_CHOICE, 'Неделя'),
        (MONTH_UNIT_CHOICE, 'Месяц'),
    )

    UNIT_VERBOSE_CHOICES = {
        WEEK_UNIT_CHOICE: 'неделю',
        MONTH_UNIT_CHOICE: 'месяц'
    }

    users = models.ManyToManyField(User, related_name='schedulers', blank=True, verbose_name='Пользователь')
    departments = models.ManyToManyField(Department, related_name='schedulers', blank=True, verbose_name='Отдел')

    examination = models.ForeignKey(Examination, related_name='schedulers', verbose_name='Тестирование')

    count = models.PositiveSmallIntegerField(verbose_name='Сколько раз повторять')
    period = models.PositiveSmallIntegerField(verbose_name='Как часто повторять')
    unit = models.CharField(max_length=255, choices=UNIT_CHOICES, default=WEEK_UNIT_CHOICE,
                            verbose_name='Единица измерения периода',
                            help_text='Например: 1 раз в 2 месяца, 3 раза в 1 неделю')

    is_active = models.BooleanField(default=False, verbose_name='В работе')

    class Meta:
        verbose_name = 'расписание'
        verbose_name_plural = 'Расписания'

    def __str__(self):
        return str(self.id)

    def get_verbose_period(self):
        if self.period != 1:
            verb = '{count} раз в {period} {unit}'
        else:
            verb = '{count} раз в {unit}'

        try:
            if self.period % 100 in (11, 12, 13, 14):
                unit = 'недель' if self.unit == self.WEEK_UNIT_CHOICE else 'месяцев'
            elif self.period % 10 == 1:
                unit = 'неделю' if self.unit == self.WEEK_UNIT_CHOICE else 'месяц'
            elif self.period % 10 in (2, 3, 4):
                unit = 'недели' if self.unit == self.WEEK_UNIT_CHOICE else 'месяца'
            else:
                unit = 'недель' if self.unit == self.WEEK_UNIT_CHOICE else 'месяцев'
        except:
            raise AttributeError

        return verb.format(unit=unit, count=self.count, period=self.period)

    def get_timedelta(self):
        if self.unit == 'month':
            timedelta = relativedelta(months=-1)
        elif self.unit == 'week':
            timedelta = relativedelta(weeks=-1)
        else:
            raise AttributeError

        return timedelta

    def get_next(self, from_dt=None):
        return self.get_datetime_for_check_period(from_dt, for_future=True)

    def get_datetime_for_check_period(self, from_dt=None, for_future=False):
        end_period = from_dt or datetime.datetime.now()
        if for_future:
            start_period = end_period + self.get_timedelta()
        else:
            start_period = end_period - self.get_timedelta()

        period_seconds = (start_period - end_period).total_seconds()

        return end_period - datetime.timedelta(
            seconds=float(self.period) / self.count * period_seconds  # TODO подумать над названиями полей(period!)
        )

    def get_users(self):
        users = {}

        for department in self.departments.all():
            for user in department.employees.all():
                users[user.id] = user

        for user in self.users.all():
            users[user.id] = user

        return users.values()

    @classmethod
    def check_user_examinations(cls):

        now = datetime.datetime.now()

        for scheduler in cls.objects.filter(is_active=True):
            scheduler_from_dt = scheduler.get_datetime_for_check_period(now)
            examination = scheduler.examination

            for user in scheduler.get_users():
                if not UserExamination.objects.filter(
                    user=user, examination=examination, available_from__gte=scheduler_from_dt
                ).exists():
                    UserExamination.objects.create(
                        examination=examination, user=user, available_from=now,
                        complete_until=now + datetime.timedelta(days=7), scheduler=scheduler
                        # TODO hard code 7 days
                    )