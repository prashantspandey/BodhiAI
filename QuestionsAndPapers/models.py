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
        (('General-Intelligence','General-Intelligence'),('General-Knowledge','General-Knowledge')
         ,('Quantitative-Analysis','Quantitative-Analysis'),('English','English'),('Defence-English','Defence-English'),
        ('Defence-Physics','Defence-Physics'),('GroupX-Maths','GroupX-Maths'),('Defence-GK-CA','Defence-GK-CA'),
        ('SSCMultipleSections','SSCMultipleSections'),('Defence-MultipleSubjects','Defence-MultipleSubjects'))
    course_choices = (('SSC','SSC'),('Railways','Railways'))

    #max_marks = models.DecimalField(max_digits=4,decimal_places=2)
    max_marks = models.IntegerField()
    testTakers = models.ManyToManyField(Student)
    published = models.DateField(auto_now_add= True)
    klas = models.ForeignKey(klass,null=True,blank=True)
    patternTestBatches = models.ManyToManyField(klass,related_name =
                                                'patternBatches',null=True,blank=True)
    patternTestCreators = models.ManyToManyField(Teacher)
    creator = models.ForeignKey(User,null=True,blank=True)
    sub = models.CharField(max_length=70,choices = subject_choices)
    due_date = models.DateField(null=True,blank=True)
    mode = models.CharField(max_length=20,choices = mode_choices)
    totalTime = models.IntegerField(blank=True,null=True)
    course =\
    models.CharField(max_length=20,choices=course_choices,default='SSC')
    pattern_test = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class TestDetails(models.Model):
    test = models.ForeignKey(SSCKlassTest)
    num_questions = models.IntegerField()
    questions = ArrayField(models.IntegerField())

    def __str__(self):
        return str(self.test.id) + str(self.num_questions)

class Comprehension(models.Model):
    text = models.TextField()
    picture = models.URLField(max_length=500,null=True,blank=True)

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
    source = models.CharField(max_length= 50,null=True,blank=True)
    dateInserted = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.text[:50]



class SSCquestions(models.Model):
    ch = 1 
    tp = 1 
    topic_choice = []
    topic_choice2 = []
    for ch in range(1,70):
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
    usedFor_choices =\
    (('SSC','SSC'),('Aptitude','Aptitude'),('Groupx','Groupx'),('Groupy','Groupy'),('RPSC','RPSC'),('RAS','RAS'))
    language_choices = (('English','English'),('Hindi','Hindi'),('Bi','Bi'))
    section_choices = \
        (('General-Intelligence','General-Intelligence'),('General-Knowledge','General-Knowledge')
         ,('Quantitative-Analysis','Quantitative-Analysis'),('English','English'),('Defence-English','Defence-English'),
        ('Defence-Physics','Defence-Physics'),('GroupX-Maths','GroupX-Maths'),('Defence-GK-CA','Defence-GK-CA'))
    diffculty_choices = (('easy','easy'),('medium','medium'),('hard','hard'))
    text = models.TextField(blank=True,null=True)
    tier_category = models.CharField(max_length=20,choices = tier_choices)
    section_category  = models.CharField(max_length=70,choices = section_choices)
    diffculty_category = models.CharField(max_length = 10,choices =
                                          diffculty_choices,null=True,blank=True)
    topic_category = models.CharField(max_length=5,choices = topic_choice)
    school = models.ManyToManyField(School)
    picture = models.URLField(max_length=500,null=True,blank=True)
    usedFor = models.CharField(max_length=30,choices=
                              usedFor_choices,null=True,blank=True)
    source = models.CharField(max_length= 50,null=True,blank=True)
    dateInserted = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    language = models.CharField(max_length = 20,choices =
                                language_choices,null=True,blank=True )



class GeneralDifficulty(models.Model):
    average_difficulty = models.FloatField()
    skipped_ratio = models.FloatField()
    quest = models.ForeignKey(SSCquestions)

    def __str__(self):
        return str(self.average_difficulty)



class InstituteQuestionDifficulty(models.Model):
    average_difficulty = models.FloatField()
    skipped_ratio = models.FloatField()
    institute = models.ForeignKey(School)
    quest = models.ForeignKey(SSCquestions)

    def __str__(self):
        return str(self.institute)+','+str(self.average_difficulty)


class TimesUsed(models.Model):
    numUsed = models.IntegerField()
    teacher = models.ForeignKey(Teacher)
    quest = models.ForeignKey(SSCquestions)
    batch = models.ForeignKey(klass,null=True,blank=True)

    def __str__(self):
        name = str(self.batch) + str(self.teacher.name) + str(self.numUsed)
        return name

