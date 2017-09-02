from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
import os.path
from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from random import randint
from datetime import timedelta
from datetime import date
import numpy as np
import pandas as pd
import urllib.request
from more_itertools import unique_everseen
from django.contrib.auth.models import User, Group
from .models import Student, Teacher, Subject, School, klass
from django.utils import timezone
from django.contrib.staticfiles.templatetags.staticfiles import static
# from .marksprediction import predictionConvertion, readmarks, averageoftest, teacher_get_students_classwise
from .marksprediction import *
from Private_Messages.models import *

def home(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Management').exists():
            all_students = Student.objects.filter(school =
                                                  user.schoolmanagement.school)
            all_studs_list = []
            all_klasses = []
            for i in all_students:
                all_studs_list.append(i)
                all_klasses.append(i.klass.name)
            all_klasses = list(unique_everseen(all_klasses))
            num_classes = len(all_klasses)
            context = {'students':all_studs_list,'num_classes':num_classes,'all_classes':all_klasses}
            return render(request,'basicinformation/managementHomePage.html',context)
        if user.is_staff:
            df = \
            pd.read_csv('/app/basicinformation/english.csv')
            #with \
            #        open('/home/prashant/Desktop/programming/projects/bodhiai/BodhiAI/basicinformation/englishpassages.pkl'
            #             ,'rb') as fi:
            #    all_passages = pickle.load(fi)
            quests = []
            optA = []
            optB = []
            optC = []
            optD = []
            right_answer = []
            quest_category = []
            quests = df['questions']
            optA = df['optionA']
            optB = df['optionB']
            optC = df['optionC']
            optD = df['optionD']
            quest_category = df['category']
            for i in df['correctOption']:
                if i == 'a':
                    right_answer.append(1)
                elif i == 'b':
                    right_answer.append(2)
                elif i == 'c':
                    right_answer.append(3)
                elif i == 'd':
                    right_answer.append(4)
            for ind in range(len(optA)):
                write_questions(quests[ind],optA[ind],optB[ind],optC[ind],optD[ind],right_answer[ind],quest_category[ind])
            #write_passages(all_passages)
            return HttpResponse('hello')
            #return render(request,'basicinformation/staffpage1.html')
        if user.groups.filter(name='Students').exists():
            profile = user.student
            me = Studs(request.user)
            subjects = user.student.subject_set.all()
            teacher_name = {}
            for sub in subjects:
                teacher_name[sub.name] = sub.teacher # retrieve all marks from database
            # Get all the student marks
            try:
                mathst1,mathst2,mathst3,mathshy,mathst4,mathspredhy =\
                me.readmarks('Maths')
            except:
                mathst1 = mathst2 = mathst3 = mathshy = mathst4 = mathspredhy=None
            try:
                hindit1,hindit2,hindit3,hindihy,hindit4,hindipredhy =\
                me.readmarks('Hindi')
            except:
                hindit1 = hindit2 = hindit3 = hindihy = hindit4 = hindipredhy=None
            try:
                englisht1,englisht2,englisht3,englishhy,englisht4,englishpredhy =\
                me.readmarks('English')
            except:
                englisht1 = englisht2 = englisht3 = englishhy = englisht4 =\
                englishpredhy=None
            try:
                sciencet1,sciencet2,sciencet3,sciencehy,sciencet4,sciencepredhy =\
                me.readmarks('Science')
            except:
                sciencet1 = sciencet2 = sciencet3 = sciencehy = sciencet4 =\
                sciencepredhy=None

            # check for announcements in past 48 hours
            startdate = date.today()
            enddate = startdate - timedelta(days=2)
            my_announcements = Announcement.objects.filter(listener =
                                                           profile,date__range=[enddate,startdate])

            # find the predicted marks
            try:
                hindipredhy_raw = \
                me.hindi_3testhyprediction(hindit1,hindit2,hindit3,me.get_dob(),me.get_section())
                hindipredhy = me.predictionConvertion(hindipredhy_raw)
            except:
                pass

            try:
                mathspredhy_raw = \
                me.hindi_3testhyprediction(mathst1,mathst2,mathst3,me.get_dob(),me.get_section())
                mathspredhy = me.predictionConvertion(mathspredhy_raw)
            except:
                pass
            try:
                englishpredhy_raw = \
                me.english_3testhyprediction(englisht1,englisht2,englisht3,me.get_dob(),me.get_section())
                englishpredhy = me.predictionConvertion(englishpredhy_raw)
            except:
                pass
            try:
                sciencepredhy_raw = \
                me.science_3testhyprediction(sciencet1,sciencet2,sciencet3,me.get_dob(),me.get_section())
                sciencepredhy = me.predictionConvertion(sciencepredhy_raw)
            except:
                pass
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
            weak_links = {}
            for i in klasses:
                weak_links[i]= me.online_problematicAreasNames(user,subjects[0],i)
            num_klasses = len(klasses)
            num_subjects = len(subjects)
            context = {'profile': profile,
                       'klasses': klasses, 'subjects': subjects, 'num_klasses': num_klasses,
                       'isTeacher': True, 'num_subjects':
                       num_subjects,'weak_links':weak_links}
            return render(request, 'basicinformation/teacher1.html', context)
        else:

            return render(request, 'basicinformation/home.html')
    else:
        return HttpResponseRedirect(reverse('membership:login'))

#def student_profile_page(request):
#    user = request.user
#    if user.is_authenticated:
#        if user.groups.filter(name='Students').exists():
#            if user.student.address and user.student.phone:
#                myProfile = StudentCustomProfile(


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
    me = Studs(user)
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
            if me.institution == 'School':
                tests = OnlineMarks.objects.filter(test__sub=subject, student=user.student)
            elif me.institution == 'SSC':
                tests = SSCOnlineMarks.objects.filter(test__sub=subject, student=user.student)

            context = {'tests': tests}
            return \
                render(request, 'basicinformation/student_self_sub_tests.html', context)
        if 'studentTestid' in request.GET:
            test_id = request.GET['studentTestid']
            if me.institution == 'School':
                test = OnlineMarks.objects.get(student=user.student, test__id=test_id)
                student_type = 'School'
            elif me.institution == 'SSC':
                test = SSCOnlineMarks.objects.get(student=user.student, test__id=test_id)
                student_type = 'SSC'
            my_marks_percent = (test.marks / test.test.max_marks) * 100
            average, percent_average = \
                me.online_findAverageofTest(test_id, percent='p')
            percentile, all_marks = me.online_findPercentile(test_id)
            all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]
            freq = me.online_QuestionPercentage(test_id)
            
            context = \
                {'test': test, 'average': average, 'percentAverage': percent_average,
                 'my_percent': my_marks_percent, 'percentile': percentile, 'allMarks': all_marks,
                 'freq': freq,'student_type':student_type}
            return \
                render(request, 'basicinformation/student_analyze_test.html', context)

