# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-22 14:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xenos_admin', '0025_auto_20180222_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 22, 15, 28, 51, 609000), null=True),
        ),
    ]
