from django.db import models
from basicinformation.models import *
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class KlassTest(models.Model):
    mode_choices =\
    (('BodhiOnline','BodhiOnline'),('BodhiSchool','BodhiSchool'))
    name = models.CharField(max_length=100)
    subject_choices = (('Maths','Maths'),('Science','Science'),('English','English')) 
    max_marks = models.PositiveIntegerField() 
    testTakers = models.ManyToManyField(Student)
    published = models.DateField(auto_now_add= True)
    klas = models.ForeignKey(klass,null=True,blank=True) 
    creator = models.ForeignKey(User,null=True,blank=True)
    sub = models.CharField(max_length=70,choices = subject_choices)
    due_date = models.DateField(null=True,blank=True)
    mode = models.CharField(max_length=20,choices = mode_choices)
    totalTime = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.name
class SSCKlassTest(models.Model):
    mode_choices =\
    (('BodhiOnline','BodhiOnline'),('BodhiSchool','BodhiSchool'))
    name = models.CharField(max_length=100)
    subject_choices = \
        (('General Intelligence','General Intelligence'),('General Knowledge &\
        General Awareness','General Knowledge & General Awareness')
         ,('Quantitatie Analysis','Quantitatie Analysis'),('English','English'),
        ('SSCMultipleSections','SSCMultipleSections'))

    max_marks = models.DecimalField(max_digits=4,decimal_places=2)
    testTakers = models.ManyToManyField(Student)
    published = models.DateField(auto_now_add= True)
    klas = models.ForeignKey(klass,null=True,blank=True)
    creator = models.ForeignKey(User,null=True,blank=True)
    sub = models.CharField(max_length=70,choices = subject_choices)
    due_date = models.DateField(null=True,blank=True)
    mode = models.CharField(max_length=20,choices = mode_choices)
    totalTime = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.name

class Comprehension(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:100]




class Questions(models.Model):
    ch = 1 
    tp = 1 
    topic_choice = []
    topic_choice2 = []
    for ch in range(1,20):
        for tp in range(1,20):
            topic_choice.append(str(ch)+'.'+str(tp))
            topic_choice2.append(str(ch)+'.'+str(tp))
    tp_choice = list(zip(topic_choice,topic_choice2))
    topic_choice = tuple(tp_choice)
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
    topic_category = models.CharField(max_length=10,choices = topic_choice)
    school = models.ManyToManyField(School)
    picture = models.URLField(null=True,blank=True)
    def __str__(self):
        return self.text[:50]
class SSCquestions(models.Model):
    ch = 1 
    tp = 1 
    topic_choice = []
    topic_choice2 = []
    for ch in range(1,10):
        for tp in range(1,10):
            topic_choice.append(str(ch)+'.'+str(tp))
            topic_choice2.append(str(ch)+'.'+str(tp))
    tp_choice = list(zip(topic_choice,topic_choice2))
    topic_choice = tuple(tp_choice)
    comprehension = models.ForeignKey(Comprehension,blank=True,null=True)
    ktest = models.ManyToManyField(SSCKlassTest,blank= True)
    max_marks = models.IntegerField(default= 2)
    negative_marks =\
    models.DecimalField(max_digits=2,decimal_places=2,default=0.25)
    tier_choices = (('1','Tier1'),('2','Tier2'),('3','Tier3'))
    section_choices = \
        (('General Intelligence','General Intelligence'),('General Knowledge &\
        General Awareness','General Knowledge & General Awareness')
         ,('Quantitatie Analysis','Quantitatie Analysis'),('English','English'))
    diffculty_choices = (('easy','easy'),('medium','medium'),('hard','hard'))
    text = models.TextField(blank=True,null=True)
    tier_category = models.CharField(max_length=20,choices = tier_choices)
    section_category  = models.CharField(max_length=70,choices = section_choices)
    diffculty_category = models.CharField(max_length = 10,choices =
                                          diffculty_choices,null=True,blank=True)
    topic_category = models.CharField(max_length=5,choices = topic_choice)
    school = models.ManyToManyField(School)
    picture = models.URLField(null=True,blank=True)
    def __str__(self):
        return self.text[:50]

class Choices(models.Model):
    res_choice = (('Correct','Correct'),('Wrong','Wrong'),('Not decided','Not decided'))
    predicament = models.CharField(max_length= 30, choices = res_choice)    
    quest = models.ForeignKey(Questions,blank=True,null=True)
    sscquest = models.ForeignKey(SSCquestions,blank=True,null=True)
    text = models.TextField()
    picture = models.URLField(null=True,blank=True)
    explanation = models.TextField(null=True,blank=True)

    def __str__(self):
        if self.text:
            return self.text[:50]
        else:
            return self.picture

class OnlineMarks(models.Model):
    test = models.ForeignKey(KlassTest)
    student = models.ForeignKey(Student)
    rightAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    wrongAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    allAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    skippedAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    marks = models.IntegerField()
    testTaken = models.DateField()
    timeTaken = models.IntegerField()
    def __str__(self):
        return str(self.marks)
    
class SSCOnlineMarks(models.Model):
    test = models.ForeignKey(SSCKlassTest)
    student = models.ForeignKey(Student)
    rightAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    wrongAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    allAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    skippedAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    marks = models.DecimalField(max_digits=4,decimal_places=2)
    testTaken = models.DateField()
    timeTaken = models.IntegerField()
    def __str__(self):
        return str(self.marks)

class TemporaryAnswerHolder(models.Model):
    stud = models.ForeignKey(Student,null=True,blank=True)
    test = models.ForeignKey(SSCKlassTest)
    quests = models.CharField(max_length=10)
    answers = models.CharField(max_length=10)
    time = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.stud)

class SSCansweredQuestion(models.Model):
    onlineMarks = models.ForeignKey(SSCOnlineMarks)
    quest = models.ForeignKey(SSCquestions)
    time = models.IntegerField()


class AnsweredQuestion(models.Model):
    onlineMarks = models.ForeignKey(OnlineMarks)
    quest = models.ForeignKey(Questions)
    time = models.IntegerField()

class SSCTemporaryQuestionsHolder(models.Model):
    quests = ArrayField(models.IntegerField())
    teacher = models.ForeignKey(Teacher)
    time = models.DateTimeField()

class TemporaryQuestionsHolder(models.Model):
    quests = ArrayField(models.IntegerField())
    teacher = models.ForeignKey(Teacher)

