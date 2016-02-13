# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_userexamination_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexamination',
            name='complete_until',
            field=models.DateTimeField(verbose_name='\u041d\u0430\u0434\u043e \u0432\u044b\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0434\u043e', db_index=True),
        ),
        migrations.AlterField(
            model_name='userexamination',
            name='finished_at',
            field=models.DateTimeField(db_index=True, null=True, verbose_name='\u0417\u0430\u043a\u043e\u043d\u0447\u0435\u043d', blank=True),
        ),
    ]
