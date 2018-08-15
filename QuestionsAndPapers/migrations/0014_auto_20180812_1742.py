# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-08-12 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionsAndPapers', '0013_studenttestanalysis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sscklasstest',
            name='sub',
            field=models.CharField(choices=[('General-Intelligence', 'General-Intelligence'), ('General-Knowledge', 'General-Knowledge'), ('Quantitative-Analysis', 'Quantitative-Analysis'), ('English', 'English'), ('Defence-English', 'Defence-English'), ('Defence-Physics', 'Defence-Physics'), ('GroupX-Maths', 'GroupX-Maths'), ('Defence-GK-CA', 'Defence-GK-CA'), ('SSCMultipleSections', 'SSCMultipleSections'), ('Defence-MultipleSubjects', 'Defence-MultipleSubjects'), ('IITJEE10-MultipleSubjects', 'IITJEE10-MultipleSubjects'), ('IITJEE11-MultipleSubjects', 'IITJEE11-MultipleSubjects'), ('IITJEE12-MultipleSubjects', 'IITJEE12-MultipleSubjects'), ('MathsIITJEE10', 'MathsIITJEE10'), ('MathsIITJEE11', 'MathsIITJEE11'), ('MathsIITJEE12', 'MathsIITJEE12'), ('ChemistryIITJEE10', 'ChemistryIITJEE10'), ('ChemistryIITJEE11', 'ChemistryIITJEE11'), ('ChemistryIITJEE12', 'ChemistryIITJEE12'), ('PhysicsIITJEE10', 'PhysicsIITJEE10'), ('PhysicsIITJEE11', 'PhysicsIITJEE11'), ('PhysicsIITJEE12', 'PhysicsIITJEE12'), ('PhysicsLocoPilot', 'PhysicsLocoPilot')], max_length=70),
        ),
        migrations.AlterField(
            model_name='sscquestions',
            name='section_category',
            field=models.CharField(choices=[('General-Intelligence', 'General-Intelligence'), ('General-Knowledge', 'General-Knowledge'), ('Quantitative-Analysis', 'Quantitative-Analysis'), ('English', 'English'), ('Defence-English', 'Defence-English'), ('Defence-Physics', 'Defence-Physics'), ('GroupX-Maths', 'GroupX-Maths'), ('Defence-GK-CA', 'Defence-GK-CA'), ('MathsIITJEE10', 'MathsIITJEE10'), ('MathsIITJEE11', 'MathsIITJEE11'), ('MathsIITJEE12', 'MathsIITJEE12'), ('ChemistryIITJEE10', 'ChemistryIITJEE10'), ('ChemistryIITJEE11', 'ChemistryIITJEE11'), ('ChemistryIITJEE12', 'ChemistryIITJEE12'), ('PhysicsIITJEE10', 'PhysicsIITJEE10'), ('PhysicsIITJEE11', 'PhysicsIITJEE11'), ('PhysicsIITJEE12', 'PhysicsIITJEE12'), ('Design and analysis of algorithm', 'Design and analysis of algorithm'), ('PhysicsLocoPilot', 'PhysicsLocoPilot')], max_length=70),
        ),
    ]
