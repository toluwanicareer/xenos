# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-01 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDigits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg', models.CharField(max_length=200)),
                ('capi', models.CharField(max_length=200)),
                ('withd', models.CharField(max_length=200)),
                ('depo', models.CharField(max_length=200)),
            ],
        ),
    ]