def student_weakAreasSubject(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Students').exists():
           me = Studs(user)
           subs = me.my_subjects_names()
           context = {'subs':subs}
           return render(request,'basicinformation/student_weakAreas_subject.html',context)


def student_weakAreas(request):
    if 'studWA' in request.GET:
       me = Studs(request.user)
       subject = request.GET['studWA']
       timing_areawise,freq_timer = me.areawise_timing(subject)
       freq = me.weakAreas_IntensityAverage(subject)
       me.improvement(subject)
        # changing topic categories numbers to names
       timing_areawiseNames =\
        me.changeTopicNumbersNames(timing_areawise,subject)
       freq_Names = me.changeTopicNumbersNames(freq,subject)
       context = \
       {'freq':freq_Names,'timing':timing_areawiseNames,'time_freq':freq_timer}
       return render(request,'basicinformation/student_weakAreas.html',context)







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

def teacher_weakAreasinDetail(request):
    user = request.user
    if user.is_authenticated:
        if 'weakAreasButton' in request.GET:
            which_class = request.GET['weakAreasClass']
            me = Teach(user)
            subjects = me.my_subjects_names()
            res = me.online_problematicAreaswithIntensityAverage(user,subjects[0],which_class)
            res = me.change_topicNumbersNamesWeakAreas(res,subjects[0])
            timing,freq_timing = me.weakAreas_timing(user,subjects[0],which_class)
            timing = me.change_topicNumbersNamesWeakAreas(timing,subjects[0])
            context =\
            {'which_class':which_class,'probAreas':res,'timing':timing}
            return render(request,'basicinformation/teacher_weakAreasinDetail.html',context)


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
    institution = profile.school.category
    klass_dict, all_klasses = teacher_get_students_classwise(request)
    me = Teach(user)
    if 'ajKlass' in request.GET:
        return HttpResponse('Choose from Above')
        #which_class = request.GET['ajKlass']
        #me = Teach(user)
        #t1,t2,t3,tphy = me.listofStudentsMarks(which_class)
        #marks = list(zip(t1,t2,t3))
        #context = {'marks':marks}
        #return render(request,'basicinformation/teacher_all_offlineMarks.html',context)
    elif 'schoolTestAnalysis' in request.GET:
        which_klass = request.GET['schoolTestAnalysis']
        which_class = which_klass.split(',')[0]
        subjects = me.my_subjects_names()
        context = {'subjects': subjects, 'which_class': which_class}
        return \
            render(request, 'basicinformation/teacher_school_analysis1.html', context)
    elif 'schoolSubject' in request.GET:
        schoolSubject = request.GET['schoolSubject']
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
        if institution == 'School':
            which_class = which_klass.split(',')[0]
            subjects = me.my_subjects_names()
            context = {'subs': subjects, 'which_class': which_class}
            return \
                render(request, 'basicinformation/teacher_online_analysis.html', context)
        elif institution == 'SSC':
            subjects = me.my_subjects_names()
            context = {'subs': subjects, 'which_class': which_klass}
            return \
                render(request, 'basicinformation/teacher_online_analysis.html', context)

    elif 'onlineschoolSubject' in request.GET:
        onlineSubject = request.GET['onlineschoolSubject']
        if institution == 'School':
            sub = onlineSubject.split(',')[0]
            which_class = onlineSubject.split(',')[1]
            online_tests = KlassTest.objects.filter(creator=
                                                    user, klas__name=which_class, sub=
                                                    sub)
            context = {'tests': online_tests}
            return render(request, 'basicinformation/teacher_online_analysis2.html', context)
        elif institution == 'SSC':
            sub = onlineSubject.split(',')[0]
            which_class = onlineSubject.split(',')[1]
            online_tests = SSCKlassTest.objects.filter(creator=
                                                    user,
                                                       klas__name=which_class, sub=
                                                    sub)
            context = {'tests': online_tests}
            return render(request, 'basicinformation/teacher_online_analysis2.html', context)

    elif 'onlinetestid' in request.GET:
        test_id = request.GET['onlinetestid']
        if institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id=test_id)
            test = KlassTest.objects.get(id = test_id)
            problem_quests = me.online_problematicAreasperTest(test_id)
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
                       'freq':freq,'sq':sq,'problem_quests':problem_quests,'school':True}
            return render(request, 'basicinformation/teacher_online_analysis3.html', context)
        elif institution == 'SSC':
            online_marks = SSCOnlineMarks.objects.filter(test__id=test_id)
            test = SSCKlassTest.objects.get(id = test_id)
            problem_quests = me.online_problematicAreasperTest(test_id)
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
                       'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True}
            return render(request, 'basicinformation/teacher_online_analysis3.html', context)

    elif 'onlineIndividualPerformace' in request.GET:
        which_klass = request.GET['onlineIndividualPerformace']
        subjects = me.my_subjects_names()
        context = {'subs': subjects, 'which_class': which_klass}
        return \
            render(request,
                   'basicinformation/teacher_online_individualPerformace.html', context)
    elif 'individualonlineschoolSubject' in request.GET:
        sub_class = request.GET['individualonlineschoolSubject']
        sub = sub_class.split(',')[0]
        klass = sub_class.split(',')[1]
        if me.institution == 'School':
            online_tests = KlassTest.objects.filter(creator=
                                                user, klas__name=klass, sub=
                                                sub)
        elif me.institution == 'SSC':
            online_tests = SSCKlassTest.objects.filter(creator =
                                                       user,klas__name =
                                                       klass,sub=sub)
        context = {'tests': online_tests}
        return render(request,
                      'basicinformation/teacher_online_individualPerformance2.html', context)
    elif 'individualonlinetestid' in request.GET:
        test_id = request.GET['individualonlinetestid']
        if me.institution == 'School':
            every_marks = OnlineMarks.objects.filter(test__id = test_id)
        elif me.institution == 'SSC':
            every_marks = SSCOnlineMarks.objects.filter(test__id =
                                                             test_id)
        studs = []
        for stu in every_marks:
            studs.append(stu.student)
        context = {'students':studs,'test_id':test_id}
        return \
    render(request,'basicinformation/teacher_online_individualPerformance3.html',context)
    elif 'individualStudentid' in request.GET:
        stude_test = request.GET['individualStudentid']
        test_id = stude_test.split(',')[1]
        student_id = stude_test.split(',')[0]
        if me.institution == 'School':
            his_marks = OnlineMarks.objects.get(student__id = student_id, test__id
                                            = test_id)
            student_type = 'School'
        elif me.institution == 'SSC':
            his_marks = SSCOnlineMarks.objects.get(student__id = student_id,
                                                test__id = test_id)
            student_type = 'SSC'

        context = {'test':his_marks,'student_type':student_type}
        return \
    render(request,'basicinformation/teacher_online_individualPerformance4.html',context)
        
