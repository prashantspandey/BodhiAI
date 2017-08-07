# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-27 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionsAndPapers', '0007_auto_20170727_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='kl',
        ),
        migrations.AddField(
            model_name='questions',
            name='level',
            field=models.CharField(choices=[('9', 'Ninth'), ('10', 'Tenth'), ('11', 'Eleventh'), ('12', 'Twelveth')], default='10', max_length=20),
            preserve_default=False,
        ),
    ]