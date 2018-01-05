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
#from Private_Messages.models import *
from operator import itemgetter
from io import BytesIO as IO
import timeit

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

            # add students  (swami)
            df = \
            pd.read_csv('/app/question_data/swami2jan.csv',error_bad_lines =False)

            #df =\
            #pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/question_data/swami2jan.csv',error_bad_lines=False )
            name = df['Name']
            dob = df['DOB']
            batch = df['Batch no']
            username = df['Phone']
            password = df['password']
            stu = list(zip(name,dob,batch,username,password))
            real_create_student(stu,request)
            return HttpResponse(stu)

            #quad_questions = SSCquestions.objects.filter(section_category =\
            #                                             'Quantitative-Analysis',topic_category=22.1)
            #ch_list = []
            #for quest in quad_questions:
            #    kk = "none"
            #    for ch in quest.choices_set.all():
            #        if ch.text == kk:
            #            ch_list.append(ch.id)
            #        kk = ch.text
            #print(ch_list)
            #for c in ch_list:
            #    ch = Choices.objects.get(id = c)
            #    if ch.predicament == 'Correct':
            #       print(ch.text)
            #       rch = Choices.objects.get(id = c-1)
            #       rch.predicament = 'Correct'
            #       rch.save()
            #       ch.delete()
            #    try:
            #        ch.delete()
            #    except Exception as e:
            #        print(str(e))

            #df=\
            #pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/swamitestanswers.csv',error_bad_lines=False )
            #marks = df.ix[:,:]
            #marks = np.array(marks)
            #for n,i in enumerate(range(31)):
            #    opt = marks[1:,i]
            #    name = marks[0,i]
            #    evaluate_offline_test(name,opt)

  
               
                    
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
            #df=\
            #pd.read_csv('/app/question_data/swamiquestions.csv',error_bad_lines=False )
            ##df=\
            ##pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/question_data/swamiquestions.csv',error_bad_lines=False )
            #quests = []
            #optA = []
            #optB = []
            #optC = []
            #optD = []
            #optE = []
            #right_answer = []
            #quest_category = []
            #quests = df['Questions']
            #temp = []
            ##qu = 'Arrange the words below meaningfully\n'
            ##for i in quests:
            ##    i = str(qu) + str(i)
            ##    temp.append(i)


            ##images = df['QuestionLinks']
            ##images = None
            #optA = df['optionA']
            #optB = df['optionB']
            #optC = df['optionC']
            #optD = df['optionD']
            ##im = df['QuestionLink']
            ##optE = df['optionE'] 
            ##exp = df['Explanation']
            #quest_category = df['category']
            ##quest_category = '11.1' # indian museams
            #for i in df['Correct']:
            #    ichanged = str(i).replace(u'\\xa0',u' ')
            #    ichanged2 = ichanged.replace('Answer',' ')
            #    ichanged3 = ichanged2.replace('Explanation',' ')
            #    if 'A' in ichanged:
            #        right_answer.append(1)
            #    elif 'B' in ichanged:
            #        right_answer.append(2)
            #    elif 'C' in ichanged:
            #        right_answer.append(3)
            #    elif 'D' in ichanged:
            #        right_answer.append(4)
            #    elif 'E' in ichanged:
            #        right_answer.append(5)
            #print(len(quests))
            #print(len(optA))
            #print(len(optB))
            #print(len(optC))
            #print(len(optD))
            #print(len(right_answer))
            #print(len(quest_category))
            #for ind in range(len(optA)):
            #    #jprint('%s -- opta,%s -- optb,%s -- optc, %s -- optd,%s\
            #    #j -- right_answer,%s -- explanation'
            #    #j %(optA[ind],optB[ind],optC[ind],optD[ind],right_answer[ind],exp[ind]))

            #    write_questions(quests[ind],optA[ind],optB[ind],optC[ind],optD[ind],None,None,right_answer[ind],quest_category[ind],None,sectionType='Resoning',fouroptions=True)
            ##write_passages(all_passages)
            #print(quests)
            #print(right_answer)
            #print(optE)
            #return HttpResponse('hello')
            ##return render(request,'basicinformation/staffpage1.html')
            #return HttpResponse('hello')
        if user.groups.filter(name='Students').exists():
            profile = user.student
            me = Studs(request.user)
            subjects = me.my_subjects_names()

