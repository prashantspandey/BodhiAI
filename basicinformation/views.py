from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
import os.path
from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from random import randint
from datetime import timedelta
import math
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
from operator import itemgetter


def home(request):
    user = request.user
    if user.is_authenticated:
        # if user is from management this code fires up
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
            quad_questions = SSCquestions.objects.filter(section_category =\
                                                         'Quantitative-Analysis',topic_category=22.1)
            ch_list = []
            for quest in quad_questions:
                kk = "none"
                for ch in quest.choices_set.all():
                    if ch.text == kk:
                        ch_list.append(ch.id)
                    kk = ch.text
            print(ch_list)
            for c in ch_list:
                ch = Choices.objects.get(id = c)
                if ch.predicament == 'Correct':
                   print(ch.text)
                   rch = Choices.objects.get(id = c-1)
                   rch.predicament = 'Correct'
                   rch.save()
                   ch.delete()
                try:
                    ch.delete()
                except Exception as e:
                    print(str(e))

               
               
                    
            #idom_text = 'Choose the option which best explains the given phrase/idiom \n'
            #underlined_text = 'Choose the option which improves the sentence. \n'
            #substitution_text = 'Choose the option which can be substituted in place of given sentence.\n'
            #quests_idoms =\
            #SSCquestions.objects.filter(section_category='English',topic_category
            #                            = 1.2)
            #quests_underlined =\
            #SSCquestions.objects.filter(section_category='English',topic_category
            #                            = 3.1)
            #quests_substitution = \
            #SSCquestions.objects.filter(section_category='English',topic_category
            #                            = 6.1)
            #for i in quests_idoms:
            #    final_text = idom_text + i.text
            #    i.text = final_text
            #    i.save()
            #    print(i.text)
            #for i in quests_underlined:
            #    final_text = underlined_text + i.text
            #    i.text = final_text
            #    i.save()
            #    print(i.text)
            #for i in quests_substitution:
            #    final_text = substitution_text + i.text
            #    i.text = final_text
            #    i.save()
            #    print(i.text)

            #df = \
            #pd.read_csv('/app/basicinformation/english.csv')
            #with \
            #        open('/home/prashant/Desktop/programming/projects/bodhiai/BodhiAI/basicinformation/englishpassages.pkl'
            #             ,'rb') as fi:
            #    all_passages = pickle.load(fi)
            #df =\
            #pd.read_csv('/home/prashant/Desktop/programming/random/tesseract/resoningAnalogy.csv')
            #df=\
            #pd.read_csv('/home/prashant/Desktop/ssc_questions/gk/gk_dishaDiagram/62links.csv',error_bad_lines=False )
            #quests = []
            #optA = []
            #optB = []
            #optC = []
            #optD = []
            #right_answer = []
            #quest_category = []
            #quests = df['direction']
            #images = df['link']
            ##images = None
            #optA = df['a']
            #optB = df['b']
            #optC = df['c']
            #optD = df['d']
            ##optE = df['e'] 
            #exp = df['explanation']
            ##quest_category = df['category']
            #quest_category = '1.3' # spot the error
            #for i in df['ans']:
            #    ichanged = str(i).replace(u'\\xa0',u' ')
            #    ichanged2 = ichanged.replace('Answer',' ')
            #    ichanged3 = ichanged2.replace('Explanation',' ')
            #    if 'a' in ichanged :
            #        right_answer.append(1)
            #    elif 'b' in ichanged :
            #        right_answer.append(2)
            #    elif 'c' in ichanged :
            #        right_answer.append(3)
            #    elif 'd' in ichanged :
            #        right_answer.append(4)
            #    elif 'e' in ichanged :
            #        right_answer.append(5)
            #for ind in range(len(optA)):
            #    #print('%s -- opta,%s -- optb,%s -- optc, %s -- optd,%s\
            #    # -- right_answer,%s -- explanation'
            #    # %(optA[ind],optB[ind],optC[ind],optD[ind],right_answer[ind],exp[ind]))

            #    write_questions(quests[ind],optA[ind],optB[ind],optC[ind],optD[ind],None,images[ind],right_answer[ind],quest_category,exp[ind],sectionType='Resoning',fouroptions=True)
            ##write_passages(all_passages)
            #print(quests)
            #print(right_answer)
            #print(optE)
            #return HttpResponse('hello')
            ##return render(request,'basicinformation/staffpage1.html')
            return HttpResponse('hello')
        if user.groups.filter(name='Students').exists():
            profile = user.student
            me = Studs(request.user)
            subjects = me.my_subjects_names()
            me.subjects_OnlineTest()
            subjects = user.student.subject_set.all()
            
            teacher_name = {}
            subject_marks = {} 
            # check for marks objects of multiple sections
            multiple_marks = SSCOnlineMarks.objects.filter(test__sub =
                                                           'SSCMultipleSections',student=profile)
            
            for sub in subjects:
                teacher_name[sub.name] = sub.teacher
                # get all the marks objects subjectwise
                marks = SSCOnlineMarks.objects.filter(test__sub = sub.name,student =
                                                     profile)
                if marks:
                    one_marks = []
                    time = []
                    # add date and marks to a dictionary with index subject
                    for i in marks:
                        one_marks.append(float(i.marks)/float(i.test.max_marks)*100)
                        time.append(i.testTaken)
                        subject_marks[sub.name] = {'marks':one_marks,'time':time}
                if multiple_marks:
                    multiple_one_marks = []
                    multiple_time = []
                    # add date and marks to a dictionary with index
                    # subject(multiple sections)
                    for i in multiple_marks:
                        multiple_one_marks.append(float(i.marks)/float(i.test.max_marks)*100)
                        multiple_time.append(i.testTaken)
                        subject_marks['SSCMultipleSections'] =\
                        {'marks':multiple_one_marks,'time':multiple_time}


           # get new tests to take (practise tests on the student page) 
            new_tests = me.toTake_Tests()
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
                       'hindihy_prediction': hindipredhy, 'mathshy_prediction': mathspredhy,
                       'englishhy_prediction': englishpredhy,
                       'sciencehy_prediction': sciencepredhy,
                       'maths1': mathst1, 'maths2': mathst2, 'maths3': mathst3,
                       'maths4': mathst4, 'hindi1': hindit1, 'hindi2': hindit2,
                       'hindi3': hindit3, 'hindi4': hindit4, 'english1': englisht1,
                       'english2': englisht2, 'english3': englisht3, 'english4': englisht4,
                       'science1': sciencet1, 'science2': sciencet2,
                       'science3': sciencet3, 'science4':
                       sciencet4,'announcements':my_announcements}
            context = \
                    {'profile':profile,'subjects':subjects,'subjectwiseMarks':subject_marks,'newTests':new_tests}

            return render(request, 'basicinformation/studentInstitute.html', context)
            #ssccoaching = School.objects.get(name='BodhiAI')
            #quests = SSCquestions.objects.all()
            #for i in quests:
            #    i.school.add(ssccoaching)

            #return HttpResponse(ssccoaching)


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
                for sub in subjects:
                    for i in klasses:
                        try:
                            weak_links[i]= \
                            me.online_problematicAreasNames(user,sub,i)
                            weak_subs.append(weak_links[i])
                            weak_klass.append(i)
                            subs.append(sub)
                        except Exception as e:
                            print(str(e))
                weak_subs_areas = list(zip(subs,weak_klass,weak_subs))
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

