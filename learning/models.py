from django.db import models
from basicinformation.models import *
from Recommendations.models import Concepts
from QuestionsAndPapers.models import *
from django.contrib.auth.models import User 
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class SubjectChapters(models.Model):
    subject = models.CharField(max_length = 200)
    name = models.CharField(max_length =200)
    code = models.FloatField()

    def __str__(self):
        return str(self.subject) + ' ' + str(self.name)
