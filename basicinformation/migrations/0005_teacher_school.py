# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-27 13:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicinformation', '0004_auto_20170426_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basicinformation.School'),
        ),
    ]
