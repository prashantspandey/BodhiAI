# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-18 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionsAndPapers', '0040_studentchapterwiseactivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssconlinemarks',
            name='testTakenTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
