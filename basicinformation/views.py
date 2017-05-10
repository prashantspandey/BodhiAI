from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import Http404, HttpResponse
import urllib.request
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
            subjects = user.student.subject_set.all()

            # retrieve all marks from database
            mathst1, mathst2, mathst3, mathshy, mathst4, mathspredhy, \
            hindit1, hindit2, hindit3, hindihy, hindit4, hindipredhy, \
            englisht1, englisht2, englisht3, englishhy, englisht4, englishpredhy, \
            sciencet1, sciencet2, sciencet3, sciencehy, sciencet4, sciencepredhy = readmarks(
                user)
            hindipredhy = predictionConvertion(hindipredhy)
            mathspredhy = predictionConvertion(mathspredhy)
            englishpredhy = predictionConvertion(englishpredhy)
            sciencepredhy = predictionConvertion(sciencepredhy)

            context = {'profile': profile, 'subjects': subjects,
                       'hindihy_prediction': hindipredhy,
                       'mathshy_prediction': mathspredhy,
                       'englishhy_prediction': englishpredhy,
                       'sciencehy_prediction': sciencepredhy,
                       'maths1': mathst1, 'maths2': mathst2, 'maths3': mathst3,
                       'maths4': mathst4, 'hindi1': hindit1, 'hindi2': hindit2,
                       'hindi3': hindit3, 'hindi4': hindit4, 'english1': englisht1,
                       'english2': englisht2, 'english3': englisht3, 'english4': englisht4,
                       'science1': sciencet1, 'science2': sciencet2, 'science3': sciencet3, 'science4': sciencet4}
            return render(request, 'basicinformation/student.html', context)

        elif user.groups.filter(name='Teachers').exists():
            profile = user.teacher

            subject = profile.subject_set.all()
            allstudents = []
            for i in subject:
                allstudents.append(i)

            st = []
            for stu in allstudents:
                st.append(stu.test1)

            context = {'profile': profile, 'allstudents': allstudents,
                       'stu': st}

            return render(request, 'basicinformation/teacher.html', context)
        else:

            return render(request, 'basicinformation/home.html')

    else:
        return HttpResponseRedirect(reverse('membership:login'))


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

            nine_a_test1, nine_b_test1, nine_a_test2, \
            nine_b_test2, nine_a_test3, nine_b_test3 = teacher_listofStudentsMarks(profile)

            klass_dict, all_klasses = teacher_get_students_classwise(request)
            context = {'profile': profile, 'klasses': all_klasses}
            return render(request, 'basicinformation/teacherHomePage.html', context)
        else:
            raise Http404("You don't have the permissions to view this page.")
    else:
        raise Http404("You don't have the permissions to view this page.")


