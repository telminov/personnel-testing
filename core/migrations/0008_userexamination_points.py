# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160203_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='userexamination',
            name='points',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='\u0411\u0430\u043b\u043b\u044b'),
        ),
    ]
