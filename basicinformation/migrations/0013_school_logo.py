# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-21 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicinformation', '0012_auto_20171004_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='logo',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
