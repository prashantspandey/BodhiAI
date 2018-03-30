# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-25 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicinformation', '0016_testingcelery'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcustomprofile',
            name='fatherName',
            field=models.CharField(default='baap', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentcustomprofile',
            name='fullName',
            field=models.CharField(default='beta', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentcustomprofile',
            name='kl',
            field=models.CharField(choices=[('10', 'Tenth'), ('11', 'Eleventh'), ('12', 'Twelveth')], default=10, max_length=10),
            preserve_default=False,
        ),
    ]
