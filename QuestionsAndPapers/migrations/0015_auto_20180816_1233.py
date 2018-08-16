# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-08-16 07:03
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicinformation', '0007_auto_20180412_1728'),
        ('QuestionsAndPapers', '0014_auto_20180812_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentWeakAreasCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('accuracies', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(max_length=50), null=True, size=None)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(max_length=50), null=True, size=None)),
                ('subject', models.CharField(max_length=100)),
                ('numTests', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicinformation.Student')),
            ],
        ),
        migrations.AlterField(
            model_name='sscklasstest',
            name='sub',
            field=models.CharField(choices=[('General-Intelligence', 'General-Intelligence'), ('General-Knowledge', 'General-Knowledge'), ('Quantitative-Analysis', 'Quantitative-Analysis'), ('English', 'English'), ('Defence-English', 'Defence-English'), ('Defence-Physics', 'Defence-Physics'), ('GroupX-Maths', 'GroupX-Maths'), ('Defence-GK-CA', 'Defence-GK-CA'), ('SSCMultipleSections', 'SSCMultipleSections'), ('Defence-MultipleSubjects', 'Defence-MultipleSubjects'), ('IITJEE10-MultipleSubjects', 'IITJEE10-MultipleSubjects'), ('IITJEE11-MultipleSubjects', 'IITJEE11-MultipleSubjects'), ('IITJEE12-MultipleSubjects', 'IITJEE12-MultipleSubjects'), ('MathsIITJEE10', 'MathsIITJEE10'), ('MathsIITJEE11', 'MathsIITJEE11'), ('MathsIITJEE12', 'MathsIITJEE12'), ('ChemistryIITJEE10', 'ChemistryIITJEE10'), ('ChemistryIITJEE11', 'ChemistryIITJEE11'), ('ChemistryIITJEE12', 'ChemistryIITJEE12'), ('PhysicsIITJEE10', 'PhysicsIITJEE10'), ('PhysicsIITJEE11', 'PhysicsIITJEE11'), ('PhysicsIITJEE12', 'PhysicsIITJEE12'), ('ElectricalLocoPilot', 'ElectricalLocoPilot')], max_length=70),
        ),
        migrations.AlterField(
            model_name='sscquestions',
            name='section_category',
            field=models.CharField(choices=[('General-Intelligence', 'General-Intelligence'), ('General-Knowledge', 'General-Knowledge'), ('Quantitative-Analysis', 'Quantitative-Analysis'), ('English', 'English'), ('Defence-English', 'Defence-English'), ('Defence-Physics', 'Defence-Physics'), ('GroupX-Maths', 'GroupX-Maths'), ('Defence-GK-CA', 'Defence-GK-CA'), ('MathsIITJEE10', 'MathsIITJEE10'), ('MathsIITJEE11', 'MathsIITJEE11'), ('MathsIITJEE12', 'MathsIITJEE12'), ('ChemistryIITJEE10', 'ChemistryIITJEE10'), ('ChemistryIITJEE11', 'ChemistryIITJEE11'), ('ChemistryIITJEE12', 'ChemistryIITJEE12'), ('PhysicsIITJEE10', 'PhysicsIITJEE10'), ('PhysicsIITJEE11', 'PhysicsIITJEE11'), ('PhysicsIITJEE12', 'PhysicsIITJEE12'), ('Design and analysis of algorithm', 'Design and analysis of algorithm'), ('ElectricalLocoPilot', 'ElectricalLocoPilot')], max_length=70),
        ),
    ]
