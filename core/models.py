# -*- coding: utf-8 -*-
import datetime
import json

import six
from dateutil.relativedelta import relativedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db.models import SET_NULL, DO_NOTHING, Q


class JSONField(models.TextField):
    def __init__(self, *args, **kwargs):
        default = kwargs.get('default', '{}')
        if isinstance(default, (list, dict)):
            kwargs['default'] = json.dumps(default)
        models.TextField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if value is None or value == '':
            return {}
        return json.loads(value)

    def get_db_prep_save(self, value, connection, **kwargs):
        """Convert our JSON object to a string before we save"""
        if value is None and self.null:
            return None
        # default values come in as strings; only non-strings should be
        # run through `dumps`
        if not isinstance(value, six.string_types):
            value = json.dumps(value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        if self.default == '{}':
            del kwargs['default']
        return name, path, args, kwargs


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_expired_examinations(self):
        return self.user_examinations.filter(Q(points=0) | Q(started_at__isnull=True))


class Department(models.Model):
    """ Отдел """
    name = models.CharField(max_length=255, verbose_name='Название')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', verbose_name='Родительский отдел')
    responsible = models.ManyToManyField(User, related_name='departments_owner', blank=True, verbose_name='Ответственные')
    employees = models.ManyToManyField(User, related_name='departments', blank=True, verbose_name='Сотрудники отдела')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'подразделение'
        verbose_name_plural = 'Подразделения'


class Examination(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    department = models.ForeignKey(Department, related_name='examinations', verbose_name='Отдел')

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

    @classmethod
    def get_remains_for_user_examination(cls, user_examination):
        user_examination_question_log = UserExaminationQuestionLog.objects.filter(
            user_examination=user_examination, user_examination_answer_logs__isnull=False
        )

        return Question.objects.filter(examination=user_examination.examination).exclude(
            id__in=user_examination_question_log.values_list('question', flat=True)
        )

    @classmethod
    def get_next_in_examination(cls, user_examination):

        return Question.objects.filter(examination=user_examination.examination).exclude(
            id__in=UserExaminationQuestionLog.objects.filter(
                user_examination=user_examination, user_examination_answer_logs__isnull=False,
            ).values_list('question', flat=True).order_by('?')
        )

    @classmethod
    def get_next_id_in_examination(cls, user_examination):
        try:
            return cls.get_next_in_examination(user_examination).values_list('id', flat=True)[0]
        except Exception as e:
            return None


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

    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Начат')
    finished_at = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name='Закончен')

    class Meta:
        verbose_name = 'тестирование пользователя'
        verbose_name_plural = 'Тестирования пользователей'

    def __unicode__(self):
        return '[UserExamination] #%s' % self.id

    def __str__(self):
        return '#%s' % self.id

    @classmethod
    def get_for_user(cls, user, qs=None):
        return cls.objects.filter(user=user)

    @classmethod
    def fixed_expired(cls):
        now = datetime.datetime.now()
        UserExamination.objects.filter(finished_at__isnull=True, complete_until__lt=now).update(finished_at=now)

    def get_status_color(self):
        if self.points >= 70:
            return 'success'
        else:
            return 'warning'

    def is_expired(self):
        return self.points == 0 or self.started_at is None

    def is_not_passed(self):
        return self.points < 70

    def calculate_points(self, force=False, commit=True):
        assert self.finished_at

        # dont allow recalculate points, if already exists(user exam was finished)
        if not force:
            assert self.points == 0

        points = 0

        questions_count = self.examination.questions.count()
        point_for_one_right_answer = float(100) / questions_count

        for question_log in self.user_examination_question_logs.all():
            right_answers_count = question_log.question.answers.filter(is_right=True).count()
            right_answers_user_count = 0
            for answer in question_log.user_examination_answer_logs.all():
                right_answers_user_count += answer.is_right

            if right_answers_user_count > 0:
                points += point_for_one_right_answer * float(right_answers_count) / right_answers_user_count

        self.points = points

        if commit:
            self.save()

        return self


class UserExaminationQuestionLog(models.Model):
    user_examination = models.ForeignKey(UserExamination, related_name='user_examination_question_logs')
    question = models.ForeignKey(Question, on_delete=DO_NOTHING, related_name='user_examination_question_logs')

    question_data = JSONField(default={})

    started_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)

    # class Meta:
    #     verbose_name = 'ответ пользователя'
    #     verbose_name_plural = 'Ответы пользователей'


class UserExaminationAnswerLog(models.Model):
    user_examination_question_log = models.ForeignKey(UserExaminationQuestionLog, related_name='user_examination_answer_logs')
    is_right = models.BooleanField()

    answer = models.ForeignKey(Answer, on_delete=DO_NOTHING)
    answer_data = JSONField()

    # class Meta:
    #     verbose_name = 'ответ пользователя(конкретно)'
    #     verbose_name_plural = 'Ответы пользователей(конкретно)'


class Scheduler(models.Model):
    WEEK_UNIT_CHOICE = 'week'
    MONTH_UNIT_CHOICE = 'month'

    UNIT_CHOICES = (
        (WEEK_UNIT_CHOICE, 'Неделя'),
        (MONTH_UNIT_CHOICE, 'Месяц'),
    )

    user = models.ForeignKey(User, null=True, blank=True, verbose_name='Пользователь')  # TODO m2m
    department = models.ForeignKey(Department, null=True, blank=True, verbose_name='Отдел')  # TODO m2m
    examination = models.ForeignKey(Examination, related_name='schedulers', verbose_name='Тестирование')

    count = models.PositiveSmallIntegerField(verbose_name='Сколько раз повторять')
    period = models.PositiveSmallIntegerField(verbose_name='Как часто повторять')
    unit = models.CharField(max_length=255, choices=UNIT_CHOICES, verbose_name='Единица измерения периода',
                                            help_text='Раз в 2 месяца, 3 раза в неделю')

    is_active = models.BooleanField(default=False, verbose_name='В работе')

    class Meta:
        verbose_name = 'расписание'
        verbose_name_plural = 'Расписания'

    def get_timedelta(self):
        if self.unit == 'month':
            timedelta = relativedelta(months=-1)
        elif self.unit == 'week':
            timedelta = relativedelta(weeks=-1)
        else:
            raise AttributeError

        return timedelta

    def get_datetime_for_check_period(self, from_dt=None):
        end_period = from_dt or datetime.datetime.now()
        start_period = end_period - self.get_timedelta()

        period_seconds = (start_period - end_period).total_seconds()

        return end_period - datetime.timedelta(
            seconds=float(self.period) / self.count * period_seconds  # TODO подумать над названиями полей(period!)
        )

    def get_users(self):
        users = []
        if self.department:
            users.extend(list(self.department.employees.all()))
        if self.user:
            users.append(self.user)
        return users

    @classmethod
    def check_user_examinations(cls):

        now = datetime.datetime.now()

        for scheduler in cls.objects.filter(is_active=True):
            scheduler_from_dt = scheduler.get_datetime_for_check_period(now)

            for user in scheduler.get_users():
                if not UserExamination.objects.filter(
                    user=user, examination=scheduler.examination,
                    available_from__gte=scheduler_from_dt
                ).exists():
                    UserExamination.objects.create(
                        examination=scheduler.examination, user=user, available_from=now,
                        complete_until=now+datetime.timedelta(days=7)  # TODO hard code 7 days
                    )
