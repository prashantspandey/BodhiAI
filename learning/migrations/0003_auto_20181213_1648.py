# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-12-13 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0002_auto_20181213_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjectchapters',
            name='course',
        ),
        migrations.AddField(
            model_name='subjectchapters',
            name='course',
            field=models.ManyToManyField(blank=True, null=True, to='learning.Course'),
        ),
    ]
