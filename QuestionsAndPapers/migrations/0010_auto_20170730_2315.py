# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-30 17:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionsAndPapers', '0009_klasstest_due_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='onlinemarks',
            old_name='wringAnswers',
            new_name='wrongAnswers',
        ),
    ]