# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-17 05:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0003_auto_20180216_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='referer',
            field=models.CharField(max_length=200, null=True),
        ),
    ]