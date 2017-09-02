# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-21 18:50
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionsAndPapers', '0004_auto_20170821_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinemarks',
            name='allAnswers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), size=None),
        ),
        migrations.AlterField(
            model_name='onlinemarks',
            name='rightAnswers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), size=None),
        ),
        migrations.AlterField(
            model_name='onlinemarks',
            name='skippedAnswers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), size=None),
        ),
        migrations.AlterField(
            model_name='onlinemarks',
            name='wrongAnswers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), size=None),
        ),
        migrations.AlterField(
            model_name='ssconlinemarks',
            name='allAnswers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), size=None),
        ),
        migrations.AlterField(
            model_name='ssconlinemarks',
            name='rightAnswers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), size=None),
        ),
        migrations.AlterField(
            model_name='ssconlinemarks',
            name='skippedAnswers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), size=None),
        ),
        migrations.AlterField(
            model_name='ssconlinemarks',
            name='wrongAnswers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), size=None),
        ),
    ]