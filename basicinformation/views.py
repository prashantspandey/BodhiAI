from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
import os.path
import pickle
from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from random import randint
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import timedelta
import math
from datetime import date
import numpy as np
import pandas as pd
import urllib.request
from more_itertools import unique_everseen
from django.contrib.auth.models import User, Group
from .models import *
from django.utils import timezone
from django.contrib.staticfiles.templatetags.staticfiles import static
# from .marksprediction import predictionConvertion, readmarks, averageoftest, teacher_get_students_classwise 
from .marksprediction import *
from operator import itemgetter
from io import BytesIO as IO
import timeit
from PIL import Image
import requests
from django.contrib import messages

@ensure_csrf_cookie
def home(request):
    user = request.user
    if user.is_authenticated:
        # if user is from management this code fires up
        if user.groups.filter(name='Management').exists():
            all_students = Student.objects.filter(school =
                                                  user.schoolmanagement.school)
            all_teachers =\
            Teacher.objects.filter(school=user.schoolmanagement.school)
            klasses = klass.objects.filter(school=user.schoolmanagement.school)
            test_teachers ={}
            for te in all_teachers:
                all_tests = SSCKlassTest.objects.filter(creator =
                                                        te.teacheruser)
                test_teachers[te] = {all_tests}
            new_test_teachers = {}
            new_test_teachers = {}
            for key,value in test_teachers.items():
                n_tests = []
                for qs in value:
                    for te in qs:
                        if te.published <=\
                        datetime.strptime('2018-01-27','%Y-%m-%d').date():
                            pass
                        else:
                            n_tests.append(te)
                    new_test_teachers[key] = {'test':n_tests}


            context =\
                    {'students':all_students,'teachers':all_teachers,'all_classes':klasses,'tests_created':new_test_teachers}
            return render(request,'basicinformation/managementHomePage.html',context)
        if user.is_staff:
            #te = SSCKlassTest.objects.get(name='GroupYT1')
            #quests = []
            #for q in te.sscquestions_set.all():
            #    quests.append(q)
            #te.pk = None
        
            #us = User.objects.get(username = 'govindgarwa@gmail.com')
            #te.creator = us
            #te.name = 'GroupYTest1GDA'
            #te.save()
            #for q in quests:
            #    q.ktest.add(te)
            #de = SSCKlassTest.objects.get(name='GroupYT2')
            #quests = []
            #for q in de.sscquestions_set.all():
            #    quests.append(q)
            #de.pk = None
        
            #us = User.objects.get(username = 'govindgarwa@gmail.com')
            #de.creator = us
            #de.name = 'GroupYTest2GDA'
            #de.save()
            #for q in quests:
            #    q.ktest.add(de)

            #ee = SSCKlassTest.objects.get(name='GroupYT3')
            #quests = []
            #for q in ee.sscquestions_set.all():
            #    quests.append(q)
            #ee.pk = None
        
            #us = User.objects.get(username = 'govindgarwa@gmail.com')
            #ee.creator = us
            #ee.name = 'GroupYTest3GDA'
            #ee.save()
            #for q in quests:
            #    q.ktest.add(ee)


            #add_teachers('teachers.csv','Govindam Defence Academy',production=True)
            #add_students('swami2jan.csv','Swami Reasoning World',swami=True,production=True)
            #add_students('students3.csv','Govindam Defence Academy',production=True)
            add_questions('Colonel Defence Academy','Defence-Physics')
            add_questions('Colonel Defence Academy','Defence-English')
            #sheet_links = ['groupx03math.csv','groupx03physics.csv']
            #sheet_links = ['groupx04math.csv','groupx04physics.csv']
            
            #sheet_links =\
            #['1english.csv','2english.csv','3english.csv','4english.csv','5english.csv']
            #sheet_link2=['7english.csv','8english.csv','9english.csv','10english.csv']
            #sheet_link3 =\
            #['1gk.csv','2gk.csv','3gk.csv','4gk.csv','5gk.csv','7gk.csv','8gk.csv','9gk.csv','10gk.csv']
            sheet_link3 =\
            ['ch5.csv','ch6.csv','ch7.csv']
            sheet_link4 =\
            ['ch8.csv','ch9.csv','ch10.csv','ch11.csv']
            #sheet_link5 = ['33t2.csv','34t2.csv']
            #add_to_database_questions(sheet_link4,'Colonel Defence\
            #                          Academy',onlyImage=True,production =\
            #                          True)
            #add_to_database_questions(sheet_link3,'Colonel Defence\
            #                          Academy',onlyImage=True,production =\
            #                          True)

            #def add_to_database_questions(sheet_link,extra_info=False,production=False,onlyImage =
            #                  False,fiveOptions=False,explanation_quest=False):

            #add_questions('BodhiAI','GroupX-Maths')
            #add_questions('Colonel Defence Academy','GroupX-Maths')
            #add_questions('Govindam Defence Academy','GroupX-Maths')
            #add_questions('Govindam Defence Academy','Defence-English')
            #add_questions('BodhiAI','Defence-English')
            #add_questions('BodhiAI','Defence-GK-CA')
            #add_questions('BodhiAI','Defence-Physics')
            #add_questions('Govindam Defence Academy','Defence-English')
            add_student_subject('Colonel Defence Academy','Defence-Physics',None,allTeacers=True)
            
            #questions = SSCquestions.objects.filter(section_category = 'GroupX-English')
            #print(len(questions))
            #delete_sectionQuestions('GroupX-English')
            return HttpResponse('hello')

        if user.groups.filter(name='Students').exists():
            profile = user.student
            #storage = messages.get_messages(request)
            me = Studs(request.user)

            # if B2C customer then add tests  to profile
            if profile.school.name == 'BodhiAI':
                #replace_quest_image()
                # checks if test is legitimate, if not then delete the test
                bad_tests = SSCKlassTest.objects.filter(Q(sub='')| Q(totalTime
                                                                    = 0))
                if bad_tests:
                    try:
                        for i in bad_tests:
                            i.delete()
                    except Exception as e:
                        print(str(e))
                
                me.subjects_OnlineTest()
            subjects = user.student.subject_set.all()

            # gets marks of all the tests taken by student to be displayed on home page
            subject_marks = me.test_information(subjects)

           # get new tests to take (practise tests on the student page) 
            new_tests = me.toTake_Tests(6)

            # sending all values to template based on type of student
            if me.profile.school.name == "BodhiAI":
                context = \
                        {'profile':profile,'subjects':subjects,'subjectwiseMarks':subject_marks,'newTests':new_tests}
            else:
                context = \
                    {'profile':profile,'subjects':subjects,'subjectwiseMarks':subject_marks,'newTests':new_tests}

            return render(request, 'basicinformation/studentInstitute.html', context)


        elif user.groups.filter(name='Teachers').exists():
            me = Teach(user)
            profile = user.teacher
            klasses = me.my_classes_names()
            subjects = me.my_subjects_names()
            weak_links = {}
            weak_klass = []
            weak_subs = []
            subs = []
            try:
                #for sub in subjects:
                #    for i in klasses:
                #        try:
                #            weak_links[i]= \
                #            me.online_problematicAreasNames(user,sub,i)
                #            weak_subs.append(weak_links[i])
                #            weak_klass.append(i)
                #            subs.append(sub)
                #        except Exception as e:
                #            print(str(e))
                #weak_subs_areas = list(zip(subs,weak_klass,weak_subs))
                weak_subs_areas = None
            except:
                weak_subs_areas = None

            num_klasses = len(klasses)
            weak_subs_areas = list(zip(subs,weak_klass,weak_subs))
            num_subjects = len(subjects)
            context = {'profile': profile,
                       'klasses': klasses, 'subjects': subjects, 'num_klasses': num_klasses,
                       'isTeacher': True, 'num_subjects':
                       num_subjects,'weak_links':weak_subs_areas}
            return render(request, 'basicinformation/teacher1.html', context)
        else:

            return render(request, 'basicinformation/home.html')
    else:
        return HttpResponseRedirect(reverse('membership:login'))


# gets tests of selected topic by the student on home page

def student_select_topicTest(request):
    user = request.user
    if user.is_authenticated:
        if 'topicwisetest' in request.GET:
            topic = request.GET['topicwisetest']
            me = Studs(user)
            new_tests = me.toTake_Tests(0,allTests=True)
            topic_tests_id = []

            for k,v in new_tests.items():
                if topic in new_tests[k]['topics']:
                    topic_tests_id.append(k)
            newer_tests = []
            for i in topic_tests_id:
                topic_test = SSCKlassTest.objects.get(id = i)
                newer_tests.append(topic_test)
            ntest = {}
            for test in newer_tests:
                all_tp = []
                count = 0
                for quest in test.sscquestions_set.all():
                    count += 1
                    cat =\
                    me.changeIndividualNames(quest.topic_category,quest.section_category)
                    all_tp.append(cat)
                all_tp_unique = list(unique_everseen(all_tp))
                ntest[test.id] =\
                {'subject':test.sub,'topics':all_tp_unique,'num_questions':count}
            context = {'newTests':ntest}
            return render(request,'basicinformation/studentInstituteTopicTests.html',context)

