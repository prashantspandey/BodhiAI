from django.shortcuts import render
from .models import Questions,Choices,KlassTest
from basicinformation.models import *
from basicinformation.marksprediction import *
import datetime
import os.path
from django.utils import timezone
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User,Group
import re
import pickle
import urllib.request
from more_itertools import unique_everseen
# Create your views here.

def home(request):
    question = Questions.objects.all()
    context = {'question':question}
    return render(request,'questions/home.html',context)

def create_test(request):
    user = request.user
    
    if user.is_authenticated:
        if user.groups.filter(name= 'Teachers').exists():
            quest_file_name = 'question_paper'+str(user.teacher)+'.pkl'
            questions = Questions.objects.all()
            me = Teach(user)
            school = me.my_school()
            all_klasses = me.my_classes_names()
            klass_reg = re.compile(r'^(.*?)th')
            try:
                if 'klass_test' in request.GET:
                    try:
                        if os.path.exists(quest_file_name):
                            os.remove(quest_file_name)
                    except:
                        pass

                    ttt = request.GET['klass_test']
                    klasses = klass.objects.filter(name=ttt)
                    klass_level = 'aa'
                    for kass in klasses:
                        klass_level = kass.level
                    quest = Questions.objects.filter(level = klass_level,school
                                                     =school)
                    if quest:
                        unique_chapters = []
                        for i in quest:
                            for j in i.chapCategory:
                                unique_chapters.append(j)
                        unique_chapters = list(unique_everseen(unique_chapters))
                        return render(request, 'questions/klass_available.html',
                                  {'fin':
                                   unique_chapters,'which_klass':ttt})
                    else:
                        noTest = 'Not Questions for this class'
                        context = {'noTest':noTest}
                        return
                    render(request,'questions/klass_available.html',context)
                if 'chapter_test' in request.GET:
                    quest_file_name = 'question_paper'+str(user.teacher)+'.pkl'
                    which_chap = request.GET['chapter_test']
                    splitChap = which_chap.split(",",1)[0]
                    splitClass = which_chap.split(",",1)[1]
                    klasses = klass.objects.filter(name=splitClass)
                    klass_level = 'aa'
                    for kass in klasses:
                        klass_level = kass.level
                    
                    if os.path.exists(quest_file_name):
                        with open(quest_file_name,'rb') as fi:
                            questions_list = pickle.load(fi)
                        idlist = []
                        for qq in questions_list:
                            idlist.append(qq.id)


                        klass_question = Questions.objects.filter(level =
                                                          klass_level,chapCategory=splitChap)
                        context = \
                        {'que':klass_question,'idlist':idlist,'which_class':splitClass }
                        return render(request,'questions/klass_questions.html',context)
                    else:
                        klass_question = Questions.objects.filter(level =
                                                          klass_level,chapCategory=splitChap)
                        context = \
                        {'que':klass_question,'which_class':splitClass }
                        return render(request,'questions/klass_questions.html',context)


            except Exception as e:
                print(str(e))

            context = {'questions':questions,'klasses':all_klasses}
            return render(request,'questions/createTest.html',context)
        else:
            raise Http404("You don't have necessary permissions.")
def add_questions(request):
    user = request.user
    quest_file_name = 'question_paper'+str(user.teacher)+'.pkl'
    if 'question_id' in request.GET:

        if os.path.exists(quest_file_name):
            with open(quest_file_name,'rb') as lql:
                questions_list = pickle.load(lql)
        else:
            questions_list = []
        question_id = request.GET['question_id']
        which_klass = question_id.split(',')[1]
        question_id = question_id.split(',')[0]
        
        questions_list.append(Questions.objects.get(id=question_id))
        questions_list = list(unique_everseen(questions_list))
        with open(quest_file_name,'wb') as ql:
            pickle.dump(questions_list,ql)
        total_marks = []
        for l in questions_list:
            total_marks.append(l.max_marks)
        total = 0
        for k in total_marks:
            total = total + k
        num_questions = len(total_marks)
        context = \
                {'questions':questions_list,'total_marks':total,'num_questions':num_questions,'which_klass':which_klass }
        return render(request,'questions/addedQuestions.html',context)
    if 'remove_id' in request.GET:
        if os.path.exists(quest_file_name):
            with open(quest_file_name,'rb') as rid:
                questions_list = pickle.load(rid)
        else:
            questions_list = []

        questions = []
        rem_id = request.GET['remove_id']
        which_klass = rem_id.split(',')[1]
        rem_id  = rem_id.split(',')[0]
        if rem_id == None:
            return HttpResponse('No questions in question paper')
        for tbr in questions_list:
            if not int(tbr.id) == int(rem_id):
                questions.append(tbr)
        total_marks = []
        questions_list = questions
        with open(quest_file_name,'wb') as ql:
            pickle.dump(questions_list,ql)
        for j in questions_list:
            total_marks.append(j.max_marks)
        total = 0
        for k in total_marks:
            total = total + k
        num_questions = len(total_marks)
        context = \
        {'questions':questions,'total_marks':total,'num_questions':num_questions
         }
        return render(request,'questions/addedQuestions.html',context)
    if request.POST:
        with open(quest_file_name,'rb') as ql:
            questions_list= pickle.load(ql)
        if len(questions_list)!=0:
            me = Teach(request.user)
            which_klass = request.POST['which_klass']
            klass = me.my_classes_objects(which_klass)
            tot = 0 
            for i in questions_list:
                tot = tot + i.max_marks
            newClassTest = KlassTest()
            newClassTest.max_marks = tot
            newClassTest.published = timezone.now()
            newClassTest.name = str(request.user.teacher) + str(timezone.now())
            newClassTest.klas = klass
            newClassTest.creator = request.user
            newClassTest.save()
            for zz in questions_list:
                zz.ktest.add(newClassTest)
            context = {'test':newClassTest}
            return render(request,'questions/publish_test.html',context)