#------------------------------------------------------------
            ## testing for AI
            #online_marks = SSCOnlineMarks.objects.filter(student = profile)
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

                
                





#-------------------------------------------------------------
            # if B2C customer then add tests  to profile
            if profile.school.name == 'BodhiAI':
                bad_tests = SSCKlassTest.objects.filter(sub='')
                if bad_tests:
                    try:
                        for i in bad_tests:
                            i.delete()
                    except Exception as e:
                        print(str(e))

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
            all_ts = []
            for i in new_tests.items():
                all_ts.append(i)
            for n,i in enumerate(all_ts):
                print("%s --- %s" %(n,i))
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
            if me.profile.school.name == "BodhiAI":
                context = \
                        {'profile':profile,'subjects':subjects,'subjectwiseMarks':subject_marks,'newTests':new_tests,'allTs':all_ts}
            else:
                context = \
                    {'profile':profile,'subjects':subjects,'subjectwiseMarks':subject_marks,'newTests':new_tests,'allTs':all_ts}

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
            #tests = SSCKlassTest.objects.filter(creator=user)
            #test = SSCOfflineMarks.objects.filter(test__id = 49)
            #names = []
            #total_marks = []
            #score = []
            #rank = []
            #percentage = []
            #correct = []
            #incorrect = []
            #attempted = []
            #not_attempted = []
            #for i in test:
            #    names.append(i.student.name)
            #    total_marks.append(50)
            #    score.append(i.marks)
            #    percentage.append((i.marks/50)*100)
            #    correct.append(len(i.rightAnswers))
            #    incorrect.append(len(i.wrongAnswers))
            #    not_attempted.append(len(i.skippedAnswers))
            #score_rank = np.array(score)
            #temp = score_rank.argsort()
            #rank = np.empty(len(score_rank),int)
            #rank[temp] =  np.arange(len(score_rank))
            #final_rank = []
            #final_rank2 = []
            #for i in rank:
            #    final_rank.append(int(i+1))
            #for i in final_rank:
            #    final_rank2.append(32-i)
            #ran = list(zip(score,final_rank2))
            #score_card =\
            #list(zip(names,total_marks,score,final_rank2,percentage,correct,incorrect,not_attempted))
            ##data =\
            #[names,score,final_rank2,percentage,correct,incorrect,attempted,not_attempted]
            #data = score_card
            #df = pd.DataFrame(data)
            #df.to_csv('SwamiReasoningWorldNov16test.csv')

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


