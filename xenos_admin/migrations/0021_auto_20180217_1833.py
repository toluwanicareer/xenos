# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-17 17:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xenos_admin', '0020_auto_20180217_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 17, 18, 33, 52, 530000), null=True),
        ),
    ]