#def student_profile_page(request):
#    user = request.user
#    if user.is_authenticated:
#        if user.groups.filter(name='Students').exists():
#            if user.student.address and user.student.phone:
#                myProfile = StudentCustomProfile(


def student_select_topicTest(request):
    user = request.user
    if user.is_authenticated:
        if 'topicwisetest' in request.GET:
            topic = request.GET['topicwisetest']
            me = Studs(user)
            new_tests = me.toTake_Tests()
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




def student_self_analysis(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Teachers').exists():
            raise Http404(" This page is only meant for student to see.")
        elif user.groups.filter(name='Students').exists():
            me = Studs(user)
            #allSubjects = me.my_subjects_names()
            allSubjects = me.subjects_OnlineTest() 
            #print('%s -- online test subejcts' %subs)
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

            context = {'tests': tests,'subject':subject}
            return \
                render(request, 'basicinformation/student_self_sub_tests.html', context)
        if 'studentTestid' in request.GET:
            idandsubject = request.GET['studentTestid']
            test_id = idandsubject.split(',')[0]
            sub = idandsubject.split(',')[1]
            if me.institution == 'School':
                test = OnlineMarks.objects.get(student=user.student, test__id=test_id)
                student_type = 'School'
            elif me.institution == 'SSC':
                print(test_id)
                test = SSCOnlineMarks.objects.get(student=user.student, test__id=test_id)
                student_type = 'SSC'
            my_marks_percent = (test.marks / test.test.max_marks) * 100
            average, percent_average = \
                me.online_findAverageofTest(test_id, percent='p')
            percentile, all_marks = me.online_findPercentile(test_id)
            print('%s all amrks' %all_marks)
            all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]
            print('%s all amrks' %all_marks)
            freq = me.online_QuestionPercentage(test_id)
            ra,wa,sp,accuracy = me.test_statistics(test_id)
            weak_areas = me.weakAreas_Intensity(sub,singleTest = test_id)
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
                 'freq':
                 freq,'student_type':student_type,'topicWeakness':weak_names,'topicTiming':timing,
                 'numberRight':ra,'numberWrong':wa,'numberSkipped':sp,'accuracy':accuracy,'subjectwise_accuracy':subjectwise_accuracy}
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
       for i,j in freq:
            strongAreas.append(i)
            strongFreq.append(float(100-j))


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
        overall = me.plot_improvement(sub)
        outer = []
        innerid = []
        innertime = []
        innerpercent = []
        try:
            for k,v in overall.items():
                outer.append(k)
                innerpercent.append(overall[k]['percent'])
                innerid.append(overall[k]['testid'])
                innertime.append(overall[k]['time'])
        except:
            pass
        subject_progress = me.improvement(sub)
        context = {'overall':overall,'subjectProgress':subject_progress}
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


def write_questions(question,optA,optB,optC,optD,optE,image,correctOpt,questCategory,exp,sectionType,fouroptions=False):
    school = School.objects.filter(category = 'SSC',name = 'BodhiAI')
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
    new_questions.tier_category = '1'
    if sectionType == 'English':
        new_questions.section_category = 'English'
    elif sectionType == 'Resoning':
        new_questions.section_category = 'General-Intelligence'
    elif sectionType == 'Maths':
        new_questions.section_category = 'Quantitative-Analysis'
    elif sectionType == 'GK':
        new_questions.section_category = 'General-Knowledge'
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
            print('%s -- correctopt' %correctOpt)
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