class TimesReported(models.Model):
    isReported = models.BooleanField()
    teacher = models.ForeignKey(Teacher)
    quest = models.ForeignKey(SSCquestions)

    def __str__(self):
        name = str(self.quest)+ str(self.teacher.name) + str(self.numReported)
        return name


class Choices(models.Model):
    class Meta:
        ordering = ['pk']
    res_choice = (('Correct','Correct'),('Wrong','Wrong'),('Not decided','Not decided'))
    predicament = models.CharField(max_length= 30, choices = res_choice)    
    quest = models.ForeignKey(Questions,blank=True,null=True)
    sscquest = models.ForeignKey(SSCquestions,blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    picture = models.URLField(null=True,blank=True)
    explanation = models.TextField(null=True,blank=True)
    explanationPicture= models.URLField(null=True,blank=True)
    def __str__(self):
        if self.text != None:
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

class SSCOfflineMarks(models.Model):
    test = models.ForeignKey(SSCKlassTest)
    student = models.ForeignKey(Student)
    rightAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    wrongAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    allAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    skippedAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    marks = models.DecimalField(max_digits=4,decimal_places=2)
    testTaken = models.DateField()
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


class TemporaryOneClickTestHolder(models.Model):
    quests = ArrayField(models.IntegerField())
    teacher = models.ForeignKey(Teacher)

class SscTeacherTestResultLoader(models.Model):
    test = models.ForeignKey(SSCKlassTest)
    teacher = models.ForeignKey(Teacher)
    onlineMarks = models.ManyToManyField(SSCOnlineMarks)
    average = models.FloatField()
    percentAverage = models.FloatField()
    grade_a = models.IntegerField(default = 0)
    grade_b = models.IntegerField(default = 0)
    grade_c = models.IntegerField(default = 0)
    grade_d = models.IntegerField(default = 0)
    grade_e = models.IntegerField(default = 0)
    grade_f = models.IntegerField(default = 0)
    grade_s = models.IntegerField(default = 0)
    skipped  = ArrayField(models.IntegerField())
    skippedFreq = ArrayField(models.IntegerField())
    problemQuestions = ArrayField(models.IntegerField())
    problemQuestionsFreq = ArrayField(models.IntegerField())
    freqAnswersQuestions = ArrayField(models.IntegerField())
    freqAnswersFreq = ArrayField(models.IntegerField())


    def __str__(self):
        return str(self.test.id)

class SscStudentWeakAreaLoader(models.Model):
    subject_choices = \
        (('General-Intelligence','General-Intelligence'),('General-Knowledge','General-Knowledge')
         ,('Quantitative-Analysis','Quantitative-Analysis'),('English','English'),
        ('SSCMultipleSections','SSCMultipleSections'))

    student = models.ForeignKey(Student)
    subject = models.CharField(max_length = 70,choices = subject_choices)
    lenonlineSingleSub = models.IntegerField(null=True)
    lenonlineMultipleSub = models.IntegerField(null=True)
    lenofflineSingleSub = models.IntegerField(null=True)
    lenofflineMultipleSub = models.IntegerField(null=True)
    topics = ArrayField(models.FloatField())
    weakTopicsPercentage = ArrayField(models.FloatField())
    timingTopics = ArrayField(models.FloatField())
    weakTiming = ArrayField(models.FloatField())
    weakTimingFreq = ArrayField(models.IntegerField())


    def __str__(self):
        return str(self.student) + str(self.weakTopics)

class StudentCurrentTest(models.Model):
    student = models.ForeignKey(Student)
    test = models.ForeignKey(SSCKlassTest)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.student) + str(self.test.id)

class TestRankTable(models.Model):
    teacher = models.ForeignKey(Teacher,null=True)
    test = models.ForeignKey(SSCKlassTest,null=True)
    names = ArrayField(models.CharField(max_length=100))
    totalMarks = ArrayField(models.IntegerField(null=True))
    scores = ArrayField(models.FloatField(null=True))
    percentage = ArrayField(models.FloatField(null=True))
    numCorrect = ArrayField(models.IntegerField(null=True))
    numIncorrect = ArrayField(models.IntegerField(null=True))
    numSkipped = ArrayField(models.IntegerField(null=True))
    rank = ArrayField(models.IntegerField(null=True,blank = True))
    time = models.DateTimeField(auto_now = True,null=True)

    def __str__(self):
        return str(self.teacher)+str(self.test.published)
