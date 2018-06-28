# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-06-27 08:56
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicinformation', '0007_auto_20180412_1728'),
        ('QuestionsAndPapers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentSmartTestTopics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topics', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('weakness', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), size=None)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicinformation.Student')),
                ('test', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='QuestionsAndPapers.SSCKlassTest')),
            ],
        ),
    ]
