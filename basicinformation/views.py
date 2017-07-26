from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import Http404, HttpResponse
from random import randint
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
<<<<<<< HEAD
            me = Studs(request.user)
=======
>>>>>>> 5320e0a2f8de669ff202dc1b9767d4f6dc29e083
            subjects = user.student.subject_set.all()
            teacher_name = {}
            for sub in subjects:
                teacher_name[sub.name] = sub.teacher
                print('%s teaches --'%sub.teacher,sub.name)
<<<<<<< HEAD
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
=======
            # retrieve all marks from database
            mathst1, mathst2, mathst3, mathshy, mathst4, mathspredhy, \
            hindit1, hindit2, hindit3, hindihy, hindit4, hindipredhy, \
            englisht1, englisht2, englisht3, englishhy, englisht4, englishpredhy, \
            sciencet1, sciencet2, sciencet3, sciencehy, sciencet4, sciencepredhy = readmarks(
                user)
            print(mathst1,sciencet1)
            hindipredhy = predictionConvertion(hindipredhy)
            mathspredhy = predictionConvertion(mathspredhy)
            englishpredhy = predictionConvertion(englishpredhy)
            sciencepredhy = predictionConvertion(sciencepredhy)

>>>>>>> 5320e0a2f8de669ff202dc1b9767d4f6dc29e083
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
<<<<<<< HEAD
            me = Teach(user)
            profile = user.teacher
=======
            profile = user.teacher
            #create_student(50,request)
>>>>>>> 5320e0a2f8de669ff202dc1b9767d4f6dc29e083
            subject = profile.subject_set.all()
            allstudents = []
            for i in subject:
                allstudents.append(i)
            st = []
<<<<<<< HEAD
=======
            #for stu in allstudents:
            #    if stu.test1:
            #        st.append(stu.test1)
            #    if stu.test2:
            #        st.append(stu.test2)
            #    if stu.test1:
            #        st.append(stu.test3)
            #    if stu.testhy:
            #        st.append(stu.testhy)

>>>>>>> 5320e0a2f8de669ff202dc1b9767d4f6dc29e083


            context = {'profile': profile, 'allstudents': allstudents,
                       'isTeacher':True}
            return render(request, 'basicinformation/teacher.html', context)
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
<<<<<<< HEAD
            me = Studs(user)
            allSubjects = me.my_subjects_objects()
=======
            profile = user.student
            subjects = profile.subject_set.all()
            allSubjects = []
            for i in subjects:
                allSubjects.append(i)
>>>>>>> 5320e0a2f8de669ff202dc1b9767d4f6dc29e083
            context = {'allSubjects':allSubjects}
            return render(request,'basicinformation/selfStudentAnalysis.html',context)
