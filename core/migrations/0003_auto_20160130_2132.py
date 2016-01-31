# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160130_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examination',
            name='finished_at',
        ),
        migrations.RemoveField(
            model_name='examination',
            name='started_at',
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
