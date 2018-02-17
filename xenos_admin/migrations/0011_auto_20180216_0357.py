# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-16 02:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xenos_admin', '0010_auto_20180214_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 16, 3, 57, 2, 693092), null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed')], default='Pending', max_length=200, null=True),
        ),
    ]