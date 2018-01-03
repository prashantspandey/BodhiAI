# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-21 07:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicinformation', '0012_auto_20171004_1833'),
        ('QuestionsAndPapers', '0028_sscofflinemarks'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimesReported',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isReported', models.BooleanField()),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuestionsAndPapers.SSCquestions')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicinformation.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='TimesUsed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numUsed', models.IntegerField()),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QuestionsAndPapers.SSCquestions')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicinformation.Teacher')),
            ],
        ),
        migrations.AlterModelOptions(
            name='choices',
            options={'ordering': ['pk']},
        ),
    ]