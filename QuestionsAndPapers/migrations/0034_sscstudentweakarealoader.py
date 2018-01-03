# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-18 10:39
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicinformation', '0013_school_logo'),
        ('QuestionsAndPapers', '0033_auto_20171214_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='SscStudentWeakAreaLoader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topics', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('weakTopics', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('weakTiming', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('weakTimingFreq', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicinformation.Student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicinformation.Subject')),
            ],
        ),
    ]