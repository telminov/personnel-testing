# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160307_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='userexamination',
            name='must_finished_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Обязан закончить до'),
        ),
    ]
