# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-08-30 16:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionsAndPapers', '0020_studentweakareasallsscmarks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentweakareasallsscmarks',
            name='student',
        ),
        migrations.DeleteModel(
            name='StudentWeakAreasAllSSCMarks',
        ),
    ]