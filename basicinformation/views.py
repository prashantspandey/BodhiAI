from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import Http404, HttpResponse
from random import randint
from datetime import timedelta
from datetime import date
import numpy as np
import urllib.request
from more_itertools import unique_everseen
from django.contrib.auth.models import User, Group
from .models import Student, Teacher, Subject, School, klass
from django.utils import timezone
# from .marksprediction import predictionConvertion, readmarks, averageoftest, teacher_get_students_classwise
from .marksprediction import *
from Private_Messages.models import *


def home(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Students').exists():
            profile = user.student
            me = Studs(request.user)
            subjects = user.student.subject_set.all()
            teacher_name = {}
            for sub in subjects:
                teacher_name[sub.name] = sub.teacher
            # retrieve all marks from database
            mathst1, mathst2, mathst3, mathshy, \
            mathst4, mathspredhy = [], [], [], [], [], []
            hindit1, hindit2, hindit3, hindihy, hindit4, \
            hindipredhy = [], [], [], [], [], []
            englisht1, englisht2, englisht3, englishhy, \
            englisht4, englishpredhy = [], [], [], [], [], []
            sciencet1, sciencet2, sciencet3, sciencehy, \
            sciencet4, sciencepredhy = [], [], [], [], [], []
            mathst1, mathst2, mathst3, mathshy, mathst4, mathspredhy, \
            hindit1, hindit2, hindit3, hindihy, hindit4, hindipredhy, \
            englisht1, englisht2, englisht3, englishhy, englisht4, englishpredhy, \
            sciencet1, sciencet2, sciencet3, sciencehy, sciencet4,
            sciencepredhy = me.readmarks()
            # check for announcements in past 48 hours
            startdate = date.today()
            enddate = startdate - timedelta(days=2)
            my_announcements = Announcement.objects.filter(listener =
                                                           profile,date__range=[enddate,startdate])

            # find the predicted marks
            #hindipredhy = me.predictionConvertion(hindipredhy)
            #mathspredhy = me.predictionConvertion(mathspredhy)
            #englishpredhy = me.predictionConvertion(englishpredhy)
            #sciencepredhy = me.predictionConvertion(sciencepredhy)
            hindipredhy = 0
            mathspredhy = 0
            englishpredhy = 0
            sciencepredhy = 0
            # sending all values to template

            context = {'profile': profile, 'subjects': subjects,
                       'hindihy_prediction': hindipredhy,
                       'mathshy_prediction': mathspredhy,
                       'englishhy_prediction': englishpredhy,
                       'sciencehy_prediction': sciencepredhy,
                       'maths1': mathst1, 'maths2': mathst2, 'maths3': mathst3,
                       'maths4': mathst4, 'hindi1': hindit1, 'hindi2': hindit2,
                       'hindi3': hindit3, 'hindi4': hindit4, 'english1': englisht1,
                       'english2': englisht2, 'english3': englisht3, 'english4': englisht4,
                       'science1': sciencet1, 'science2': sciencet2,
                       'science3': sciencet3, 'science4':
                       sciencet4,'announcements':my_announcements}

            return render(request, 'basicinformation/student.html', context)

        elif user.groups.filter(name='Teachers').exists():
            me = Teach(user)
            profile = user.teacher
            klasses = me.my_classes_names()
            subjects = me.my_subjects_names()
            num_klasses = len(klasses)
            num_subjects = len(subjects)

            context = {'profile': profile,
                       'klasses': klasses, 'subjects': subjects, 'num_klasses': num_klasses,
                       'isTeacher': True, 'num_subjects': num_subjects}
            return render(request, 'basicinformation/teacher1.html', context)
        else:

            return render(request, 'basicinformation/home.html')
    else:
        return HttpResponseRedirect(reverse('membership:login'))


def student_self_analysis(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Teachers').exists():
            raise Http404(" This page is only meant for student to see.")
        elif user.groups.filter(name='Students').exists():
            me = Studs(user)
            allSubjects = me.my_subjects_names()
            analysis_types = ['School Tests Analysis', 'Online Test Analysis']
            context = {'subjects': allSubjects}
            return render(request, 'basicinformation/selfStudentAnalysis.html', context)


def student_subject_analysis(request):
    user = request.user
    if user.is_authenticated:
        if 'studentwhichsub' in request.GET:
            which_sub = request.GET['studentwhichsub']
            ana_type = ['School Tests', 'Online Tests']
            context = {'anatype': ana_type, 'sub': which_sub}
            return \
                render(request, 'basicinformation/student_analysis_subjects.html', context)
        if 'studentwhichana' in request.GET:
            which_one = request.GET['studentwhichana']
            subject = which_one
            tests = OnlineMarks.objects.filter(test__sub=subject, student=user.student)
            context = {'tests': tests}
            return \
                render(request, 'basicinformation/student_self_sub_tests.html', context)
        if 'studentTestid' in request.GET:
            me = Studs(user)
            test_id = request.GET['studentTestid']
            test = OnlineMarks.objects.get(student=user.student, test__id=test_id)
            my_marks_percent = (test.marks / test.test.max_marks) * 100
            average, percent_average = \
                me.online_findAverageofTest(test_id, percent='p')
            percentile, all_marks = me.online_findPercentile(test_id)
            all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]
            freq = me.online_QuestionPercentage(test_id)
            context = \
                {'test': test, 'average': average, 'percentAverage': percent_average,
                 'my_percent': my_marks_percent, 'percentile': percentile, 'allMarks': all_marks,
                 'freq': freq}
            return \
                render(request, 'basicinformation/student_analyze_test.html', context)


def current_analysis(request, grade):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Students').exists():
            raise Http404("You don't have the permissions to view this page.")
        elif user.groups.filter(name='Teachers').exists():

            klass_dict, all_klasses = teacher_get_students_classwise(request)

            klass_test1_dict, klass_test2_dict, klass_test3_dict = teacher_get_testmarks_classwise(request, klass_dict)
            # find out the average of class tests (all the classes separated by commas)

            av1 = []  # list to hold the averages of test1
            av2 = []
            av3 = []
            for i in klass_test1_dict.values():
                av_test1 = averageoftest(i)
                av1.append(av_test1)

            for i in klass_test2_dict.values():
                av_test2 = averageoftest(i)
                av2.append(av_test2)

            for i in klass_test3_dict.values():
                av_test3 = averageoftest(i)
                av3.append(av_test3)

            context = {'avtest1': av1, 'avtest2': av2, 'avtest3': av3, 'klass_dict': klass_dict}

            return render(request, 'basicinformation/analysis_current.html',
                          context)
    else:
        raise Http404("You don't have the permissions to view this page.")


def teacher_home_page(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Teachers').exists():
            profile = user.teacher
            klass_dict, all_klasses = teacher_get_students_classwise(request)
            all_klasses = list(unique_everseen(all_klasses))
            context = {'profile': profile, 'klasses': all_klasses}
            return render(request, 'basicinformation/teacherHomePage.html', context)
        else:
            raise Http404("You don't have the permissions to view this page.")
    else:
        raise Http404("You don't have the permissions to view this page.")


def teacher_update_page(request):
    user = request.user
    profile = user.teacher
    klass_dict, all_klasses = teacher_get_students_classwise(request)
    if 'ajKlass' in request.GET:
        which_class = request.GET['ajKlass']
        return HttpResponse('nice')

    elif 'schoolTestAnalysis' in request.GET:
        which_klass = request.GET['schoolTestAnalysis']
        me = Teach(user)
        which_class = which_klass.split(',')[0]
        subjects = me.my_subjects_names()
        context = {'subjects': subjects, 'which_class': which_class}
        return \
            render(request, 'basicinformation/teacher_school_analysis1.html', context)
    elif 'schoolSubject' in request.GET:
        schoolSubject = request.GET['schoolSubject']
        me = Teach(user)
        sub = schoolSubject.split(',')[0]
        which_class = schoolSubject.split(',')[1]
        marks_class_test1, marks_class_test2, marks_class_test3, marks_class_predictedHy = \
            me.listofStudentsMarks(which_class)
        if not marks_class_test1:
            noTest = 'No Tests'
            context = {'noTest': noTest, 'which_class': which_class}
            return \
                render(request, 'basicinformation/teacher_school_analysis2.html', context)
        if not marks_class_test2:
            Tests = ['Test1']
            context = {'Tests': Tests, 'which_class': which_class}
            return \
                render(request, 'basicinformation/teacher_school_analysis2.html', context)

        if not marks_class_test3:
            Tests = ['Test1', 'Test2']
            context = {'Tests': Tests, 'which_class': which_class}
            return \
                render(request, 'basicinformation/teacher_school_analysis2.html', context)

        if marks_class_test3:
            Tests = ['Test1', 'Test2', 'Test3']
            context = {'Tests': Tests}
            return \
                render(request, 'basicinformation/teacher_school_analysis2.html', context)
    elif 'schoolTestid' in request.GET:
        test_class = request.GET['schoolTestid']
        me = Teach(user)
        test = test_class.split(',')[0]
        which_class = test_class.split(',')[1]
        marks_class_test1, marks_class_test2, marks_class_test3, marks_class_predictedHy = \
            me.listofStudentsMarks(which_class)

        if test == 'Test1':
            context = me.school_test_analysis(marks_class_test1)
            return render(request,
                          'basicinformation/teacher_school_analysis3.html', context)
        elif test == 'Test2':
            context = me.school_test_analysis(marks_class_test2)
            return render(request,
                          'basicinformation/teacher_school_analysis3.html', context)
        elif test == 'Test3':
            context = me.school_test_analysis(marks_class_test3)
            return render(request,
                          'basicinformation/teacher_school_analysis3.html', context)
    elif 'onlineTestAnalysis' in request.GET:
        which_klass = request.GET['onlineTestAnalysis']
        me = Teach(user)
        which_class = which_klass.split(',')[0]
        subjects = me.my_subjects_names()
        context = {'subs': subjects, 'which_class': which_class}
        return \
            render(request, 'basicinformation/teacher_online_analysis.html', context)
    elif 'onlineschoolSubject' in request.GET:
        onlineSubject = request.GET['onlineschoolSubject']
        sub = onlineSubject.split(',')[0]
        which_class = onlineSubject.split(',')[1]
        online_tests = KlassTest.objects.filter(creator=
                                                user, klas__name=which_class, sub=
                                                sub)
        context = {'tests': online_tests}
        return render(request, 'basicinformation/teacher_online_analysis2.html', context)
    elif 'onlinetestid' in request.GET:
        test_id = request.GET['onlinetestid']
        me = Teach(user)
        online_marks = OnlineMarks.objects.filter(test__id=test_id)
        test = KlassTest.objects.get(id = test_id)
        max_marks = 0
        for i in online_marks:
            max_marks = i.test.max_marks
        average,percent_average =\
        me.online_findAverageofTest(test_id,percent='p')
        grade_s,grade_a,grade_b,grade_c,grade_d,grade_e,grade_f= \
        me.online_freqeucyGrades(test_id)
        freq = me.online_QuestionPercentage(test_id)
        sq = me.online_skippedQuestions(test_id)
        context = {'om': online_marks,'test':test,'average':average
                   ,'percentAverage':percent_average,'maxMarks':max_marks,
                   'grade_s':grade_s,'grade_a':grade_a,'grade_b':grade_b,'grade_c':grade_c,
                   'grade_d':grade_d,'grade_e':grade_e,'grade_f':grade_f,
                   'freq':freq,'sq':sq}
        return render(request, 'basicinformation/teacher_online_analysis3.html', context)



