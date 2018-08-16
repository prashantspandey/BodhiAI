from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from basicinformation.models import *
from QuestionsAndPapers.models import *
# Create your models here.

class RecommendedContent(models.Model):
    weakness = models.ForeignKey(StudentWeakAreasCache,null=True,blank=True)
    title = models.CharField(max_length=200)
    url = models.URLField()
    lang = models.CharField(max_length=50)
    contentType = models.CharField(max_length=100)
    chapter = models.FloatField()
    subject = models.CharField(max_length = 50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.subject) + str(self.chapter) + str(self.title)


