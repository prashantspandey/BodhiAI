# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-27 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionsAndPapers', '0008_auto_20170727_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='klasstest',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
