# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-22 17:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0007_profile_passpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='passpost',
        ),
    ]