# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-16 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160411_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='deleted_at',
            field=models.DateTimeField(db_index=True, null=True),
        ),
    ]