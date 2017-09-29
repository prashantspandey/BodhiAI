from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField

class School(models.Model):
    category_choices = (('School','School'),('SSC','SSC'))
    name = models.CharField(max_length=200)
    pincode = models.IntegerField()
    category = models.CharField(max_length = 10, choices = category_choices)
    
    def __str__(self):
        return self.name


class klass(models.Model):
    level_choices =\
    (('9','Ninth'),('10','Tenth'),('11','Eleventh'),('12','Twelveth'),('SSC','SSC'))
    school = models.ForeignKey(School)
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=10, choices =
                             level_choices,null=True,blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    studentuser = models.OneToOneField(User,blank=True,null=True)
    klass = models.ForeignKey(klass,related_name='klass')
    rollNumber = models.BigIntegerField()
    name = models.CharField(max_length=200)
    dob = models.DateField()
    pincode = models.IntegerField()
    school = \
    models.ForeignKey(School,related_name='school',blank=True,null=True)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacheruser = models.OneToOneField(User,blank=True,null=True)
    name = models.CharField(max_length=200)
    experience = models.FloatField()
    school = models.ForeignKey(School,blank=True,null=True)
    

    def __str__(self):
        return self.name


class Subject(models.Model):
    student = models.ForeignKey(Student)
    teacher = models.ForeignKey(Teacher,blank=True,null=True)
    name = models.CharField(max_length=200)
    test1 = models.IntegerField(null=True, blank=True)
    test2 = models.IntegerField(null=True, blank=True)
    test3 = models.IntegerField(null=True, blank=True)
    hy = models.IntegerField(null=True, blank=True)
    test4 = models.IntegerField(null=True, blank=True)
    lab1 = models.IntegerField(null=True, blank=True)
    lab2 = models.IntegerField(null=True, blank=True)
    lab3 = models.IntegerField(null=True, blank=True)
    finalexam = models.IntegerField(null=True, blank=True)
    predicted_hy = models.IntegerField(null=True,blank= True)
    prdicted_final = models.IntegerField(null= True, blank=True)

    def __str__(self):
        return \
    '{}---{}----{}----{}'.format(self.name,self.student,self.teacher,self.student.school)

class StudentCustomProfile(models.Model):
    student = models.OneToOneField(Student)
    address = models.CharField(max_length = 400)
    phone = models.IntegerField(null=True, blank=True,
                            validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
   
    def __str__(self):
       return self.student.name

class SchoolManagement(models.Model):
    management = models.OneToOneField(User)
    school = models.ForeignKey(School)

    def __str__(self):
        return 'management of {}'.format(self.school.name)


#class ImprovementStudent(models.Model):
#    testid = ArrayField(models.IntegerField())
#    percent = ArrayField(models.CharField(max_length=10))
#    date = ArrayField(models.CharField(max_length = 10))
#    topic = ArrayField(models.CharField(max_length = 10))
#
#    def __str__(self):
#        return str(self.topic)