# gets tests of selected topic by the student on home page

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
            if me.profile.school.name == 'BodhiAI':
                allSubjects = me.subjects_OnlineTest() 
                allSubjects = me.already_takenTests_Subjects()
            else:
                allSubjects = me.my_subjects_names()
            if me.institution == 'SSC':
                analysis_types = ['Institute Tests Analysis', 'Online Test Analysis']
            else:
                analysis_types = ['School Tests Analysis', 'Online Test Analysis']
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
                    tests = OnlineMarks.objects.filter(test__sub=subject, student=user.student)
                elif me.institution == 'SSC':
                    tests = SSCOnlineMarks.objects.filter(test__sub=subject, student=user.student)

                context = {'tests': tests,'subject':subject}
                return \
                    render(request, 'basicinformation/student_self_sub_tests.html', context)
            elif mode == 'offline':
                if me.institution == 'School':
                    tests = OnlineMarks.objects.filter(test__sub=subject, student=user.student)
                elif me.institution == 'SSC':
                    tests = SSCOfflineMarks.objects.filter(test__sub=subject, student=user.student)
                context = {'tests': tests,'subject':subject}
                return \
                    render(request, 'basicinformation/student_self_sub_tests.html', context)

        if 'studentTestid' in request.GET:
            idandsubject = request.GET['studentTestid']
            test_id = idandsubject.split(',')[0]
            #visible_tests(test_id)
            sub = idandsubject.split(',')[1]
            if me.institution == 'School':
                test = OnlineMarks.objects.get(student=user.student, test__id=test_id)
                student_type = 'School'
            elif me.institution == 'SSC':
                try:
                    test = SSCOfflineMarks.objects.get(student=user.student, test__id=test_id)
                    mode = 'offline'
                except:
                    test = SSCOnlineMarks.objects.get(student=user.student, test__id=test_id)
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
#        if me.institution == 'SSC':
#            my_marks = SSCOnlineMarks.objects.filter(student =
#                                                     self.profile,test__sub = subject)
#            all_marks = SSCOnlineMarks.objects.filter(student= self.profile,test__sub =
#                                              'SSCMultipleSections')
#            offline_my_marks =SSCOfflineMarks.objects.filter(student=self.profile,test__sub=subject)
#            offline_all_marks =SSCOfflineMarks.objects.filter(student =
#                                                              self.profile,test__sub =
#                                               'SSCMultipleSections')
#
#            try:
#                weak_loader = SscStudentWeakAreaLoader.objects.get(student =
#                                                                   me.profile,subject
#                                                                   = subject)
#                saved_onlinesinglesub = weak_loader.lenonlineSingleSub
#                saved_onlinemultiplesub = weak_loader.lenonlineMultipleSub
#                saved_offlinesinglesub = weak_loader.lenofflineSingleSub
#                saved_offlinemultiplesub = weak_loader.lenofflineMultipleSub
#
#                if len(my_marks) == saved_onlinesinglesub and len(all_marks) ==
#                saved_onlinemultiplesub and len(offline_my_marks) ==
#                saved_offlinesinglesub and len(offline_all_marks) ==
#                saved_offlinemultiplesub:
#                    freq_category = weak_loader.topics
#                    freq_weakness = weak_loader.weakTopics
#                    freq = list(zip(freq_category,freq_weakness))
#                else:
#                    weak_loader.lenonlineSingleSub = len(my_marks)
#                    weak_loader.lenonlineMultipleSub = len(all_marks)
#                    weak_loader.lenofflineSingleSub = len(offline_my_marks)
#                    weak_loader.lenofflineMultipleSub = len(offline_all_marks)
#                    freq = me.weakAreas_IntensityAverage(subject)
#                    freq_cat = freq[:,0]
#                    freq_weakness = freq[:,1]
#                    weak_loader.topics = freq_cat
#                    weak_loader.weakTopics = freq_weakness
#                    timing_areawise,freq_timer = me.areawise_timing(subject)
#                    weak_loader.weakTiming = 0












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
            end = timeit.default_timer()
            before = timeit.default_timer()
            res = me.change_topicNumbersNamesWeakAreas(res,which_sub)
            end = timeit.default_timer()
            before = timeit.default_timer()
            timing,freq_timing = me.weakAreas_timing(user,which_sub,which_class)
            timing = me.change_topicNumbersNamesWeakAreas(timing,which_sub)
            end = timeit.default_timer()
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
                                                    sub,mode='BodhiOnline')
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

def real_create_student(stu, request):
    print('in process............')
    user = request.user
    school = School.objects.get(name='Swami Reasoning World')
    teacher = Teacher.objects.get(school__name = 'Swami Reasoning World')
    for na,dob,batch,phone,pa in stu:
        #ss = Student.objects.get(studentuser__username = phone)
        #print(ss.name)
        try:
            pa = str.lower(pa)
            dob = datetime.strptime(dob,'%d/%m/%Y')
            us = User.objects.create_user(username=phone,
                                          email='swamireasoning' + str(na) + '@gmail.com',
                                          password=pa)
            us.save()
            gr = Group.objects.get(name='Students')
            gr.user_set.add(us)
            if batch == 16:
                cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch16')
            elif batch == 17:
                 cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch17')
            elif batch == 24:
                  cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch24')
          
            stu = Student(studentuser=us, klass=cl,
                              rollNumber=phone,
                              name= na,
                              dob=dob,
                          pincode=int(str(302018)),school= school)
            stu.save()
            sub = Subject(name='General-Intelligence', student=stu,
                          teacher=teacher)
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
    school = School.objects.filter(category = 'SSC')
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
             






