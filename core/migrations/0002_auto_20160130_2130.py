# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userexaminationquestionlog',
            options={},
        ),
        migrations.RemoveField(
            model_name='examination',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='examination',
            name='repeat_every',
        ),
        migrations.AlterField(
            model_name='department',
            name='responsible',
            field=models.ManyToManyField(related_name='departments_owner', verbose_name='\u041e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0435\u043d\u043d\u044b\u0435', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='examination',
            name='department',
            field=models.ForeignKey(related_name='examinations', verbose_name='\u041e\u0442\u0434\u0435\u043b', to='core.Department'),
        ),
        migrations.AlterField(
            model_name='examination',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
