# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-11 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xenos_admin', '0005_auto_20180211_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]