def teacher_update_page(request):
    user = request.user
    profile = user.teacher
    nine_a, nine_b = teacher_listofStudents(profile)
    klass_dict, all_klasses = teacher_get_students_classwise(request)

    if request.GET:
        ajKlass = request.GET['ajKlass']

        if urllib.request.unquote(str(ajKlass)) == urllib.request.unquote('9th a'):

            return render(request, 'basicinformation/teacher_update_page.html', {'klass': nine_a})
        elif urllib.request.unquote(str(ajKlass)) == urllib.request.unquote('9th b'):

            return render(request, 'basicinformation/teacher_update_page.html', {'klass': nine_b})
        elif urllib.request.unquote(str(ajKlass)) == urllib.request.unquote('9th b' + 'relativeaveragescurrent'):

            nine_a_test1, nine_b_test1, nine_a_test2, \
            nine_b_test2, nine_a_test3, nine_b_test3 = teacher_listofStudentsMarks(profile)
            nine_b_average_test1, nine_b_average_test2, nine_b_average_test3 = averageoftest(nine_b_test1, nine_b_test2,
                                                                                             nine_b_test3)

            t1, t2, t3 = find_grade_from_marks(nine_b_test1, nine_b_test2, nine_b_test3)
            t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
            t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s, \
            t3_fg_a, t3_fg_b, t3_fg_c, t3_fg_d, t3_fg_e, t3_fg_f, t3_fg_s = find_frequency_grades(t1, t2, t3)

            context = {'test1av': nine_b_average_test1, 'test2av': nine_b_average_test2,
                       'test3av': nine_b_average_test3, 't1_fg_a': t1_fg_a, 't1_fg_b': t1_fg_b, 't1_fg_c': t1_fg_c,
                       't1_fg_d': t1_fg_d,
                       't1_fg_e': t1_fg_e, 't1_fg_f': t1_fg_f, 't1_fg_s': t1_fg_s, 't2_fg_a': t2_fg_a,
                       't2_fg_b': t2_fg_b,
                       't2_fg_c': t2_fg_c, 't2_fg_d': t2_fg_d, 't2_fg_e': t2_fg_e, 't2_fg_f': t2_fg_f,
                       't2_fg_s': t2_fg_s,
                       't3_fg_a': t3_fg_a, 't3_fg_b': t3_fg_b, 't3_fg_c': t2_fg_c, 't3_fg_d': t3_fg_d,
                       't3_fg_e': t3_fg_e, 't3_fg_f': t3_fg_f, 't3_fg_s': t3_fg_s}
            return render(request, 'basicinformation/teacher_relative_averages_current.html', context)
        elif urllib.request.unquote(str(ajKlass)) == urllib.request.unquote('9th a' + 'relativeaveragescurrent'):

            nine_a_test1, nine_b_test1, nine_a_test2, \
            nine_b_test2, nine_a_test3, nine_b_test3 = teacher_listofStudentsMarks(profile)
            nine_a_average_test1, nine_a_average_test2, nine_a_average_test3 = averageoftest(nine_a_test1, nine_a_test2,
                                                                                             nine_a_test3)

            t1, t2, t3 = find_grade_from_marks(nine_a_test1, nine_a_test2, nine_a_test3)
            t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
            t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s, \
            t3_fg_a, t3_fg_b, t3_fg_c, t3_fg_d, t3_fg_e, t3_fg_f, t3_fg_s = find_frequency_grades(t1, t2, t3)

            context = {'test1av': nine_a_average_test1, 'test2av': nine_a_average_test2,
                       'test3av': nine_a_average_test3, 't1_fg_a': t1_fg_a, 't1_fg_b': t1_fg_b, 't1_fg_c': t1_fg_c,
                       't1_fg_d': t1_fg_d,
                       't1_fg_e': t1_fg_e, 't1_fg_f': t1_fg_f, 't1_fg_s': t1_fg_s, 't2_fg_a': t2_fg_a,
                       't2_fg_b': t2_fg_b,
                       't2_fg_c': t2_fg_c, 't2_fg_d': t2_fg_d, 't2_fg_e': t2_fg_e, 't2_fg_f': t2_fg_f,
                       't2_fg_s': t2_fg_s,
                       't3_fg_a': t3_fg_a, 't3_fg_b': t3_fg_b, 't3_fg_c': t2_fg_c, 't3_fg_d': t3_fg_d,
                       't3_fg_e': t3_fg_e, 't3_fg_f': t3_fg_f, 't3_fg_s': t3_fg_s}
            return render(request, 'basicinformation/teacher_relative_averages_current.html', context)
 # def create_student(num):
 #
 #
 #     for i in range(10, num):
 #
 #         us = User.objects.create_user(username='student' + str(i),
 #                                                      email='studentss' + str(i) + '@gmail.com',
 #                                                      password='dnpandey')
 #         us.save()
 #         gr = Group.objects.get(name='Students')
 #         gr.user_set.add(us)
 #         cl = klass.objects.all()
 #         classes = []
 #         for k in cl:
 #
 #             classes.append(k)
 #             stu = Student(studentuser=us, klass=classes[0], rollNumber=int(str(i) + '00'), name='stu' + str(i),
 #                                      dob=timezone.now(), pincode=int(str(405060)))
 #             stu.save()
 #             sub = Subject(name='Science', student=stu)
 #             sub.save()