def student_moreTests(request):
    user = request.user
    if user.is_authenticated:
        if 'homePageMoreTests' in request.GET:
            me = Studs(user)
            new_tests = me.toTake_Tests(0,allTests = True)
            context = {'newTests':new_tests}
            return render(request,'basicinformation/studentMoreTests.html',context)


def student_self_analysis(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Teachers').exists():
            raise Http404(" This page is only meant for student to see.")
        elif user.groups.filter(name='Students').exists():
            me = Studs(user)
            if me.profile.school.name == 'BodhiAI':
                allSubjects = me.subjects_OnlineTest() 
                allSubjects = me.already_takenTests_Subjects()
            else:
                allSubjects = me.already_takenTests_Subjects()
            
            context = {'subjects': allSubjects}
            return render(request, 'basicinformation/selfStudentAnalysis.html', context)


def student_subject_analysis(request):
    user = request.user
    me = Studs(user)
    if user.is_authenticated:
        if 'studentwhichsub' in request.GET:
            which_sub = request.GET['studentwhichsub']
            if me.institution == 'SSC':
                ana_type = ['Institute Tests', 'Online Tests']
            else:
                ana_type = ['School Tests', 'Online Tests']

            context = {'anatype': ana_type, 'sub': which_sub}
            return \
                render(request, 'basicinformation/student_analysis_subjects.html', context)
        if 'studentwhichana' in request.GET:
            which_one = request.GET['studentwhichana']
            mode = which_one.split(',')[1]
            sub = which_one.split(',')[0]
            subject = sub

            if mode == 'online':
                if me.institution == 'School':
                    tests = OnlineMarks.objects.filter(test__sub=subject,
                                                       student=me.profile)
                elif me.institution == 'SSC':
                    tests = SSCOnlineMarks.objects.filter(test__sub=subject,
                                                          student=me.profile)

                context = {'tests': tests,'subject':subject}
                return \
                    render(request, 'basicinformation/student_self_sub_tests.html', context)
            elif mode == 'offline':
                if me.institution == 'School':
                    tests = OnlineMarks.objects.filter(test__sub=subject,
                                                       student=me.profile)
                elif me.institution == 'SSC':
                    tests = SSCOfflineMarks.objects.filter(test__sub=subject,
                                                           student=me.profile)
                context = {'tests': tests,'subject':subject}
                return \
                    render(request, 'basicinformation/student_self_sub_tests.html', context)

        if 'studentTestid' in request.GET:
            idandsubject = request.GET['studentTestid']
            test_id = idandsubject.split(',')[0]
            #visible_tests(test_id)
            sub = idandsubject.split(',')[1]
            if me.institution == 'School':
                test = OnlineMarks.objects.get(student=me.profile, test__id=test_id)
                student_type = 'School'
            elif me.institution == 'SSC':
                try:
                    test = SSCOfflineMarks.objects.get(student=me.profile, test__id=test_id)
                    mode = 'offline'
                except:
                    test = SSCOnlineMarks.objects.get(student=me.profile, test__id=test_id)
                    mode = 'online'

                student_type = 'SSC'
            if mode == 'online':
                my_marks_percent = (test.marks / test.test.max_marks) * 100
                average, percent_average = \
                    me.online_findAverageofTest(test_id, percent='p')
                percentile, all_marks = me.online_findPercentile(test_id)
                percentile = percentile * 100
                all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]
                freq = me.online_QuestionPercentage(test_id)
                # converting test time seconds to hours and minutes
                test_totalTime = test.timeTaken
                hours = int(test_totalTime/3600)
                t = int(test_totalTime%3600)
                mins = int(t/60)
                seconds =int(t%60)
                if hours == 0:
                    tt = '{} minutes and {} seconds'.format(mins,seconds)
                if hours == 0 and mins == 0:
                    tt = '{} seconds'.format(seconds)
                if hours > 0:
                    tt = '{} hours {} minutes and {}\
                    seconds'.format(hours,mins,seconds)
                try:
                    if tt:
                        pass
                except:
                    tt = None

                ra,wa,sp,accuracy = me.test_statistics(test_id)
                weak_areas = me.weakAreas_Intensity(sub,singleTest = test_id)
                sk_weak = me.skipped_testwise(test_id,me.profile)
                area_timing,freq = me.areawise_timing(sub,test_id)
                subjectwise_accuracy = me.test_SubjectAccuracy(test_id)
                if sub == 'SSCMultipleSections':
                    weak_names = weak_areas
                    timing = area_timing
                else:
                    weak_names = me.changeTopicNumbersNames(weak_areas,sub)
                    timing = me.changeTopicNumbersNames(area_timing,sub)
                context = \
                    {'test': test, 'average': average, 'percentAverage': percent_average,
                     'my_percent': my_marks_percent, 'percentile': percentile, 'allMarks': all_marks,
                     'freq':\
                     freq,'student_type':student_type,'topicWeakness':weak_names,'topicTiming':timing,
                     'numberRight':ra,'numberWrong':wa,'numberSkipped':sp,'accuracy':accuracy,'subjectwise_accuracy':subjectwise_accuracy,'tt':tt}
                return \
                    render(request, 'basicinformation/student_analyze_test.html', context)

        # for offline tests conducted in institute (with OMR) (no timing in
        # these)

            elif mode == 'offline':
                my_marks_percent = (test.marks / test.test.max_marks) * 100
                average, percent_average = \
                    me.offline_findAverageofTest(test_id, percent='p')
                percentile, all_marks = me.offline_findPercentile(test_id)
                percentile = percentile * 100
                all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]
                freq = me.offline_QuestionPercentage(test_id)
                ra,wa,sp,accuracy = me.offline_test_statistics(test_id)
                weak_areas = me.offline_weakAreas_Intensity(sub,singleTest = test_id)
                weak_names = me.changeTopicNumbersNames(weak_areas,sub)
                subjectwise_accuracy = me.offline_test_SubjectAccuracy(test_id)
                context = \
                    {'test': test, 'average': average, 'percentAverage': percent_average,
                     'my_percent': my_marks_percent, 'percentile': percentile, 'allMarks': all_marks,
                     'freq':
                     freq,'student_type':student_type,'topicWeakness':weak_names,
                     'numberRight':ra,'numberWrong':wa,'numberSkipped':sp,'accuracy':accuracy,'subjectwise_accuracy':subjectwise_accuracy,}
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
        freq_timer = me.changeTopicNumbersNames(freq_timer,subject)

        freq = me.weakAreas_IntensityAverage(subject)
        strongAreas = []
        strongFreq = []
        try:
           for i,j in freq:
                strongAreas.append(i)
                strongFreq.append(float(100-j))
        except Exception as e:
            print(str(e))
        if freq == 0:
           context = {'noMistake':'noMistake'}
           return render(request,'basicinformation/student_weakAreas.html',context)
        # changing topic categories numbers to names
        timing_areawiseNames =\
        me.changeTopicNumbersNames(timing_areawise,subject)
        freq_Names = me.changeTopicNumbersNames(freq,subject)
        skills = list(zip(strongAreas,strongFreq))
        skills_names = me.changeTopicNumbersNames(skills,subject)
        context = \
               {'freq':freq_Names,'timing':timing_areawiseNames,'time_freq':freq_timer,'skills':skills_names}
        return render(request,'basicinformation/student_weakAreas.html',context)


