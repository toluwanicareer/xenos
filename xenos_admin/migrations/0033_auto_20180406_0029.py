# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-05 23:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xenos_admin', '0032_auto_20180405_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 6, 0, 29, 31, 305960), null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]
