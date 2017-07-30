from django.db import models
from basicinformation.models import klass,Student,Subject,School
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class KlassTest(models.Model):
    name = models.CharField(max_length=100)
    subject_choices = \
        (('Maths','Maths'),('Science','Science'),('English','English'))
    max_marks = models.PositiveIntegerField() 
    testTakers = models.ManyToManyField(Student)
    published = models.DateField(auto_now_add= True)
    klas = models.ForeignKey(klass,null=True,blank=True)
    creator = models.ForeignKey(User,null=True,blank=True)
    sub = models.CharField(max_length=70,choices = subject_choices)
    due_date = models.DateField(null=True,blank=True)
    def __str__(self):
        return self.name

class Questions(models.Model):
    level_choices = (('9','Ninth'),('10','Tenth'),('11','Eleventh'),('12','Twelveth'))
    ktest = models.ManyToManyField(KlassTest,blank= True)
    chapter_choices = (('1','Chapter 1'),('2','Chapter 2'),('3','Chapter 3'))
    subject_choices = \
        (('Maths','Maths'),('Science','Science'),('English','English'))
    text = models.TextField()
    level = models.CharField(max_length=20,choices = level_choices)
    max_marks = models.IntegerField()
    sub  = models.CharField(max_length=70,choices = subject_choices)
    chapCategory = models.CharField(max_length=30,choices=chapter_choices)
    school = models.ManyToManyField(School)
    picture = models.URLField(null=True,blank=True)
    def __str__(self):
        return self.text[:50]


class Choices(models.Model):
    res_choice = (('Correct','Correct'),('Wrong','Wrong'),('Not decided','Not decided'))
    predicament = models.CharField(max_length= 30, choices = res_choice)    
    quest = models.ForeignKey(Questions)
    text = models.TextField()
    picture = models.URLField(null=True,blank=True)

    def __str__(self):
        if self.text:
            return self.text[:50]
        else:
            return self.picture

class OnlineMarks(models.Model):
    test = models.ForeignKey(KlassTest)
    student = models.ForeignKey(Student)
    rightAnswers = ArrayField(models.IntegerField())
    wrongAnswers = ArrayField(models.IntegerField())
    allAnswers = ArrayField(models.IntegerField())
    skippedAnswers = ArrayField(models.IntegerField())
    marks = models.IntegerField()
    testTaken = models.DateField()
    def __str__(self):
        return str(self.marks)
    


