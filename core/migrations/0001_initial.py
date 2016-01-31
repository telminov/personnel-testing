# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=150)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField()),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044f',
                'verbose_name_plural': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('is_right', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '\u043e\u0442\u0432\u0435\u0442',
                'verbose_name_plural': '\u041e\u0442\u0432\u0435\u0442\u044b \u043d\u0430 \u0432\u043e\u043f\u0440\u043e\u0441\u044b',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('employees', models.ManyToManyField(related_name='departments', verbose_name='\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0438 \u043e\u0442\u0434\u0435\u043b\u0430', to=settings.AUTH_USER_MODEL, blank=True)),
                ('parent', models.ForeignKey(related_name='children', verbose_name='\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u043e\u0442\u0434\u0435\u043b', blank=True, to='core.Department', null=True)),
                ('responsible', models.ManyToManyField(related_name='departments_owner', verbose_name='\u041e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0435', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u043f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('repeat_every', models.PositiveIntegerField(help_text='\u0412 \u0434\u043d\u044f\u0445')),
                ('duration', models.PositiveIntegerField(help_text='\u0412 \u0434\u043d\u044f\u0445')),
                ('started_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u0442\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f')),
                ('finished_at', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u0442\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f', blank=True)),
                ('department', models.ForeignKey(related_name='examinations', to='core.Department')),
            ],
            options={
                'verbose_name': '\u0442\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435',
                'verbose_name_plural': '\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('time_limit', models.PositiveSmallIntegerField()),
                ('examination', models.ForeignKey(related_name='questions', to='core.Examination')),
            ],
            options={
                'verbose_name': '\u0432\u043e\u043f\u0440\u043e\u0441',
                'verbose_name_plural': '\u0412\u043e\u043f\u0440\u043e\u0441\u044b',
            },
        ),
        migrations.CreateModel(
            name='UserExamination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('available_from', models.DateTimeField(verbose_name='\u0422\u0435\u0441\u0442 \u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d \u0434\u043b\u044f \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f \u043e\u0442')),
                ('complete_until', models.DateTimeField(verbose_name='\u041d\u0430\u0434\u043e \u0432\u044b\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0434\u043e')),
                ('started_at', models.DateTimeField(null=True, verbose_name='\u041d\u0430\u0447\u0430\u0442', blank=True)),
                ('finished_at', models.DateTimeField(null=True, verbose_name='\u0417\u0430\u043a\u043e\u043d\u0447\u0435\u043d', blank=True)),
                ('examination', models.ForeignKey(related_name='user_examinations', to='core.Examination')),
                ('user', models.ForeignKey(related_name='user_examinations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0442\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='UserExaminationAnswerLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_right', models.BooleanField()),
                ('answer_data', django_extensions.db.fields.json.JSONField()),
                ('answer', models.ForeignKey(to='core.Answer', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
        ),
        migrations.CreateModel(
            name='UserExaminationQuestionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_data', django_extensions.db.fields.json.JSONField()),
                ('started_at', models.DateTimeField(default=datetime.datetime.now)),
                ('finished_at', models.DateTimeField(null=True)),
                ('question', models.ForeignKey(related_name='user_examination_question_logs', on_delete=django.db.models.deletion.DO_NOTHING, to='core.Question')),
                ('user_examination', models.ForeignKey(related_name='user_examination_question_logs', to='core.UserExamination')),
            ],
            options={
                'verbose_name': '\u043e\u0442\u0432\u0435\u0442 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u041e\u0442\u0432\u0435\u0442\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
        ),
        migrations.AddField(
            model_name='userexaminationanswerlog',
            name='user_examination_question_log',
            field=models.ForeignKey(related_name='user_examination_answer_logs', to='core.UserExaminationQuestionLog'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='core.Question'),
        ),
    ]
