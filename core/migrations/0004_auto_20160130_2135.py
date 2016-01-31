# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160130_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='name',
        ),
        migrations.RemoveField(
            model_name='question',
            name='name',
        ),
        migrations.RemoveField(
            model_name='question',
            name='time_limit',
        ),
        migrations.AddField(
            model_name='answer',
            name='body',
            field=models.TextField(default='', verbose_name='\u0422\u0435\u043a\u0441\u0442'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='body',
            field=models.CharField(default='', max_length=255, verbose_name='\u0422\u0435\u043a\u0441\u0442'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_right',
            field=models.BooleanField(default=False, verbose_name='\u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0439'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441', to='core.Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='examination',
            field=models.ForeignKey(related_name='questions', verbose_name='\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435', to='core.Examination'),
        ),
    ]
