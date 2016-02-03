# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160130_2224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scheduler',
            options={'verbose_name': '\u0440\u0430\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435', 'verbose_name_plural': '\u0420\u0430\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u044f'},
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='department',
            field=models.ForeignKey(verbose_name='\u041e\u0442\u0434\u0435\u043b', blank=True, to='core.Department', null=True),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='examination',
            field=models.ForeignKey(related_name='schedulers', verbose_name='\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435', to='core.Examination'),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='\u0412 \u0440\u0430\u0431\u043e\u0442\u0435'),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='unit',
            field=models.CharField(help_text='\u0420\u0430\u0437 \u0432 2 \u043c\u0435\u0441\u044f\u0446\u0430, 3 \u0440\u0430\u0437\u0430 \u0432 \u043d\u0435\u0434\u0435\u043b\u044e', max_length=255, verbose_name='\u0415\u0434\u0438\u043d\u0438\u0446\u0430 \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f \u043f\u0435\u0440\u0438\u043e\u0434\u0430', choices=[('week', '\u041d\u0435\u0434\u0435\u043b\u044f'), ('month', '\u041c\u0435\u0441\u044f\u0446')]),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='user',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
