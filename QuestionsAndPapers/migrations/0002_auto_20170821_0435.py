# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-20 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionsAndPapers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporaryanswerholder',
            name='answers',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='temporaryanswerholder',
            name='quests',
            field=models.CharField(max_length=4),
        ),
    ]