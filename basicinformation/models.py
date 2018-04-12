from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField

class School(models.Model):
    category_choices = (('School','School'),('SSC','SSC'))
    name = models.CharField(max_length=200)
    pincode = models.IntegerField()
    category = models.CharField(max_length = 10, choices =
                                category_choices,null=True,blank=True)
    logo = models.URLField(max_length = 500,null=True,blank=True)
    
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
    rollNumber = models.BigIntegerField(null=True,blank=True)
    name = models.CharField(max_length=200)
    dob = models.DateField(null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    school = \
    models.ForeignKey(School,related_name='school',blank=True,null=True)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacheruser = models.OneToOneField(User,blank=True,null=True)
    name = models.CharField(max_length=200)
    experience = models.FloatField()
    school = models.ForeignKey(School,blank=True,null=True)
    subBatch = models.CharField(max_length=5,null=True,blank=True)
    

    def __str__(self):
        return self.name


class Subject(models.Model):
    student = models.ForeignKey(Student)
    teacher = models.ForeignKey(Teacher,blank=True,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return \
    '{}---{}----{}----{}'.format(self.name,self.student,self.teacher,self.student.school)

class StudentCustomProfile(models.Model):
    kl_choices =\
    (('10','Tenth'),('11','Eleventh'),('12','Twelveth'))
    student = models.OneToOneField(User,null=True,blank=True)
    address = models.CharField(max_length = 400,null=True,blank=True)
    phone = models.BigIntegerField(null=True, blank=True,
                            validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
    kl = models.CharField(max_length = 10,choices =\
                          kl_choices,null=True,blank=True)
    fatherName = models.CharField(max_length = 200,null=True,blank=True)
    fullName = models.CharField(max_length = 200,null=True,blank=True)
     
    def __str__(self):
        return str(self.fullName)+' ' + str(self.fatherName)

class StudentConfirmation(models.Model):
    name = models.CharField(max_length = 200)
    student = models.OneToOneField(User,null=True,blank=True)
    teacher = models.OneToOneField(Teacher,null=True,blank=True)
    batch = models.ForeignKey(klass,null=True,blank=True)
    school = models.ForeignKey(School)
    phone = models.BigIntegerField(null=True, blank=True,
                            validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
    confirm = models.NullBooleanField()

    def __str__(self):
        return str(self.student) + str(self.school.name) 



class StudentProfile(models.Model):
    student = models.OneToOneField(User,null=True,blank=True)
    phone = models.BigIntegerField(null=True, blank=True,
                            validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
    school = models.ForeignKey(School,null=True,blank=True)
    batch = models.ForeignKey(klass,null=True,blank=True)
    code = models.CharField(max_length = 100)

     
    def __str__(self):
        return str(self.student.first_name)


class SchoolManagement(models.Model):
    management = models.OneToOneField(User)
    school = models.ForeignKey(School)

    def __str__(self):
        return 'management of {}'.format(self.school.name)

class InterestedPeople(models.Model):
    number = models.BigIntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return str(self.number)+str(self.time)


class TeacherClasses(models.Model):
    teacher = models.ForeignKey(Teacher)
    klass = models.CharField(max_length=50)
    numStudents = models.IntegerField()

    def __str__(self):
        return str(self.teacher)+str(self.klass)


#class ImprovementStudent(models.Model):
#    testid = ArrayField(models.IntegerField())
#    percent = ArrayField(models.CharField(max_length=10))
#    date = ArrayField(models.CharField(max_length = 10))
#    topic = ArrayField(models.CharField(max_length = 10))
#
#    def __str__(self):
#        return str(self.topic)
