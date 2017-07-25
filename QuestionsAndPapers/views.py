from django.shortcuts import render
from .models import Questions,Choices,KlassTest
from basicinformation.models import klass
from basicinformation.marksprediction import *
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
            questions = Questions.objects.all()
            _,all_klasses = teacher_get_students_classwise(request)
            all_klasses = list(all_klasses)
            all_klasses = list(unique_everseen(all_klasses))
            klass_reg = re.compile(r'^(.*?)th')
            try:
                if 'klass_test' in request.GET:
                    #klasses = klass.objects.all()
                    ttt = request.GET['klass_test']
                    klasses = klass.objects.filter(name=ttt)
                    quest = Questions.objects.filter(kl= klasses)
                    unique_chapters = []
                    for i in quest:
                        for j in i.category:
                            unique_chapters.append(j)
                    unique_chapters = list(unique_everseen(unique_chapters))
                    return render(request, 'questions/klass_available.html',
                                  {'fin':
                                   unique_chapters,'which_klass':ttt})
                if 'chapter_test' in request.GET:
                    which_chap = request.GET['chapter_test']
                    print(which_chap)
                    splitChap = which_chap.split(",",1)[0]
                    splitClass = which_chap.split(",",1)[1]
                    klasses = klass.objects.filter(name=splitClass)
                    klass_question = Questions.objects.filter(kl=klasses,category=splitChap)
                    return render(request,'questions/klass_questions.html',{'que':klass_question})

            except Exception as e:
                print(str(e))

            context = {'questions':questions,'klasses':all_klasses}
            return render(request,'questions/createTest.html',context)
        else:
            raise Http404("You don't have necessary permissions.")
def add_questions(request):
    questions_list = []
    if 'question_id' in request.GET:
        questions = []
        ultimate_list = []
        question_id = request.GET['question_id']
        question_id = question_id.replace(',','')
        question_id = list(question_id)
        for i in question_id:
            questions.append(Questions.objects.get(id=i))
        total_marks = []
        for j in questions:
            questions_list.append(j)
        with open('questions_list.pkl','wb') as ql:
            pickle.dump(questions_list,ql)
        for l in questions_list:
            total_marks.append(l.max_marks)
        total = 0
        for k in total_marks:
            total = total + k
        num_questions = len(total_marks)
        context = {'questions':questions_list,'total_marks':total,'num_questions':num_questions}
        return render(request,'questions/addedQuestions.html',context)
    if 'remove_id' in request.GET:
        questions = []
        rem_id = request.GET['remove_id']
        if rem_id == None:
            return HttpResponse('No questions in question paper')
        rem_id = rem_id.replace(',','')
        for i in rem_id:
            questions.append(Questions.objects.get(pk=i))
        total_marks = []
        questions_list = questions
        with open('questions_list.pkl','wb') as ql:
            pickle.dump(questions_list,ql)
        for j in questions_list:
            total_marks.append(j.max_marks)
        total = 0
        for k in total_marks:
            total = total + k
        num_questions = len(total_marks)
        context = {'questions':questions,'total_marks':total,'num_questions':num_questions}
        return render(request,'questions/addedQuestions.html',context)
    if request.POST:
        with open('questions_list.pkl','rb') as ql:
            questions_list= pickle.load(ql)
        if len(questions_list)!=0:
            tot = 0 
            for i in questions_list:
                tot = tot + i.max_marks
            kl = questions_list[0].kl
            newClassTest = KlassTest()
            newClassTest.max_marks = tot
            newClassTest.published = timezone.now()
            newClassTest.name = 'New Test'
            newClassTest.klas = kl
            newClassTest.creator = request.user
            newClassTest.save()
            for zz in questions_list:
                zz.ktest.add(newClassTest)
            return HttpResponse('created')
def see_Test(request):
    user = request.user
    tests = KlassTest.objects.filter(creator = user)
    context = {'tests':tests}
    return render(request, 'questions/seeCreatedTest.html',context)



