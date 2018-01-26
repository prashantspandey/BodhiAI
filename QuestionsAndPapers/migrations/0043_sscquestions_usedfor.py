# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-20 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionsAndPapers', '0042_timesused_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='sscquestions',
            name='usedFor',
            field=models.CharField(blank=True, choices=[('SSC', 'SSC'), ('Aptitude', 'Aptitude'), ('Groupx', 'Groupx'), ('Groupy', 'Groupy')], max_length=30, null=True),
        ),
    ]