def student_subject_analysis(request):
    user = request.user
    if user.is_authenticated:
        if 'subject_name' in request.GET:
            subject_name = request.GET['subject_name']
            subject = user.student.subject_set.get(name=subject_name)
            test1 = subject.test1
            context = {'test1_marks':test1}
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

    if request.GET:
        ajKlass = request.GET['ajKlass']
        
        if 'relativeaveragescurrent' in urllib.request.unquote(str(ajKlass)):
            which_class = ajKlass.split('relativeaveragescurrent')[0]
            print(which_class)
            marks_class_test1,marks_class_test2,marks_class_test3,marks_class_predictedHy=\
            teacher_listofStudentsMarks(profile,which_class)
            if len(marks_class_test1)==0:
                Notest = 'No Tests taken'
                context = {'notest':Notest}
                return render(request, 'basicinformation/teacher_relative_averages_current.html', context)
                
            elif len(marks_class_test2) ==0:
                averages = []
                average_test1 = averageoftest(marks_class_test1)
                g1 = find_grade_from_marks(marks_class_test1)
                t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s=\
                find_frequency_grades(g1)
                averages.append(average_test1)
                context =\
                {'test1av':average_test1,'t1_fg_a':t1_fg_a,'t1_fg_b':t1_fg_b,
                 't1_fg_c':t1_fg_c,'t1_fg_d':t1_fg_d,'t1_fg_e':t1_fg_e,'t1_fg_f':t1_fg_f,
                 't1_fg_s':t1_fg_s,'averages':averages}
                
                return render(request, 'basicinformation/teacher_relative_averages_current.html', context)
            elif len(marks_class_test3) == 0:
                averages = []
                average_test1,average_test2 = \
                averageoftest(marks_class_test1,marks_class_test2)
                g1, g2 =\
                find_grade_from_marks(marks_class_test1,marks_class_test2)
                t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
                t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f,\
                t2_fg_s,=find_frequency_grades(g1,g2)
                averages.append(average_test1)
                averages.append(average_test2)

                last = [1,2]
                context =\
                {'test1av':average_test1,'test2av':average_test2,'t1_fg_a':t1_fg_a,'t1_fg_b':t1_fg_b,
                 't1_fg_c':t1_fg_c,'t1_fg_d':t1_fg_d,'t1_fg_e':t1_fg_e,'t1_fg_f':t1_fg_f,
                 't1_fg_s':t1_fg_s,'t2_fg_a':t2_fg_a,'t2_fg_b':t2_fg_b,'t2_fg_c':t2_fg_c,
                 't2_fg_d':t2_fg_d,'t2_fg_e':t2_fg_e,'t2_fg_f':t2_fg_f,'t2_fg_s':t2_fg_s,'averages':averages}
                return render(request, 'basicinformation/teacher_relative_averages_current.html', context)

            else:
                averages = []
                average_test1,average_test2,average_test3 =\
                averageoftest(marks_class_test1,marks_class_test2,marks_class_test3)
                g1, g2, g3 = find_grade_from_marks(marks_class_test1,
                                               marks_class_test2,
                                               marks_class_test3)
                t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
                t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s, \
                t3_fg_a, t3_fg_b, t3_fg_c, t3_fg_d, t3_fg_e, t3_fg_f, t3_fg_s =\
                find_frequency_grades(g1, g2, g3)
                averages.append(average_test1)
                averages.append(average_test2)
                averages.append(average_test3)
                
                context = {'test1av': average_test1, 'test2av': average_test2,
                       'test3av': average_test3, 't1_fg_a': t1_fg_a, 't1_fg_b': t1_fg_b, 't1_fg_c': t1_fg_c,
                       't1_fg_d': t1_fg_d,
                       't1_fg_e': t1_fg_e, 't1_fg_f': t1_fg_f, 't1_fg_s': t1_fg_s, 't2_fg_a': t2_fg_a,
                       't2_fg_b': t2_fg_b,
                       't2_fg_c': t2_fg_c, 't2_fg_d': t2_fg_d, 't2_fg_e': t2_fg_e, 't2_fg_f': t2_fg_f,
                       't2_fg_s': t2_fg_s,
                       't3_fg_a': t3_fg_a, 't3_fg_b': t3_fg_b, 't3_fg_c': t2_fg_c, 't3_fg_d': t3_fg_d,
                       't3_fg_e': t3_fg_e, 't3_fg_f': t3_fg_f, 't3_fg_s':
                           t3_fg_s,'averages':averages}
                return render(request, 'basicinformation/teacher_relative_averages_current.html', context)
        elif urllib.request.unquote(str(ajKlass)) == urllib.request.unquote('9th a' + 'relativeaveragespredicted'):
            nine_a_test1, nine_b_test1, nine_a_test2, \
            nine_b_test2, nine_a_test3, nine_b_test3, \
            nine_a_predictedHy, nine_b_predictedHy = teacher_listofStudentsMarks(profile)
            t1 = find_grade_fromMark_predicted(nine_a_predictedHy)
            print(t1)
            print(nine_a_predictedHy)

            t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s = find_frequency_grades(t1)
            context ={'t1_fg_a': t1_fg_a, 't1_fg_b': t1_fg_b, 't1_fg_c': t1_fg_c,
                       't1_fg_d': t1_fg_d,
                       't1_fg_e': t1_fg_e, 't1_fg_f': t1_fg_f, 't1_fg_s': t1_fg_s}
            return render(request, 'basicinformation/teacher_relative_averages_predicted.html', context)
        elif urllib.request.unquote(str(ajKlass)) == urllib.request.unquote('9th b' + 'relativeaveragespredicted'):
            nine_a_test1, nine_b_test1, nine_a_test2, \
            nine_b_test2, nine_a_test3, nine_b_test3, \
            nine_a_predictedHy, nine_b_predictedHy = teacher_listofStudentsMarks(profile)
            t1 = find_grade_fromMark_predicted(nine_b_predictedHy)
            print(t1)
            print(nine_b_predictedHy)

            t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s = find_frequency_grades(t1)
            context = {'t1_fg_a': t1_fg_a, 't1_fg_b': t1_fg_b, 't1_fg_c': t1_fg_c,
                       't1_fg_d': t1_fg_d,
                       't1_fg_e': t1_fg_e, 't1_fg_f': t1_fg_f, 't1_fg_s': t1_fg_s}
            return render(request, 'basicinformation/teacher_relative_averages_predicted.html', context)
        else:
            listofstudents = teacher_listofStudents(profile,ajKlass)
            return render(request, 'basicinformation/teacher_update_page.html',
                          {'klass': listofstudents})


def create_student(num,request):
  user = request.user 
 
  for i in range(3, num):
      try:
          us = User.objects.create_user(username='student' + str(i),
                                                       email='studentss' + str(i) + '@gmail.com',
                                                       password='dnpandey')
          us.save()
          gr = Group.objects.get(name='Students')
          gr.user_set.add(us)
          cl = klass.objects.all()
          classes = []
          for k in cl:
              classes.append(k)
              stu = Student(studentuser=us, klass=classes[0], rollNumber=int(str(i) + '00'), name='stu' + str(i),
                                       dob=timezone.now(), pincode=int(str(405060)))
              stu.save()
              sub = Subject(name='Science', student=stu,teacher = user.teacher, test1
                            =randint(3,10),test2 = randint(3,9))
              sub.save()
      except Exception as e:
        print(str(e))