def publish_test(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name= 'Teachers').exists():
            if 'publishTest' in request.POST:
                date = request.POST['dueDate']
                testid = request.POST['testid']
                myTest = KlassTest.objects.get(id = testid)
                kl = myTest.klas
                students = Student.objects.filter(klass = kl)
                for i in students:
                    myTest.testTakers.add(i)
                due_date = datetime.datetime.strptime(date, "%m/%d/%Y")
                myTest.due_date = due_date
                for sub in myTest.questions_set.all():
                    subject = sub.sub
                    break
                myTest.sub = subject
                myTest.save()
                return HttpResponse('nice')


def see_Test(request):
    user = request.user
    tests = KlassTest.objects.filter(creator = user)
    context = {'tests':tests}
    return render(request, 'questions/seeCreatedTest.html',context)

def student_my_tests(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name= 'Students').exists():
            me = Studs(user)
            subjects = me.my_subjects_names()
            context = {'subjects':subjects}
            return render(request,'questions/student_my_tests.html',context)


def student_show_onlineTests(request):
        if 'onlineTestSubject' in request.GET:
            my_sub = request.GET['onlineTestSubject']
            me = Studs(request.user)
            tests = me.OnlineTestsSubwise(my_sub)
            context = {'tests':tests}
            return render(request,'questions/student_onlinetests_subjectwise.html',context)
        if 'onlineTestid' in request.GET:
            me = Studs(request.user)
            testid = request.GET['onlineTestid']
            old_test = me.is_onlineTestTaken(testid)
            if old_test:
                context = {'marks':old_test}
                return render(request,'questions/student_evaluated_test.html',context)
            else:
                test = KlassTest.objects.get(id = testid)
                context = {'test':test}
                return render(request,'questions/student_OnlineTest.html',context)
        if request.POST:
            all_answers = []
            right_answers = []
            right_answers2 = []
            wrong_answers = []
            wrong_answers2 = []
            skipped_answers = []
            skipped_answers2 = []
            num_of_quests = 0
            testid = request.POST['submitTest']
            test = KlassTest.objects.get(id= testid)
            for j in test.questions_set.all():
                num_of_quests += 1
            for i in range(num_of_quests+1):
                #ans = eval("'ans'+str(i)")
                try:
                    answerChoice = eval("'answerChoice'+str(i)")
                    ans = request.POST[answerChoice]
                    all_answers.append(int(ans))
                except:
                    pass
            test_marks  = 0
            for qu in test.questions_set.all():
                for ch in qu.choices_set.all():
                    if not ch.id in all_answers:
                        skipped_answers.append(qu.id)
                    elif ch.id in all_answers and ch.predicament == "Correct":
                        right_answers.append(qu.id)
                        right_answers2.append(ch.id)
                        test_marks += int(qu.max_marks)
                    elif ch.id in all_answers and ch.predicament == "Wrong":
                        wrong_answers.append(qu.id)
                        wrong_answers2.append(ch.id)
            skipped_answers = list(unique_everseen(skipped_answers))
            for an in skipped_answers:
                if not an in right_answers and not an in wrong_answers:
                    skipped_answers2.append(an)
            my_marks = OnlineMarks()
            my_marks.test = test
            my_marks.student = request.user.student
            my_marks.rightAnswers = right_answers2
            my_marks.wrongAnswers = wrong_answers2
            my_marks.skippedAnswers = skipped_answers2
            my_marks.allAnswers = all_answers
            my_marks.marks = test_marks
            my_marks.testTaken = timezone.now()
            my_marks.save()
            context = {'marks':my_marks}
            return render(request,'questions/student_answered_paper.html',context)
            



