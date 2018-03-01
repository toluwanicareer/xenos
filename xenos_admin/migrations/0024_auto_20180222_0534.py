# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-22 04:34
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xenos_admin', '0023_auto_20180222_0453'),
    ]

    operations = [
        migrations.AddField(
            model_name='xenos_payment',
            name='status',
            field=models.CharField(choices=[(b'Pending', b'Pending'), (b'Success', b'Success')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 22, 5, 34, 40, 273000), null=True),
        ),
        migrations.AlterField(
            model_name='xenos_payment',
            name='bought_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
