# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-01-25 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectChapters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('code', models.FloatField()),
                ('logo', models.URLField(blank=True, max_length=500, null=True)),
                ('course', models.ManyToManyField(blank=True, null=True, to='learning.Course')),
            ],
        ),
    ]
