# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-17 05:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0004_profile_referer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='wallet',
            field=models.DecimalField(decimal_places=10, max_digits=19, max_length=20, null=True),
        ),
    ]