# functions for school management

def management_homePage(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Management').exists():
            all_students = Student.objects.filter(school =
                                                  user.schoolManagement.school)
            all_studs_list = []
            all_klasses = []
            for i in all_students:
                all_studs_list.append(i)
                all_klasses.append(i.klass.name)
            all_klasses = list(unique_everseen(all_klasses))
            num_classes = len(all_klasses)

            context =\
            {'students':all_studs_list,'num_classes':num_classes,'all_classes':all_klasses}
            return
        render(request,'basicinformation/managementHomePage.html',context)



# functions for the admin


def create_entities(request):
    if request.POST:
        who = request.POST['deed']
        if who == 'teacher':
            create_teacher(5)
            return HttpResponse('done')
        elif who == 'student':
            create_student(100,request)
            return HttpResponse('done') 



def create_student(num, request):

    user = request.user
    school = School.objects.get(name='Not Dummy School')
    #teachers = Teacher.objects.filter(school__name = 'Not Dummy School')
    mathTeacher = Teacher.objects.get(name = 'teacher4')
    scienceTeacher = Teacher.objects.get(name ='teacher3')
    for i in range(1, num):
        try:
            us = User.objects.create_user(username='student' +
                                          str(i),
                                          email='studentss' + str(i) + '@gmail.com',
                                          password='dummypassword')
            us.save()
            gr = Group.objects.get(name='Students')
            gr.user_set.add(us)
            cl = klass.objects.filter(school__name='Not Dummy School')
            classes = []
            for cc in cl:
                classes.append(cc)
            stu = Student(studentuser=us, klass=np.random.choice(classes),
                              rollNumber=int(str(randint(7000,12000)) + '00'),
                              name='stud' + str(randint(800,4500)),
                              dob=timezone.now(),
                          pincode=int(str(405060)),school= school)
            stu.save()
            sub = Subject(name='Maths', student=stu, teacher=mathTeacher, test1
            =randint(3, 10), test2=randint(3, 9), test3=
                          randint(3, 9))
            sub1 = Subject(name='Science', student=stu, teacher=scienceTeacher, test1
            =randint(3, 10), test2=randint(3, 9), test3=
                          randint(3, 9))

            sub.save()
        except Exception as e:
            print(str(e))


def create_teacher(num):
    school1 = School.objects.get(name='Dummy School')
    school2 = School.objects.get(name='Not Dummy School')
    schools = [school1,school2]
    for i in range(num):
        try:
            us = User.objects.create_user(username='teacher' + str(i),
                                          email='teacher' + str(i) + '@gmail.com',
                                          password='dummypassword')
            us.save()
            gr = Group.objects.get(name='Teachers')
            gr.user_set.add(us)

            teache = Teacher(teacheruser=us,
                             experience=randint(1, 20), name=us.username,
                             school=np.random.choice(schools))
            teache.save()
        except Exception as e:
            print(str(e))

def read_questions(fi):
    with open(fi,encoding='latin-1') as questFile:
        readcsv = csv.reader(questFile,delimiter=',')
        questText = []
        a = []
        b = []
        c = []
        d = []
        for row in questFile:
            text = row[1]
            questText.append(str(text))
    return questText


def write_questions(question,optA,optB,optC,optD,correctOpt,questCategory):
    school = School.objects.filter(category = 'SSC')
    all_options = [optA,optB,optC,optD]
    new_questions = SSCquestions()
    new_questions.tier_category = '1'
    new_questions.section_category = 'English'
    new_questions.text = str(question)
    print(questCategory)
    if str(questCategory) == '1.0':
        new_questions.topic_category = '1.1'
    elif str(questCategory) == '2.0':
        new_questions.topic_category = '2.1'
    elif str(questCategory) == '3.0':
        new_questions.topic_category = '3.1'
    elif str(questCategory) == '4.0':
        new_questions.topic_category = '4.1'
    elif str(questCategory) == '5.0':
        new_questions.topic_category = '5.1'
    elif str(questCategory) == '6.0':
        new_questions.topic_category = '6.1'
    elif str(questCategory) == '7.0':
        new_questions.topic_category = '7.1'
    elif str(questCategory) == '8.0':
        new_questions.topic_category = '8.1'
    elif str(questCategory) == '9.0':
        new_questions.topic_category = '9.1'
    else:
        new_questions.topic_category = str(questCategory)
    new_questions.save()
    for sch in school:
        new_questions.school.add(sch)
    #for j in range(1,9):
    #    if questCategory == str(j):
    #        mn = questCategory + '.'+'1'
    #        print(mn)
    #        new_questions.topic_category = str(mn)
    #        new_questions.topic_category = str(mn)
    #        new_questions.save()
    #    else:
    #        new_questions.topic_category = str(questCategory)
    #        new_questions.save()
    #print(new_questions.topic_category)
    for n,i in enumerate(all_options):
        new_choices = Choices()
        new_choices.sscquest = new_questions
        new_choices.text = str(i)
        if correctOpt == n+1:
            new_choices.predicament = 'Correct'
        else:
            new_choices.predicament = 'Wrong'
        new_choices.save()

def write_passages(passages):
    for i in passages:
        new_passage = Comprehension()
        new_passage.text = str(i)
        new_passage.save()







