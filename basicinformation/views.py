from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import Http404, HttpResponse
from random import randint
import numpy as np
import urllib.request
from more_itertools import unique_everseen
from django.contrib.auth.models import User, Group
from .models import Student, Teacher, Subject, School, klass
from django.utils import timezone
# from .marksprediction import predictionConvertion, readmarks, averageoftest, teacher_get_students_classwise
from .marksprediction import *


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
                print('%s teaches --'%sub.teacher,sub.name)
            #retrieve all marks from database
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
            # find the predicted marks
            hindipredhy = me.predictionConvertion(hindipredhy)
            mathspredhy = me.predictionConvertion(mathspredhy)
            englishpredhy = me.predictionConvertion(englishpredhy)
            sciencepredhy = me.predictionConvertion(sciencepredhy)
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
                       'science3': sciencet3, 'science4': sciencet4}
                       
            return render(request, 'basicinformation/student.html', context)

        elif user.groups.filter(name='Teachers').exists():
            me = Teach(user)
            profile = user.teacher
            klasses = me.my_classes_names()
            subjects = me.my_subjects_names()
            num_klasses = len(klasses)
            num_subjects = len(subjects)
            
            context = {'profile': profile,
                       'klasses':klasses,'subjects':subjects,'num_klasses':num_klasses,
                       'isTeacher':True,'num_subjects':num_subjects}
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
            analysis_types = ['School Tests Analysis','Online Test Analysis']
            context = {'analysisTypes':analysis_types}
            return render(request,'basicinformation/selfStudentAnalysis.html',context)


def student_subject_analysis(request):
    user = request.user
    if user.is_authenticated:
        me = Studs(user)
        if 'analysistype' in request.GET:
            ana_type = request.GET['analysistype']
            allSubjects = me.my_subjects_names()
            if ana_type == 'School':
                print('in school')
                allSubjects = me.my_subjects_names()
                context = {'subjects':allSubjects,'which_analysis':ana_type}
                return render(request,'basicinformation/studentAverageCurrent.html',context)
            elif ana_type == 'Online':
                context = {'subjects':allSubjects}
                return render(request,'basicinformation/studentAverageCurrent.html',context)


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
        context = {'subjects':subjects,'which_class':which_class}
        return \
    render(request,'basicinformation/teacher_school_analysis1.html',context)
    elif 'schoolSubject' in request.GET:
        schoolSubject = request.GET['schoolSubject']
        me = Teach(user)
        sub = schoolSubject.split(',')[0]
        which_class = schoolSubject.split(',')[1]
        marks_class_test1,marks_class_test2,marks_class_test3,marks_class_predictedHy=\
        me.listofStudentsMarks(which_class)
        if not marks_class_test1:
            noTest  = 'No Tests'
            context = {'noTest':noTest,'which_class':which_class}
            return \
        render(request,'basicinformation/teacher_school_analysis2.html',context)
        if not marks_class_test2:
            Tests = ['Test1']
            context ={'Tests':Tests,'which_class':which_class}
            return \
        render(request,'basicinformation/teacher_school_analysis2.html',context)

        if not marks_class_test3:
            Tests = ['Test1','Test2']
            context ={'Tests':Tests,'which_class':which_class}
            return \
        render(request,'basicinformation/teacher_school_analysis2.html',context)

        if marks_class_test3:
            Tests = ['Test1','Test2','Test3']
            context ={'Tests':Tests}
            return \
        render(request,'basicinformation/teacher_school_analysis2.html',context)
    elif 'schoolTestid' in request.GET:
        test_class = request.GET['schoolTestid']
        me = Teach(user)
        test = test_class.split(',')[0]
        which_class = test_class.split(',')[1]
        print(test,which_class)
        marks_class_test1,marks_class_test2,marks_class_test3,marks_class_predictedHy=\
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


    #elif urllib.request.unquote(str(ajKlass)) == urllib.request.unquote('9th a' + 'relativeaveragespredicted'):
    #    nine_a_test1, nine_b_test1, nine_a_test2, \
    #    nine_b_test2, nine_a_test3, nine_b_test3, \
    #    nine_a_predictedHy, nine_b_predictedHy = teacher_listofStudentsMarks(profile)
    #    t1 = find_grade_fromMark_predicted(nine_a_predictedHy)
    #    print(t1)
    #    print(nine_a_predictedHy)

    #    t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s = find_frequency_grades(t1)
    #    context ={'t1_fg_a': t1_fg_a, 't1_fg_b': t1_fg_b, 't1_fg_c': t1_fg_c,
    #               't1_fg_d': t1_fg_d,
    #               't1_fg_e': t1_fg_e, 't1_fg_f': t1_fg_f, 't1_fg_s': t1_fg_s}
    #    return render(request, 'basicinformation/teacher_relative_averages_predicted.html', context)
    #elif urllib.request.unquote(str(ajKlass)) == urllib.request.unquote('9th b' + 'relativeaveragespredicted'):
    #    nine_a_test1, nine_b_test1, nine_a_test2, \
    #    nine_b_test2, nine_a_test3, nine_b_test3, \
    #    nine_a_predictedHy, nine_b_predictedHy = teacher_listofStudentsMarks(profile)
    #    t1 = find_grade_fromMark_predicted(nine_b_predictedHy)
    #    print(t1)
    #    print(nine_b_predictedHy)

    #    t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s = find_frequency_grades(t1)
    #    context = {'t1_fg_a': t1_fg_a, 't1_fg_b': t1_fg_b, 't1_fg_c': t1_fg_c,
    #               't1_fg_d': t1_fg_d,
    #               't1_fg_e': t1_fg_e, 't1_fg_f': t1_fg_f, 't1_fg_s': t1_fg_s}
    #    return render(request, 'basicinformation/teacher_relative_averages_predicted.html', context)
    #else:
    #    listofstudents = teacher_listofStudents(profile,ajKlass)
    #    return render(request, 'basicinformation/teacher_update_page.html',
    #                      {'klass': listofstudents})


def create_student(num,request):
  user = request.user 
 
  for i in range(1, num):
      try:
          us = User.objects.create_user(username='student' + str(i),
                                                       email='studentss' + str(i) + '@gmail.com',
                                                       password='dnpandey')
          us.save()
          gr = Group.objects.get(name='Students')
          gr.user_set.add(us)
          cl = klass.objects.filter(school__name = 'First School')
          classes = []
          for cc in cl:
              classes.append(cc)
          for k in classes:
              stu = Student(studentuser=us, klass=np.random.choice(classes), rollNumber=int(str(i) + '00'), name='stu' + str(i),
                                       dob=timezone.now(), pincode=int(str(405060)))
              stu.save()
              sub = Subject(name='Maths', student=stu,teacher = user.teacher, test1
                            =randint(3,10),test2 = randint(3,9),test3=
                            randint(3,9))
              sub.save()
      except Exception as e:
        print(str(e))


def create_teacher(num):
    school1 = School.objects.filter(name = 'First School')
    school2 = School.objects.filter(name = 'Second School')
    for i in range( num):
         us = User.objects.create_user(username='teacher' + str(i),
                                       email='teacher' + str(i) + '@gmail.com',
                                       password='dnpandey')
         us.save()
         gr = Group.objects.get(name='Teachers')
         gr.user_set.add(us)
            
         teache = Teacher(teacheruser=us,
                          experience=randint(1,20),name=us.username,school =
                          school1)
         teache.save()
        
        

