# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-17 04:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xenos_admin', '0014_auto_20180217_0453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='btc_address',
        ),
        migrations.RemoveField(
            model_name='investment',
            name='link',
        ),
        migrations.AlterField(
            model_name='investment',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 17, 5, 8, 24, 286000), null=True),
        ),
    ]