def student_improvement(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Students').exists():
           me = Studs(user)
           subjects = me.my_subjects_names()
           context = {'subjects':subjects}
           return \
       render(request,'basicinformation/student_improvement1.html',context)

def student_improvement_sub(request):
    user = request.user
    if 'improvementSub' in request.GET:
        sub = request.GET['improvementSub']
        me = Studs(user)
        overall = me.section_improvement(sub)
        if overall == 0:
            context = {'overall':None}
        else:
            context = {'overall':overall,}
        return\
    render(request,'basicinformation/student_improvement2.html',context)




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
            which_sub = request.GET['weakAreasSub']
            me = Teach(user)
            before = timeit.default_timer()
            res = \
            me.online_problematicAreaswithIntensityAverage(user,which_sub,which_class)
            res = me.change_topicNumbersNamesWeakAreas(res,which_sub)
            timing,freq_timing = me.weakAreas_timing(user,which_sub,which_class)
            timing = me.change_topicNumbersNamesWeakAreas(timing,which_sub)
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
        offline_tests = SSCKlassTest.objects.filter(sub =
                                                    sub,mode='BodhiSchool')
        context = {'Tests':offline_tests}
        return \
    render(request,'basicinformation/teacher_school_analysis2.html',context)

    elif 'schoolTestid' in request.GET:
        test_class = request.GET['schoolTestid']
        test_id = test_class.split(',')[0]
        which_class = test_class.split(',')[1]
        offline_marks = SSCOfflineMarks.objects.filter(test__id=test_id)
        test = SSCKlassTest.objects.get(id = test_id)
        problem_quests = me.offline_problematicAreasperTest(test_id)
        max_marks = 0
        for i in offline_marks:
            max_marks = i.test.max_marks
        average,percent_average =\
        me.offline_findAverageofTest(test_id,percent='p')
        grade_s,grade_a,grade_b,grade_c,grade_d,grade_e,grade_f= \
        me.online_freqeucyGrades(test_id,mode='offline')
        freq = me.offline_QuestionPercentage(test_id)
        result = me.generate_rankTable(test_id,mode='offline')
        try:
            result = result[result[:,3].argsort()]
        except:
            result = None
        sq = me.online_skippedQuestions(test_id,mode='offline')
        context = {'om': offline_marks,'test':test,'average':average
                   ,'percentAverage':percent_average,'maxMarks':max_marks,
                   'grade_s':grade_s,'grade_a':grade_a,'grade_b':grade_b,'grade_c':grade_c,
                   'grade_d':grade_d,'grade_e':grade_e,'grade_f':grade_f,
                   'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
        return render(request, 'basicinformation/teacher_school_analysis3.html', context)

    elif 'onlineTestAnalysis' in request.GET:
        which_klass = request.GET['onlineTestAnalysis']
        if institution == 'School':
            which_class = which_klass.split(',')[0]
            subjects = me.my_subjects_names()
            context = {'subs': subjects, 'which_class': which_class}
            return \
                render(request, 'basicinformation/teacher_online_analysis.html', context)
        elif institution == 'SSC':
            subject0 = me.my_subjects_names()
            #subject1 = me.pattern_test_taken_subjects()
            subjects = me.test_taken_subjects(user)
            sub = subject0+subjects
            context = {'subs': sub, 'which_class': which_klass}
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
            kl = me.my_classes_objects(which_class)

            online_tests = SSCKlassTest.objects.filter(creator=
                                                user,
                                                   klas=kl, sub=
                                                sub,mode='BodhiOnline')
            if len(online_tests) == 0 and sub == 'Defence-MultipleSubjects':
                online_tests = SSCKlassTest.objects.filter(creator=
                                                user,
                                                    sub=
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
            online_marks =\
            SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                                          me.profile.school)
            try:
                result_loader = SscTeacherTestResultLoader.objects.get(test__id = test_id)
            except:
                result_loader = SscTeacherTestResultLoader()
                res_test = SSCKlassTest.objects.get(id=test_id)
                result_loader.test = res_test
                result_loader.teacher = me.profile
                max_marks = res_test.max_marks
                result_loader.average,result_loader.percentAverage =\
                me.online_findAverageofTest(test_id,percent='p')
                result_loader.grade_s,result_loader.grade_a,result_loader.grade_b,\
                result_loader.grade_c,result_loader.grade_d,\
                result_loader.grade_e,result_loader.grade_f,\
                 = me.online_freqeucyGrades(test_id)
                skipped_loader = me.online_skippedQuestions(test_id)
                result_loader.skipped = list(skipped_loader[:,0])
                result_loader.skippedFreq = list(skipped_loader[:,1])
                problem_loader = me.online_problematicAreasperTest(test_id)
                result_loader.problemQuestions = list(problem_loader[:,0])
                result_loader.problemQuestionsFreq = list(problem_loader[:,1])
                freqAnswers = me.online_QuestionPercentage(test_id)
                freqAnswerQuest = freqAnswers[:,0]
                freqAnswersfreq = freqAnswers[:,1]
                result_loader.freqAnswersQuestions = list(freqAnswerQuest)
                result_loader.freqAnswersFreq = list(freqAnswersfreq)
                result_loader.save()
                for i in online_marks:
                    result_loader.onlineMarks.add(i)
                result = me.generate_rankTable(test_id)
                try:
                    result = result[result[:,3].argsort()]
                except:
                    result = None

                context = {'om':
                           online_marks,'test':result_loader.test,'average':result_loader.average
                           ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                           'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                           'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                           'freq':freqAnswers,'sq':skipped_loader,'problem_quests':problem_loader,'ssc':True,'result':result}
                return render(request, 'basicinformation/teacher_online_analysis3.html', context)


            saved_marks = result_loader.onlineMarks.all()
            if len(online_marks) == len(saved_marks):
                max_marks = result_loader.test.max_marks    
                pro_quests = result_loader.problemQuestions
                pro_freq  = result_loader.problemQuestionsFreq
                average = result_loader.average
                percent_average = result_loader.percentAverage
                problem_quests = list(zip(pro_quests,pro_freq))
                grade_s = result_loader.grade_s
                grade_a = result_loader.grade_a
                grade_b = result_loader.grade_b
                grade_c = result_loader.grade_c
                grade_d = result_loader.grade_d
                grade_e = result_loader.grade_e
                grade_f = result_loader.grade_f
                skipped_quests = result_loader.skipped
                skipped_freq = result_loader.skippedFreq
                sq = list(zip(skipped_quests,skipped_freq))
                freqQuests = result_loader.freqAnswersQuestions
                freqQuestsfreq = result_loader.freqAnswersFreq
                freq = list(zip(freqQuests,freqQuestsfreq))
                result = me.generate_rankTable(test_id)
                try:
                    result = result[result[:,3].argsort()]
                except:
                    result = None
                context = {'om':
                           online_marks,'test':result_loader.test,'average':result_loader.average
                           ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                           'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                           'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                           'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
                return render(request, 'basicinformation/teacher_online_analysis3.html', context)

            else:
                #test = SSCKlassTest.objects.get(id = test_id)
                #problem_quests = me.online_problematicAreasperTest(test_id)
                #max_marks = 0
                #for i in online_marks:
                #    max_marks = i.test.max_marks
                #average,percent_average =me.online_findAverageofTest(test_id,percent='p')
                #grade_s,grade_a,grade_b,grade_c,grade_d,grade_e,grade_f= \
                #me.online_freqeucyGrades(test_id)
                #freq = me.online_QuestionPercentage(test_id)
                #sq = me.online_skippedQuestions(test_id)
                result = me.generate_rankTable(test_id)
                try:
                    result = result[result[:,3].argsort()]
                except:
                    result = None
                
                
                result_loader.average,result_loader.percentAverage =\
                me.online_findAverageofTest(test_id,percent='p')
                result_loader.grade_s,result_loader.grade_a,result_loader.grade_b,\
                result_loader.grade_c,result_loader.grade_d,\
                result_loader.grade_e,result_loader.grade_f,\
                 = me.online_freqeucyGrades(test_id)
                skipped_loader = me.online_skippedQuestions(test_id)
                result_loader.skipped = list(skipped_loader[:,0])
                result_loader.skippedFreq = list(skipped_loader[:,1])
                problem_loader = me.online_problematicAreasperTest(test_id)
                result_loader.problemQuestions = list(problem_loader[:,0])
                result_loader.problemQuestionsFreq = list(problem_loader[:,1])
                freqAnswers = me.online_QuestionPercentage(test_id)
                freqAnswerQuest = freqAnswers[:,0]
                freqAnswersfreq = freqAnswers[:,1]
                result_loader.freqAnswersQuestions = list(freqAnswerQuest)
                result_loader.freqAnswersFreq = list(freqAnswersfreq)
                result_loader.save()
                max_marks = result_loader.test.max_marks
                for i in online_marks:
                    result_loader.onlineMarks.add(i)
                context = {'om':
                           online_marks,'test':result_loader.test,'average':result_loader.average
                           ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                           'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                           'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                           'freq':freqAnswers,'sq':skipped_loader,'problem_quests':problem_loader,'ssc':True,'result':result}
                return render(request, 'basicinformation/teacher_online_analysis3.html', context)

    elif 'onlineIndividualPerformace' in request.GET:
        which_klass = request.GET['onlineIndividualPerformace']
        subjects = me.test_taken_subjects(user)
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
            offline_every_marks = SSCOfflineMarks.objects.filter(test__id =
                                                         test_id)
            if len(offline_every_marks)>0:
                studs = []
                for stu in offline_every_marks:
                    studs.append(stu.student)
                context = {'students':studs,'test_id':test_id}
                return \
    render(request,'basicinformation/teacher_online_individualPerformance3.html',context)
            else:
                online_every_marks = SSCOnlineMarks.objects.filter(test__id =
                                                             test_id)
                studs = []
                for stu in online_every_marks:
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
            try:
                his_marks = SSCOfflineMarks.objects.get(student__id = student_id,
                                                test__id = test_id)
            except:
                his_marks = SSCOnlineMarks.objects.get(student__id = student_id,
                                                test__id = test_id)
            student_type = 'SSC'

        context = {'test':his_marks,'student_type':student_type}
        return \
    render(request,'basicinformation/teacher_online_individualPerformance4.html',context)

def teacher_download_result(request):
    user = request.user
    me = Teach(user)
    if 'downloadresult' in request.GET:
        test_id = request.GET['downloadresult']
        result = me.generate_rankTable(test_id)
        if len(result) == 0:
            result = me.generate_rankTable(test_id,mode='offline')
        try:
            result = result[result[:,3].argsort()]
        except:
            result = result
        df = pd.DataFrame(result)
        excel_result = IO()
        xlwriter = pd.ExcelWriter(excel_result, engine= 'xlsxwriter')
        df.to_excel(xlwriter,'result')
        xlwriter.save()
        xlwriter.close()
        excel_result.seek(0)
        response =\
        HttpResponse(excel_result.read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=results.xlsx'

        return response


        
# functions for school management
def management_information(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Management').exists():
            if 'managementBatchid' in request.GET:
               batchid = request.GET['managementBatchid']
               teachers = Teacher.objects.filter(Q(school =\
                                                  user.schoolmanagement.school) and
               Q(subBatch = None))
               if len(teachers) != 0:
                   context = {'SubBatch':True,'batch':batchid}
                   return\
               render(request,'basicinformation/management_Information2.html',context)
               else:
                   tests = SSCKlassTest.objects.filter(klas__id = batchid)
                   teachers = []
                   for te in tests:
                       teachers.append(te.creator)
                   teachers = list(unique_everseen(teachers)) 
                   context = {'teachers':teachers,'batch':batchid}
                   return\
                render(request,'basicinformation/management_Information3.html',context)
            if 'managementChoice' in request.GET:
                choiceandbatch = request.GET['managementChoice']
                choice = choiceandbatch.split(',')[0]
                batch_id = choiceandbatch.split(',')[1]

                if choice == 'chbatch':

                    context={'ho':'hello'} 
                    return\
                render(request,'basicinformation/management_Information3.html',context)
                else:
                   tests = SSCKlassTest.objects.filter(klas__id = batch_id)
                   teachers = []
                   for te in tests:
                       teachers.append(te.creator)
                   teachers = list(unique_everseen(teachers)) 
                   context = {'teachers':teachers}

                   return\
                render(request,'basicinformation/management_Information3.html',context)
            if 'managementTeacherid' in request.GET:
                teacher_id = request.GET['managementTeacherid']
                tests = SSCKlassTest.objects.filter(creator__id = teacher_id)
                context = {'tests':tests}
                return\
            render(request,'basicinformation/management_Information4.html',context)
            if 'managementTestid' in request.GET:
                test_id = request.GET['managementTestid']
                test = SSCKlassTest.objects.get(id= int(test_id))
                teacher_user = test.creator
                me = Teach(teacher_user)
                online_marks = SSCOnlineMarks.objects.filter(test__id=test_id)
                try:
                    result_loader = SscTeacherTestResultLoader.objects.get(test__id = test_id)
                except Exception as e:
                    print(str(e))

                    result_loader = SscTeacherTestResultLoader()
                    res_test = SSCKlassTest.objects.get(id=test_id)
                    result_loader.test = res_test
                    result_loader.teacher = me.profile
                    max_marks = res_test.max_marks
                    result_loader.average,result_loader.percentAverage =\
                    me.online_findAverageofTest(test_id,percent='p')
                    result_loader.grade_s,result_loader.grade_a,result_loader.grade_b,\
                    result_loader.grade_c,result_loader.grade_d,\
                    result_loader.grade_e,result_loader.grade_f,\
                     = me.online_freqeucyGrades(test_id)
                    skipped_loader = me.online_skippedQuestions(test_id)
                    result_loader.skipped = list(skipped_loader[:,0])
                    result_loader.skippedFreq = list(skipped_loader[:,1])
                    problem_loader = me.online_problematicAreasperTest(test_id)
                    result_loader.problemQuestions = list(problem_loader[:,0])
                    result_loader.problemQuestionsFreq = list(problem_loader[:,1])
                    freqAnswers = me.online_QuestionPercentage(test_id)
                    freqAnswerQuest = freqAnswers[:,0]
                    freqAnswersfreq = freqAnswers[:,1]
                    result_loader.freqAnswersQuestions = list(freqAnswerQuest)
                    result_loader.freqAnswersFreq = list(freqAnswersfreq)
                    result_loader.save()
                    for i in online_marks:
                        result_loader.onlineMarks.add(i)
                    result = me.generate_rankTable(test_id)
                    try:
                        result = result[result[:,3].argsort()]
                    except:
                        result = None
                    context = {'om':
                               online_marks,'test':result_loader.test,'average':result_loader.average
                               ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                               'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                               'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                               'freq':freqAnswers,'sq':skipped_loader,'problem_quests':problem_loader,'ssc':True,'result':result}

                    return\
                    render(request,'basicinformation/management_Information5.html',context)
                saved_marks = result_loader.onlineMarks.all()
                if len(online_marks) == len(saved_marks):
                    max_marks = result_loader.test.max_marks    
                    pro_quests = result_loader.problemQuestions
                    pro_freq  = result_loader.problemQuestionsFreq
                    average = result_loader.average
                    percent_average = result_loader.percentAverage
                    problem_quests = list(zip(pro_quests,pro_freq))
                    grade_s = result_loader.grade_s
                    grade_a = result_loader.grade_a
                    grade_b = result_loader.grade_b
                    grade_c = result_loader.grade_c
                    grade_d = result_loader.grade_d
                    grade_e = result_loader.grade_e
                    grade_f = result_loader.grade_f
                    skipped_quests = result_loader.skipped
                    skipped_freq = result_loader.skippedFreq
                    sq = list(zip(skipped_quests,skipped_freq))
                    freqQuests = result_loader.freqAnswersQuestions
                    freqQuestsfreq = result_loader.freqAnswersFreq
                    freq = list(zip(freqQuests,freqQuestsfreq))
                    result = me.generate_rankTable(test_id)
                    try:
                        result = result[result[:,3].argsort()]
                    except:
                        result = None
                    context = {'om':
                               online_marks,'test':result_loader.test,'average':result_loader.average
                               ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                               'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                               'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                               'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
                    return render(request,
                                  'basicinformation/management_Information5.html', context)

                else:
                    result = me.generate_rankTable(test_id)
                    try:
                        result = result[result[:,3].argsort()]
                    except:
                        result = None
                    
                    
                    result_loader.average,result_loader.percentAverage =\
                    me.online_findAverageofTest(test_id,percent='p')
                    result_loader.grade_s,result_loader.grade_a,result_loader.grade_b,\
                    result_loader.grade_c,result_loader.grade_d,\
                    result_loader.grade_e,result_loader.grade_f,\
                     = me.online_freqeucyGrades(test_id)
                    skipped_loader = me.online_skippedQuestions(test_id)
                    result_loader.skipped = list(skipped_loader[:,0])
                    result_loader.skippedFreq = list(skipped_loader[:,1])
                    problem_loader = me.online_problematicAreasperTest(test_id)
                    result_loader.problemQuestions = list(problem_loader[:,0])
                    result_loader.problemQuestionsFreq = list(problem_loader[:,1])
                    freqAnswers = me.online_QuestionPercentage(test_id)
                    freqAnswerQuest = freqAnswers[:,0]
                    freqAnswersfreq = freqAnswers[:,1]
                    result_loader.freqAnswersQuestions = list(freqAnswerQuest)
                    result_loader.freqAnswersFreq = list(freqAnswersfreq)
                    result_loader.save()
                    max_marks = result_loader.test.max_marks
                    for i in online_marks:
                        result_loader.onlineMarks.add(i)
                    context = {'om':
                               online_marks,'test':result_loader.test,'average':result_loader.average
                               ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                               'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                               'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                               'freq':freqAnswers,'sq':skipped_loader,'problem_quests':problem_loader,'ssc':True,'result':result}
                    return render(request,
                              'basicinformation/management_Information5.html', context)














               #batchid = request.GET['managementBatchid']
               #tests = SSCKlassTest.objects.filter(klas__id = batchid)
               #teachers = []
               #for te in tests:
               #    teachers.append(te.creator)
               #teachers = list(unique_everseen(teachers)) 
               #context = {'teachers':teachers}
               #return\
           #render(request,'basicinformation/management_Information2.html',context)

            if 'managementTeacherid' in request.GET:
                return HttpResponse('teacher')
            klasses = klass.objects.filter(school=user.schoolmanagement.school)
            context = {'klasses':klasses}
            return\
        render(request,'basicinformation/management_Information.html',context)



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
    school = School.objects.get(name='Swami Reasoning World')
    teacher = Teacher.objects.get(school__name = 'Swami Reasoning World')
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

def real_create_student(stu,schoolName,swami=False,multiTeacher =False):
    print('in process............')
    school = School.objects.get(name=schoolName)
    if swami:
        for na,dob,batch,phone,password in stu:
            try:
                teacher = Teacher.objects.get(teacheruser__username =
                                              'rajeshkswamiadmin')
            except Exception as e:
                print(str(e))
            try:
                us = User.objects.create_user(username=phone,
                                                email=str(na)+'@swami.com',
                                              password=password)
                us.save()
                gr = Group.objects.get(name='Students')
                gr.user_set.add(us)
                if batch == 16:
                    cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch16')
                elif batch == 17:
                    cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch17')
                elif batch == 24:
                    cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch24')
                elif batch == 15:
                    cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch15')
                stu = Student(studentuser=us, klass=cl,
                                  rollNumber=us.id,
                                  name= str(na),
                                  dob=datetime.strptime(dob,'%d/%m/%Y').strftime('%Y-%m-%d'),
                              pincode=int(str(302018)),school= school)
                stu.save()
                sub = Subject(name='General-Intelligence', student=stu,
                              teacher=teacher)

                sub.save()
                print('%s -- saved' %na)

            except Exception as e:
                print(str(e))

    else:
        for na,batch,phone,teach,email in stu:
            try:
                if multiTeacher:
                    teacher = Teacher.objects.filter(school__name = schoolName)
                    print('%s num teacher' %len(teacher))
                else:
                    teacher = Teacher.objects.get(teacheruser__username = teach)
                    print(teacher)
            except Exception as e:
                print(str(e))
            try:
                pa = str(phone)
                pa = pa[::-1]
                us = User.objects.create_user(username=phone,
                                              email='',
                                              password=pa)
                us.save()
                gr = Group.objects.get(name='Students')
                gr.user_set.add(us)
                if schoolName == 'Swami Reasoning World':
                    if batch == 16:
                        cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch16')
                    elif batch == 17:
                         cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch17')
                    elif batch == 24:
                          cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch24')
                    elif batch == 15:
                          cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch15')
                elif schoolName =='JECRC':
                    if '4th' in batch:
                        cl =\
                        klass.objects.get(school__name=schoolName,name='IT-4th-semester')
                    if '6th' in batch:
                        cl =\
                        klass.objects.get(school__name=schoolName,name='IT-6th-semester')
                elif schoolName == 'Govindam Defence Academy':
                    cl = klass.objects.get(school__name =
                                           schoolName,name='DefenceBatch')
                elif schoolName == 'Colonel Defence Academy':
                    cl = klass.objects.get(school__name =
                                           schoolName,name='DefenceBatch')

                stu = Student(studentuser=us, klass=cl,
                                  rollNumber=us.id,
                                  name= str(na),
                                  dob=timezone.now(),
                              pincode=int(str(302018)),school= school)
                stu.save()
                if multiTeacher:
                    for te in teacher:
                        sub = Subject(name='Defence-Physics', student=stu,
                                      teacher=te)
                        sub1 = Subject(name='GroupX-Maths', student=stu,
                                      teacher=te)
                        sub2 = Subject(name='Defence-English', student=stu,
                                      teacher=te)

                        sub.save()
                        print('%s student-- %s subject -- %s teacher'
                              %(stu,sub.name,te))
                        sub1.save()
                        print('%s student-- %s subject -- %s teacher'
                              %(stu,sub1.name,te))
                        sub2.save()
                        print('%s student-- %s subject -- %s teacher'
                              %(stu,sub2.name,te))

                else:
                    sub = Subject(name='Defence-Physics', student=stu,
                                  teacher=teacher)
                    sub1 = Subject(name='GroupX-Maths', student=stu,
                                  teacher=teacher)
                    sub2 = Subject(name='Defence-English', student=stu,
                                  teacher=teacher)

                    sub.save()
                    sub1.save()
                    sub2.save()

                print('%s -- saved' %na)
            except Exception as e:
                print(str(e))


def create_teacher(num):
    school1 = School.objects.get(name='Dummy School')
    school2 = School.objects.get(name='Not Dummy School')
    schools = [school1,school2]
    for i in range():
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


def\
write_questions(school,question,optA,optB,optC,optD,optE,image,correctOpt,questCategory,exp,sectionType,lang,used_for,source,fouroptions=False,replace=False):
    if replace:
        quest = SSCquestions.objects.filter(picture = image)
        for n,qu in enumerate(quest):
            for num,ch in enumerate(qu.choices_set.all()):
                print(num)
                if num+1 == correctOpt:
                    ch.predicament ='Correct'
                else:
                    ch.predicament = 'Wrong'
                ch.save()
            
    else:


        school = School.objects.filter(name = school)
        if fouroptions == True:
            all_options = [optA,optB,optC,optD]
        else:
            try:
                if optE:
                    if math.isnan(optE):
                        all_options = [optA,optB,optC,optD]
                    else:
                        all_options = [optA,optB,optC,optD,optE]
                else:
                        all_options = [optA,optB,optC,optD,optE]
            except Exception as e:
                print(str(e))
                all_options = [optA,optB,optC,optD,optE]
        new_questions = SSCquestions()
        if lang == 'Hindi':
            new_questions.language = 'Hindi'
        if lang == 'Bi':
            new_questions.language = 'Bi'
        if lang == 'English':
            new_questions.language = 'English'

        if used_for == 'Groupx':
            new_questions.usedFor = 'Groupx'
        if used_for == 'Groupy':
            new_questions.usedFor = 'Groupx'
        if used_for == 'SSC':
            new_questions.usedFor = 'SSC'
        if source:
            new_questions.source = source

        new_questions.tier_category = '1'
        new_questions.max_marks = int(1)
        new_questions.negative_marks = 0.0
        if sectionType == 'English':
            new_questions.section_category = 'English'
        elif sectionType == 'Reasoning':
            new_questions.section_category = 'General-Intelligence'
        elif sectionType == 'Maths':
            new_questions.section_category = 'Quantitative-Analysis'
        elif sectionType == 'GK':
            new_questions.section_category = 'General-Knowledge'
        elif sectionType == 'groupxen':
            new_questions.section_category = 'Defence-English'
        elif sectionType == 'groupxphy':
            new_questions.section_category = 'Defence-Physics'
        elif sectionType == 'groupxmath':
            new_questions.section_category = 'GroupX-Maths'
        elif sectionType == 'groupgk':
            new_questions.section_category = 'Defence-GK-CA'

        if question != None:
            new_questions.text = str(question)
        new_questions.topic_category = str(questCategory)
        if image:
            new_questions.picture = image
        new_questions.save()
        for sch in school:
            new_questions.school.add(sch)
        #for j in range(1,9):
        #    if questCategory == str(j):
        #        mn = questCategory + '.'+'1'
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
            if 'https:' in str(i):
                new_choices.picture = str(i)
            else:
                itext = str(i).replace('[','')
                itext2 = itext.replace(']','')
                itext3 = itext2.replace(')','')
                itext4 = itext3.replace(u'\\xa0',u' ')
                itext5 = itext4.replace('\"','')
                new_choices.text = itext5
            if 'https:' in str(exp):
                pass
            else:
                exptext = str(exp).replace('[','')
                exptext2 = exptext.replace(']','')
                exptext3 = exptext2.replace(u'\\xa0',u' ')
                exptext4 = exptext3.replace('\"','')
            if correctOpt == n+1:
                new_choices.predicament = 'Correct'
                if 'https:' in str(exp):
                    new_choices.explanationPicture = exp
                else:
                    new_choices.explanation = exptext4
            else:
                new_choices.predicament = 'Wrong'
            new_choices.save()

def write_passages(passages):
    for i in passages:
        new_passage = Comprehension()
        new_passage.text = str(i)
        new_passage.save()

def evaluate_offline_test(studentid,opt):
    test = SSCKlassTest.objects.get(creator__username = 'rajeshkswamiadmin')
    qid = []
    for q in test.sscquestions_set.all():
        qid.append(q.id)
    qans = list(zip(qid,opt))
    chid = []
    rightAnswer = []
    wrongAnswer = []
    allAnswer = []
    skippedAnswer = []
    total_marks = 0
    for j,k in qans:
        quest = SSCquestions.objects.get(id=j)
        for n,i in enumerate(quest.choices_set.all()):
            if k == '0':
                skippedAnswer.append(j)
                break
            if k == 'a' and n == 0:
                chid.append(i.id)
                if i.predicament == 'Correct':
                    rightAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks += 2
                elif i.predicament == 'Wrong':
                    wrongAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks -= 0.25
                break
            elif k == 'b' and n == 1:
                chid.append(i.id)
                if i.predicament == 'Correct':
                    rightAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks += 2
                elif i.predicament == 'Wrong':
                    wrongAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks -= 0.25
                break
            elif k == 'c' and n == 2:
                chid.append(i.id)
                if i.predicament == 'Correct':
                    rightAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks += 2
                elif i.predicament == 'Wrong':
                    wrongAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks -= 0.25
                break
            elif k == 'd' and n == 3:
                chid.append(i.id)
                if i.predicament == 'Correct':
                    rightAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks += 2
                elif i.predicament == 'Wrong':
                    wrongAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks -= 0.25
                break
            elif k == 'e' and n == 4:
                chid.append(i.id)
                if i.predicament == 'Correct':
                    rightAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks += 2
                elif i.predicament == 'Wrong':
                    wrongAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks -= 0.25
                break
    offline_marks = SSCOfflineMarks()
    offline_marks.allAnswers = allAnswer
    offline_marks.rightAnswers = rightAnswer
    offline_marks.wrongAnswers = wrongAnswer
    offline_marks.skippedAnswers = skippedAnswer
    offline_marks.test = test
    student = Student.objects.get(studentuser__username = studentid)
    offline_marks.student = student
    offline_marks.marks = total_marks
    offline_marks.testTaken = timezone.now()
    offline_marks.save()
             

def trial_ai(request):
    school = School.objects.get(name= 'Swami Reasoning World')
    students = Student.objects.filter(school=school)
    marks = []
    stud = []
    time = []
    ave_oftest = []
    for st in students:
        try:
            online_marks = SSCOnlineMarks.objects.filter(student =
                                                         st).order_by('testTaken')
            if len(online_marks) != 0:
                marks.extend(online_marks)
                for times in range(len(online_marks)):
                    stud.append(st)
                for num,om in enumerate(online_marks):
                    try:
                        test_loader =\
                        SscTeacherTestResultLoader.objects.get(test=om.test)
                        ave_oftest.append(test_loader.average)
                    except Exception as e:
                        print(str(e))
                        ave_oftest.append(float('nan'))
                    time.append(int(num+1))
        except Exception as e:
            print(str(e))
    st_marks = list(zip(stud,marks,ave_oftest,time))
    st_marks = np.array(st_marks)
    print(st_marks)
    print(st_marks.shape)
    qid2 = []
    catid2 = []
    accid2 = []
    st2 = []
    quest_acc = []
    questidfinal = []
    for st in students:
        online_marks =\
        SSCOnlineMarks.objects.filter(student=st).order_by('testTaken')
        if len(online_marks) != 0:
            for nu,marks in enumerate(online_marks):
                qid = []
                catid = []
                r_w = []
                for nu,quest in enumerate(marks.test.sscquestions_set.all()):
                    q_test = SSCOnlineMarks.objects.filter(test__sscquestions=quest)
                    right = 0
                    wrong = 0
                    skipped = 0
                    for q in q_test:
                        for c in quest.choices_set.all():
                            if c.id in q.rightAnswers:
                                right += 1
                            if c.id in q.wrongAnswers:
                                wrong += 1
                            else:
                                skipped += 1
                    try:
                        quest_acc.append((right-wrong)/(right+wrong)*100)
                        questidfinal.append(quest.id)
                    except Exception as e:
                        print(str(e))
                        quest_acc.append(float('nan'))
                        questidfinal.append(quest.id)

                    
                        
                    for ch in quest.choices_set.all():
                        if ch.id in marks.rightAnswers:
                            r_w.append('R')
                        if ch.id in marks.wrongAnswers:
                            r_w.append('W')
                        else:
                            r_w.append('S')
                        qid.append(quest.id)
                        catid.append(quest.topic_category)
                        st2.append(st.id)
                qid2.extend(qid)
                catid2.extend(catid)
                accid2.extend(r_w)

    #unique,count = np.unique(catid2,return_counts = True)
    #cat_unique = np.asarray((unique,count)).T
    cat_unique = list(unique_everseen(catid2))
    cat_tot = []
    acc_cat_stu = []
    stu_cat = []
    for st in students:
        for un_cat in cat_unique:
            right = 0
            wrong = 0
            om_marks = SSCOnlineMarks.objects.filter(test__testTakers
                                                     =st)
            for om in om_marks:
                for quest in\
                om.test.sscquestions_set.filter(topic_category=un_cat):
                    for ch in quest.choices_set.all():
                        if ch.id in om.rightAnswers:
                            right += 1
                        if ch.id in om.wrongAnswers:
                            wrong += 1
            try:
                acc = ((right-wrong)/(right+wrong)*100)

            except Exception as e:
                acc_cat_stu.append(float('nan'))
            cat_tot.append(un_cat)
            acc_cat_stu.append(acc)
            stu_cat.append(st.id)

           

    personal_cat = list(zip(stu_cat,cat_tot,acc_cat_stu))
    personal_cat = np.array(personal_cat)
    print(personal_cat)
    print(personal_cat.shape)
    qu_acc = list(zip(questidfinal,quest_acc))
    qu_acc = np.array(qu_acc)
    final = list(zip(st2,qid2,catid2,accid2))
    final = np.array(final)
    quest_accuracy = []
    for st,qid,catid,accid in final:
        for q,a in qu_acc:
            if int(qid) == int(q):
                quest_accuracy.append(a)
    final2 = list(zip(st2,qid2,catid2,accid2,quest_accuracy))
    final2 = np.array(final2)
    stu_category = []
    last_st = []
    last_cat = []
    last_qid = []
    last_accid = []
    last_questacc = []
    last_stqacc = []
    for st,qid,catid,accid,quest_accuracy in final2:
        for stid,cat,qacc in personal_cat:
            if st == stid and catid == cat:
                last_st.append(st)
                last_cat.append(catid)
                last_qid.append(qid)
                last_accid.append(accid)
                last_questacc.append(quest_accuracy)
                last_stqacc.append(qacc)
    last =\
    list(zip(last_st,last_cat,last_qid,last_accid,last_questacc,last_stqacc))
    last = np.array(last)
    with open('bodhidata.pkl','wb') as fi:
        pickle.dump(last,fi)
    print(last)
    print(last.shape)
    print(last.shape)
    print(len(stu_category))
    print(len(personal_cat))
    print(final.shape)
    print(qu_acc.shape)



def replace_quest_image():
    image_questions = SSCquestions.objects.all()
    all_quests = []
    for i in image_questions:
        if i.picture != None:
            all_quests.append(i)
    for num,i in enumerate(all_quests):
        if num == 5:
            break
        img = Image.open(requests.get(i.picture,stream=True).raw)
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2]:
                newData.append((255,255,255,0))
            else:
                newData.append(item)
                img.putdata(newData)
        img.show()

def real_create_teacher(name,teach,ph = False):
    school = School.objects.get(name=name)
    for name,batch,email in teach:
        print([name,batch,email])
        if ph:
            pas = str(email)
            pas = pas[::-1]
        else:
            pass
        try:
            us = User.objects.create_user(username=str(email),
                                          email='',
                                          password=pas)
            us.save()
            gr = Group.objects.get(name='Teachers')
            gr.user_set.add(us)

            teache = Teacher(teacheruser=us,
                             experience=0, name=name,
                             school=school)
            teache.save() 
            print('%s --- name saved' %name)
        except Exception as e:
            print(str(e))

def add_teachers(path_file,schoolName,production=False,jecrc=False,dummy=False):
    if dummy != True:
        if production:
            df = \
            pd.read_csv('/app/client_info/govindamdefence_Kuchaman/'+path_file,error_bad_lines =False)
        else:
            df =\
            pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/client_info/govindamdefence_Kuchaman/'+path_file,error_bad_lines=False )
        if jecrc:
            name = df['Name']
            batch = df['Group associated']
            email = df['email ID']
            teach = list(zip(name,batch,email))
            real_create_teacher('JECRC',teach)
        if schoolName == 'Colonel Defence Academy':
            print('here in colonel')
            name = df['Name']
            phone = df['Phone']
            batch = ['DefenceBatch','DefenceBatch']
            teach = list(zip(name,batch,phone))
            real_create_teacher('Colonel Defence Academy',teach,ph=True)
        if schoolName == 'Govindam Defence Academy':
            name = df['Name']
            many = len(name)
            phone = df['Phone']
            batch = many*['DefenceBatch']
            teach = list(zip(name,batch,phone))
            real_create_teacher('Govindam Defence Academy',teach,ph=True)



    else:
        if schoolName == 'Govindam Defence Academy':
            name = ['Name']
            many = len(name)
            phone = ['Phone']
            batch = many*['DefenceBatch']
            teach = list(zip(name,batch,phone))
            real_create_teacher('Govindam Defence Academy',teach,ph=True)



def add_students(path_file,schoolName,production = False,swami=False,dummy=False):
    if dummy == False:
        if production:
            df = \
            pd.read_csv('/app/client_info/swami_jaipur/'+path_file,error_bad_lines =False)
        else:
            df =\
            pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/client_info/swami_jaipur/'+path_file,error_bad_lines=False )
        if swami:
            name = df['Name']
            dob = df['DOB']
            batch = df['Batch no']
            username = df['Phone']
            password = df['password']
            stu = list(zip(name,dob,batch,username,password))
            real_create_student(stu,'Swami Reasoning World',swami = True)
            return HttpResponse(stu)
        if schoolName == 'Colonel Defence Academy':
            name = df['Name']
            many = len(name)
            email = many*['']
            phone = df['Phone']
            batch = many*['']
            teach = many*['']
            stu = list(zip(name,batch,phone,teach,email))
            real_create_student(stu,'Colonel Defence Academy',multiTeacher=True)
            return HttpResponse(stu)

        if schoolName == 'Govindam Defence Academy':
            name = df['Name']
            many = len(name)
            email = many*['']
            phone = df['Phone']
            batch = many*['']
            teach = many*['']
            stu = list(zip(name,batch,phone,teach,email))
            real_create_student(stu,'Govindam Defence Academy',multiTeacher=True)
            return HttpResponse(stu)



    else:
        #name = df['Student Name']
        #email = df['Email ID(Active)']
        #phone = df['Contact Number(Whatsapp)']
        #teach = df['TG']
        #batch = df['batch']
        name = ['Dummy Student1','Dummy Student2','Dummy\
                Student3','Dummy Student4','Dummy Student5','Dummy\
                Student6','Dummy Student7','Dummy Student8','Dummy\
                Student9','Dummy Student10','Dummy Student11','Dummy Student12']
        email =\
        ['dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com']
        phone =\
        ['g1','g2','g3','g4','g5','g6','g7','g8','g9','g10','g11','g12']
        teach =\
        ['govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com']
        batch =\
        ['Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX']
        print(len(name))
        print(len(email))
        print(len(phone))
        print(len(teach))
        print(len(batch))
        stu_details = list(zip(name,batch,phone,teach,email))
        real_create_student(stu_details,'Govindam Defence Academy')


def add_questions(institute,section):
    if institute == 'JECRC':
       questions = SSCquestions.objects.filter(school__name = 'Swami Reasoning World')
       school = School.objects.get(name = institute)
       print('%s --num quests' %len(questions))
       for i in questions:
           i.school.add(school)
    elif institute == 'Govindam Defence':
       questions = SSCquestions.objects.filter(school__name =
                                               'BodhiAI',section_category='English')
       school = School.objects.get(name = institute)
       print('%s --num quests' %len(questions))
       for i in questions:
           i.school.add(school)
    else:
        questions =\
        SSCquestions.objects.filter(section_category=section)
        school = School.objects.get(name = institute)
        print(len(questions))
        for i in questions:
            i.school.add(school)

                    
def change_password(institute,acc):
    if institute == 'JECRC':
        for us,pa in acc:
            user = User.objects.get(username = us)
            print(user.password)
            user.set_password(pa)
            user.save()
            print('%s-- username , %s -- password'
                  %(user.username,user.password))

def add_to_database_questions(sheet_link,school,production=False,onlyImage =
                              False,fiveOptions=False,explanation_quest=False):
        for sh in sheet_link:
            if production:
                df=\
                pd.read_csv('/app/question_data/defence_maths/lucent/'+sh,error_bad_lines=False )
            else:
                df=\
                pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/question_data/defence_maths/lucent/'+sh,error_bad_lines=False )

            quests = []
            optA = []
            optB = []
            optC = []
            optD = []
            optE = []
            right_answer = []
            quest_category = []
            temp = []
            used_for = df['usedfor']
            #lang = df['lang']
            source = df['source']
            if onlyImage:
                images = df['QuestionLink']
            else:
                quest_text = df['Question']
            optA = df['optionA']
            optB = df['optionB']
            optC = df['optionC']
            optD = df['optionD']
            sectionType = df['sectionType']
            if fiveOptions:
                optE = df['optionE'] 
            if explanation_quest:
                exp = df['Explanation']
            quest_category = df['category']
            for i in df['correct']:
                ichanged = str(i).replace(u'\\xa0',u' ')
                ichanged2 = ichanged.replace('Answer',' ')
                ichanged3 = ichanged2.replace('Explanation',' ')

                if 'a'  in ichanged.lower():
                    right_answer.append(1)
                elif 'b' in ichanged.lower():
                    right_answer.append(2)
                elif 'c'  in ichanged.lower():
                    right_answer.append(3)
                elif 'd'  in ichanged.lower():
                    right_answer.append(4)
                elif 'e' in ichanged.lower():
                    right_answer.append(5)
            if onlyImage:
                print('%s num images' %len(images))
            else:
                print('%s num quest text' %len(quest_text))
            print('%s optA' %len(optA))
            print('%s optB' %len(optB))
            print('%s optC' %len(optC))
            print('%s optD' %len(optD))
            print('%s correct answers' %len(right_answer))
            print('%s number of categories' %len(quest_category))
            #print('%s languages ' %len(lang))
            print('%s sources' %len(source))
            print('%s sheet ' %sh)
        
            for ind in range(len(optA)):
                if onlyImage:
                    write_questions(school,None,optA[ind],optB[ind],optC[ind],optD[ind],None,images[ind],right_answer[ind],quest_category[ind],None,sectionType[ind],str(used_for[ind]),None,source[ind],fouroptions=True)
                else:
                    write_questions(school,quest_text,optA[ind],optB[ind],optC[ind],optD[ind],None,None,right_answer[ind],quest_category[ind],None,sectionType[ind],used_for,lang[ind],source[ind],fouroptions=True)


def delete_sectionQuestions(section):
    questions = SSCquestions.objects.filter(section_category = section)
    print(len(questions))
    for i in questions:
        i.delete()


def add_student_subject(institute,subject,teach,allTeacers=False):
    students = Student.objects.filter(school__name = institute)
    if allTeacers:
        teachers = Teacher.objects.filter(school__name = institute)
        for st in students:
            for teach in teachers:
                sub = Subject(name=subject, student=st,
                                    teacher=teach)
                sub.save()

    else:
        teach = Teacher.objects.get(name=teach,school=institute)
        for st in students:
            sub = Subject(name=subject, student=st,
                                    teacher=teach)
            sub.save()



def check_add_entities():
        all_students = Student.objects.filter(school__name = 'JECRC')
        all_teachers = Teacher.objects.filter(school__name = 'JECRC')
        
        print(len(all_teachers))
        df =\
        pd.read_csv('/app/client_info/jecrc/jecrc_6thsem_itdepartment.csv',error_bad_lines=False )
        cf =\
        pd.read_csv('/app/client_info/jecrc/jecrc_4thsem.csv',error_bad_lines=False )
        tf =\
        pd.read_csv('/app/client_info/jecrc/jecrc_teacher.csv',error_bad_lines=False )
        name = tf['Name']
        email = tf['email ID']
        em_id = []
        for i in email:
            em_id.append(i)
        password = []
        for i in name:
            j = i.replace(" ","")
            pa = j.lower()
            password.append(str(pa))
        acc = list(zip(em_id,password))
        change_password('JECRC',acc)
        phoneNum = []
        phone = df['Contact Number(Whatsapp)']
        phone2 = cf['Contact Number(Whatsapp)']

        for i in phone:
            phoneNum.append(str(i))
        for i in phone2:
            phoneNum.append(str(i))
        print(len(phoneNum))
        print(phoneNum)
        student_num = []
        for num,st in enumerate(all_students):
            student_num.append(str(st.rollNumber))
        print('%s len students' %len(student_num))
        pho = list(unique_everseen(phoneNum))
        print('%s len pho' %len(pho))
        for n,ph in enumerate(phoneNum):
            if str(ph) in student_num:
                pass
            else:
                print('%s ---%s' %(n,ph))


def old_student_marks():
             #Get all the student marks
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

            # check for announcements in past 24 hours
            startdate = date.today()
            enddate = startdate - timedelta(days=1)
            try:
                my_announcements = Announcement.objects.filter(listener =
                                                           profile,date__range=[enddate,startdate])
            except:
                my_announcements = None

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
            context = {'profile': profile, 'subjects': subjects,
                       'hindihy_prediction': hindipredhy, 'mathshy_prediction': mathspredhy,
                       'englishhy_prediction': englishpredhy,
                       'sciencehy_prediction': sciencepredhy,
                       'maths1': mathst1, 'maths2': mathst2, 'maths3': mathst3,
                       'maths4': mathst4, 'hindi1': hindit1, 'hindi2': hindit2,
                       'hindi3': hindit3, 'hindi4': hindit4, 'english1': englisht1,
                       'english2': englisht2, 'english3': englisht3, 'english4': englisht4,
                       'science1': sciencet1, 'science2': sciencet2,
                       'science3': sciencet3, 'science4':
                       sciencet4,'announcements':my_announcements,'message':storage}
def some_AI_function():
            # testing for AI
            #trial_ai(request)
            #school = School.objects.get(name='Swami Reasoning World')
            #student = Student.objects.filter(school = school)
            #all_categories = []
            #student_accuracy = []
            #acc_list_all = []
            #acc_cat_all = []
            #stu_id_all = []
            
            #for i in student:
            #    total_right = []
            #    total_wrong = []
            #    subTest = SSCKlassTest.objects.filter(testTakers = i,sub =
            #                                          'General-Intelligence')
            #    right = 0
            #    wrong = 0
            #    category_right = []
            #    category_wrong = []
            #    for j in subTest:
            #        onlineMarks = SSCOnlineMarks.objects.filter(test =
            #                                                j,student =
            #                                                i)
            #        
            #        for k in onlineMarks:
            #            right = right + len(k.rightAnswers)
            #            wrong = wrong + len(k.wrongAnswers)
            #            for quest in k.test.sscquestions_set.all():
            #                for ch in quest.choices_set.all():
            #                    if ch.id in k.rightAnswers:
            #                        category_right.append(quest.topic_category)

            #                    if ch.id in k.wrongAnswers:
            #                        category_wrong.append(quest.topic_category)

            #            
            #    category_right = np.array(category_right)
            #    category_wrong = np.array(category_wrong)
            #    unique,counts = np.unique(category_right,return_counts = True)
            #    right_category = np.asarray((unique,counts)).T
            #    unique,counts = np.unique(category_wrong,return_counts = True)
            #    wrong_category = np.asarray((unique,counts)).T
            #    print(right_category,wrong_category)
            #    acc_list = []
            #    acc_cat = []
            #    stu_id = []
            #    for ca,freq in right_category:
            #        for cw,freqwr in wrong_category:
            #            if ca == cw:
            #                acc =\
            #                ((int(freq)-int(freqwr))/(int(freq)+int(freqwr)))*100
            #                acc_list.append(acc)
            #                acc_cat.append(ca)
            #                stu_id.append(i.id)
            #    acc_list_all.extend(acc_list)
            #    acc_cat_all.extend(acc_cat)
            #    stu_id_all.extend(stu_id)
            #    for cat_r in category_right:
            #        all_categories.append(cat_r)
            #    for cat_wr in category_wrong:
            #        all_categories.append(cat_wr)
            #acc_student = np.array([stu_id_all,acc_cat_all,acc_list_all])
            #all_categories = list(unique_everseen(all_categories))
            #print(all_categories)
            #teach = Teacher.objects.get(school = school)
            #all_questions = []
            #all_std = []
            #for stu in student:
            #    questions = []
            #    std =[]
            #    online_marks =SSCOnlineMarks.objects.filter(student=stu)
            #    for om in online_marks:
            #        for q in om.test.sscquestions_set.all():
            #            questions.append(q)
            #    count = len(questions)
            #    for i in range(count):
            #        std.append(stu)
            #    all_std.extend(std)
            #    
            #    

            #    if len(questions) != 0:
            #        all_questions.extend(questions)
            #        overall = list(zip(all_std,all_questions))
            #overall = np.array(overall)
            #print(overall.shape)
            #quest_accuracy = []
            #quest_skipped = []
            #for i,k in overall:
            #     
            #    topic = k.topic_category
            #    r_ans = 0
            #    w_ans = 0
            #    s_ans = 0

            #    online_marks =\
            #        SSCOnlineMarks.objects.filter(test__sscquestions=k,test__creator=
            #                                     teach.teacheruser)

            #    for qid in online_marks:
            #        if k.id in qid.skippedAnswers:
            #            s_ans = s_ans + 1
            #        else:
            #            for ch in k.choices_set.all():
            #                if ch.id in qid.rightAnswers:
            #                    r_ans = r_ans + 1
            #                if ch.id in qid.wrongAnswers:
            #                    w_ans = w_ans + 1
            #    try:
            #        accuracy = ((r_ans-w_ans)/(r_ans+w_ans))*100
            #        print('%s--%s---%s---%s----%s'
            #              %(k.id,accuracy,s_ans,r_ans,w_ans))
            #    except:
            #        accuracy = None
            #    quest_accuracy.append(accuracy)
            #    quest_skipped.append(s_ans)
            #quest_accuracy = np.array(quest_accuracy)
            #quest_skipped = np.array(quest_skipped)
            #overall_2 =\
            #np.array([overall[:,0],overall[:,1],quest_accuracy,quest_skipped])
            #overall_2 = np.transpose(overall_2)
            #student_accuracy = np.array(acc_student)
            #student_accuracy = np.transpose(student_accuracy)
            #num = 0
            #for stu,quest,acc,ski in overall_2:
            #    num = num +1
            #    for s,c,a in student_accuracy:
            #        
            #        if int(stu.id) == int(s) and quest.topic_category == c:
            #            print('%s--%s-- %s---%s---%s---%s'
            #                  %(num,stu.id,quest.topic_category,acc,a,ski))
            #predicament = []
            #stu_id = []
            #q_id = []
            #for stu,quest in overall_2[:,[0,1]]:
            #    stu_id.append(stu.id)
            #    q_id.append(quest.id)
            #    online_marks = SSCOnlineMarks.objects.filter(student =
            #                                                 stu,test__sscquestions
            #                                                 = quest)
            #    for om in online_marks:
            #        if quest.id in om.skippedAnswers:
            #            predicament.append('S')
            #        for ch in quest.choices_set.all():
            #            if ch.id in om.rightAnswers:
            #                predicament.append('R')
            #            if ch.id in om.wrongAnswers:
            #                predicament.append('W')
            #predicament = np.array(predicament)
            #stu_id = np.array(stu_id)
            #q_id = np.array(q_id)
            #pred = list(zip(stu_id,predicament,q_id))

            #pred = np.array(pred)
            #print(pred[:10])
            #print(pred.shape)
            #st_final = []
            #qu_final = []
            #qu_cat_fianl = []
            #for st in overall_2[:,0]:
            #    st_final.append(st.id)
            #for qu in overall_2[:,1]:
            #    qu_final.append(qu.id)
            #    qu_cat_fianl.append(qu.topic_category)
            #acc_student = np.transpose(acc_student)

            #print('%s-- ac student' %acc_student)
            #final =\
            #list(zip(st_final,qu_final,qu_cat_fianl,overall_2[:,2],overall_2[:,3],predicament))
            #final = np.array(final)
            #st_accu = []
            #n=0
            #nu = 0
            #for st,qu,cat,tacc,sk,pr in final:
            #    n = n +1
            #    for s,c,a in acc_student:
            #        if int(st) == int(s) and cat == c:
            #            nu = nu + 1
            #            print('%s-- %s-----%s---%s' %(n,nu,a,c))
            #            st_accu.append(a)
            #temp =[]
            #no_ids = []
            #unique,counts = np.unique(st_final,return_counts = True)
            #unique_stu = np.asarray((unique,counts)).T
            #for s in unique_stu[:,0]:
            #    if s in stu_id_all:
            #        temp.append('yes')
            #    else:
            #        temp.append('no')
            #        no_ids.append(s)
            #        print(s)
            #right_quid = []
            #quid = []
            #ls_id = []
            #acc_list = []
            ##for s,q,c,qa,qsk,pre in final:
            ##    marks =\
            ##    SSCOnlineMarks.objects.filter(student=stud)
            ##    if len(marks) == 0:
            ##        acc_list.append(0)
            ##    for ma in marks:
            ##        right = 0
            ##        wrong = 0
            ##        for quest in ma.test.sscquestions_set.all():
            ##            if quest.topic_category == c:
            ##                for ch in quest.choices_set.all():
            ##                    if ch.id in ma.rightAnswers:
            ##                        right = right + 1
            ##                    if ch.id in ma.wrongAnswers:
            ##                        wrong += 1
            ##                try:
            ##                    acc = ((right-wrong)/(right + wrong)*100)
            ##                except:
            ##                    acc = 0
            ##            else:
            ##                continue
            ##        quid.append(quest.id)
            ##        acc_list.append(acc)
            ##        ls_id.append(st)

            #lost_students = list(zip(ls_id,quid,acc_list))
            #lost_students = np.array(lost_students)
            #print(lost_students)
            #print(lost_students.shape)
            #





            #                   


            #unique,counts = np.unique(temp,return_counts = True)
            #unique_stu2 = np.asarray((unique,counts)).T
            #print(unique_stu2)
       
            #print(len(new_list))
            #new_list = np.array(new_list)
            #final_2 =\
            #list(zip([st_final,qu_final,qu_cat_fianl,overall_2[:,2],overall_2[:,3],new_list,predicament]))
            #final_2 = np.array(final_2)
            #final_2 = np.transpose(final_2)

            #print(final)
            #print(final_2.shape)
            #print(len(st_accu))



            #with open('bodhidata.pkl','wb') as fi:
            #    pickle.dump(final,fi)

            

                                
                                





 
                
            #for i in all_categories:
            #    quests = SSCquestions.objects.filter(section_category =
            #                                         'General-Intelligence',topic_category =
            #                                         i)
            #    print('%s quests len---%s topic' %(len(quests),i))
            #    for j in quests:
            #        r_ans = 0
            #        w_ans = 0
            #        s_ans = 0

            #        online_marks =\
            #            SSCOnlineMarks.objects.filter(test__sscquestions=j,test__creator=
            #                                         teach.teacheruser)

            #        if len(online_marks) != 0:
            #            for qid in online_marks:
            #                if j.id in qid.skippedAnswers:
            #                    s_ans = s_ans + 1
            #                else:
            #                    for ch in j.choices_set.all():
            #                        if ch.id in qid.rightAnswers:
            #                            r_ans = r_ans + 1
            #                        if ch.id in qid.wrongAnswers:
            #                            w_ans = w_ans + 1
            #        try:
            #            accuracy = ((r_ans-w_ans)/(r_ans+w_ans))*100
            #            print('%s--%s---%s' %(j.id,accuracy,s_ans))
            #        except:
            #            accuracy = None
            #            print('%s--%s---%s' %(j.id,accuracy,s_ans))


                




            #print('%s - tests taken' %len(online_marks))
            #tests = []
            #for i in online_marks:
            #    tests.append(i.test)
            #quests = []
            #for n,i in enumerate(tests):
            #    for q in i.sscquestions_set.all():
            #        quests.append(q)
            #for i in quests:
            #    print(i.text)
    pass
                
                






