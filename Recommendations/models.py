from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from basicinformation.models import *
from QuestionsAndPapers.models import *
# Create your models here.

class RecommendedContent(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    lang = models.CharField(max_length=50)
    contentType = models.CharField(max_length=100)
    chapter = models.FloatField()
    subject = models.CharField(max_length = 50)
    date = models.DateField(auto_now_add=True)
    source = models.CharField(max_length =200,null=True,blank=True)

    def __str__(self):
        return str(self.subject) + str(self.chapter) + str(self.title)

class Concept(models.Model):
    question = models.ForeignKey(SSCquestions,null=True,blank=True)
    name = models.CharField(max_length=200)
    content = models.ForeignKey(RecommendedContent,null=True,blank=True)
    subject = models.CharField(max_length =200)
    chapter = models.FloatField()
    concpet_number = models.IntegerField()


    def __str__(self):
        return str(self.question.id) +' '+ str(self.name) + ' ' +\
    str(self.subject)\
    + ' ' + str(self.chapter)
