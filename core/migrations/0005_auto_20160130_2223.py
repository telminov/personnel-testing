# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160130_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveSmallIntegerField(verbose_name='\u0421\u043a\u043e\u043b\u044c\u043a\u043e \u0440\u0430\u0437 \u043f\u043e\u0432\u0442\u043e\u0440\u044f\u0442\u044c')),
                ('period', models.PositiveSmallIntegerField(verbose_name='\u041a\u0430\u043a \u0447\u0430\u0441\u0442\u043e \u043f\u043e\u0432\u0442\u043e\u0440\u044f\u0442\u044c')),
                ('unit', models.PositiveSmallIntegerField(help_text='\u0420\u0430\u0437 \u0432 2 \u043c\u0435\u0441\u044f\u0446\u0430, 3 \u0440\u0430\u0437\u0430 \u0432 \u0433\u043e\u0434', verbose_name='\u0415\u0434\u0438\u043d\u0438\u0446\u0430 \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f \u043f\u0435\u0440\u0438\u043e\u0434\u0430', choices=[('month', '\u041c\u0435\u0441\u044f\u0446'), ('year', '\u0413\u043e\u0434')])),
                ('is_active', models.BooleanField(verbose_name='')),
                ('department', models.ForeignKey(blank=True, to='core.Department', null=True)),
                ('examination', models.ForeignKey(related_name='schedulers', to='core.Examination')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='body',
            field=models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442'),
        ),
        migrations.AlterField(
            model_name='userexamination',
            name='examination',
            field=models.ForeignKey(related_name='user_examinations', verbose_name='\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435', to='core.Examination'),
        ),
        migrations.AlterField(
            model_name='userexamination',
            name='user',
            field=models.ForeignKey(related_name='user_examinations', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL),
        ),
    ]
