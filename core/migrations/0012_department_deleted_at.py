# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-17 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20160416_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='deleted_at',
            field=models.DateTimeField(db_index=True, null=True),
        ),
    ]
