from django.db import models
from basicinformation.models import klass,Student,Subject
from django.contrib.auth.models import User
# Create your models here.


class KlassTest(models.Model):
    name = models.CharField(max_length=100)
    max_marks = models.PositiveIntegerField()
    user_marks = models.ManyToManyField(Student,null=True,blank=True)
    published = models.DateTimeField(auto_now_add= True)
    klas = models.ForeignKey(klass,null=True,blank=True)
    creator = models.ForeignKey(User,null=True,blank=True)
    def __str__(self):
        return self.name

class Questions(models.Model):
    ktest = models.ManyToManyField(KlassTest,blank= True)
    klass_choices = (('9','Ninth'),('10','Tenth'),('11','Eleventh'),('12','Twelfth'))
    chapter_choices = (('1','Chapter 1'),('2','Chapter 2'),('3','Chapter 3'))
    text = models.TextField()
    kl = models.ForeignKey(klass,null=True,blank=True)
    max_marks = models.IntegerField()
    category = models.ForeignKey(Subject)
    
    def __str__(self):
        return self.text[:50]


class Choices(models.Model):
    res_choice = (('Correct','Correct'),('Wrong','Wrong'),('Not decided','Not decided'))
    predicament = models.CharField(max_length= 30, choices = res_choice)    
    quest = models.ForeignKey(Questions)
    text = models.TextField()
    

    def __str__(self):
        return self.text[:50]


