# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-07 10:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicinformation', '0019_auto_20180307_1542'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TeacherSubjects',
            new_name='TeacherClasses',
        ),
    ]