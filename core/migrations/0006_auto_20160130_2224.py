# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20160130_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduler',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='unit',
            field=models.CharField(help_text='\u0420\u0430\u0437 \u0432 2 \u043c\u0435\u0441\u044f\u0446\u0430, 3 \u0440\u0430\u0437\u0430 \u0432 \u0433\u043e\u0434', max_length=255, verbose_name='\u0415\u0434\u0438\u043d\u0438\u0446\u0430 \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f \u043f\u0435\u0440\u0438\u043e\u0434\u0430', choices=[('month', '\u041c\u0435\u0441\u044f\u0446'), ('year', '\u0413\u043e\u0434')]),
        ),
    ]
