from celery import shared_task
from rest_framework.response import Response
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .models import *
from learning.models import *
from QuestionsAndPapers.models import *
from Private_Messages.models import *
from django.utils import timezone
from more_itertools import unique_everseen
from django.http import Http404
from .marksprediction import *
from django.core import serializers
from django.core.mail import send_mail
import pandas as pd
import numpy as np 
from .views import * 
import pickle
import json
from django.db.models.signals import post_save
from notifications.api.views import *
from membership.models import *
from apiclient.discovery import build 
from apiclient.errors import HttpError 
from oauth2client.tools import argparser 
import pprint 
import boto3
import random
import requests
DEVELOPER_KEY = "AIzaSyDOW6Nt-1jpzxcEbypSpJ-ObCsZHjYBjPA" 
ACCESS_KEY_ID = 'AKIAJWLJN4TAFCMJWM2Q'
ACCESS_SECRET_KEY = '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'


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


@shared_task
def bring_teacher_subjects_analysis(user_id):
    user = User.objects.get(id=user_id)
    me = Teach(user)
    subject0 = me.my_subjects_names()
    subject1 = me.test_taken_subjects(user)
    sub = subject0 + subject1
    sub = list(unique_everseen(sub))
    return sub 
@shared_task
def evaluate_test(user_id,test_id,time_taken):
        # get values of test id and total test time
        user = User.objects.get(id = user_id)
        student_type = 'SSC'
        already_taken =\
        SSCOnlineMarks.objects.filter(student=user.student,test__id=test_id)
        if len(already_taken) > 0:
            raise Http404('You have already taken this test, Sorry retakes\
                          are not allowed')
        try:
            test = SSCKlassTest.objects.get(id = test_id)
        except Exception as e:
            print(str(e))
        online_marks = SSCOnlineMarks()
        quest_ids = []
        skipped_ids = []
        quest_ans_dict = {}
        online_marks.test = test
        online_marks.testTaken = timezone.now()
        online_marks.student = user.student
        for q in test.sscquestions_set.all():
            quest_ids.append(q.id)
        # iterate over all the questions in the test
        for i in quest_ids:
            try:
                answers_ids = []
                time_ids = []
                # get all the temporary holders and put the answer and time
                # in a dictionary and add skipped questions to a list
                temp_marks =\
                TemporaryAnswerHolder.objects.filter(stud=user.student,test__id=int(test_id),quests
                                                     =
                                                     str(i)).order_by('time')
                for j in temp_marks:
                    try:
                        answers_ids.append(int(j.answers))
                        time_ids.append(j.time)
                    except Exception as e:
                        pass 
                
                qad = {'answers':answers_ids,'time':time_ids}
                quest_ans_dict[i] = qad
        
                
            except Exception as e:
                pass
                skipped_ids.append(i)

        all_answers = []
        final_skipped = []
        final_correct = []
        final_wrong = []
        ra = []
        wa = []
        all_time = []
        num = 0
        # iterate over all the answer and time holding dictionary
        for k in quest_ans_dict.keys():
            for j in quest_ans_dict[k]:
                num = num +1
                try:
                    #final answer when more than one questions answered
                    final_ans = quest_ans_dict[k][j][-1] 
                    # if statement for weeding out the skipped(cleared
                    # selection) questions
                    if final_ans == -1:
                        pass
                    else:
                        # add time and answer ids to respective lists
                        # according to the keys of quest_ans_dict
                        if j == 'answers':
                            all_answers.append(final_ans)
                        elif j == 'time':
                            all_time.append(final_ans)

                except:
                    # same as above but runs only when one or none
                    # questions are answered
                    final_ans = quest_ans_dict[k][j]
                    if final_ans == -1:
                        pass
                    else:
                        if len(final_ans) == 0:
                            pass
                        else:
                            if num %2 == 0:
                                all_answers.append(final_ans)
                            else:
                                all_time.append(final_ans)
                

        test_marks = 0
        # evaluate the test
        for question in test.sscquestions_set.all():
            for choice in question.choices_set.all():
        # identify the skipped questions
                if not choice.id in all_answers:
                    final_skipped.append(question.id)
        # identify the correct answers and add marks to total marks
                elif choice.id in all_answers and choice.predicament == \
                "Correct":
                    final_correct.append(choice.id)
                    ra.append(question.id)
                    test_marks += question.max_marks
        # identify the wrong answers and subtract marks from total marks
                elif choice.id in all_answers and choice.predicament == \
                "Wrong":
                    final_wrong.append(choice.id)
                    wa.append(question.id)
                    test_marks -= question.negative_marks
            final_skipped = list(unique_everseen(final_skipped))
        final_skipped2=[]
        for an in final_skipped:
            if not an in ra and not an in wa:
                final_skipped2.append(an)
        # calculate the total time taken for the test
        try:
            time_taken = float(time_taken)
        except Exception as e:
            time_taken = float(100)

        try:
            total_time = (test.totalTime * 60)- time_taken
        except Exception as e:
            total_time = int(1000) - time_taken
        # save to SSCOnlinemarks
        try:
            online_marks.rightAnswers = final_correct
            online_marks.wrongAnswers = final_wrong
            online_marks.skippedAnswers = final_skipped2
            online_marks.allAnswers = all_answers
            online_marks.marks = test_marks
            online_marks.timeTaken = total_time
            online_marks.save()
        except Exception as e:
            pass
        num = 0
        # save question and time taken to solve the question
        for q in test.sscquestions_set.all():
            times = 0
            online_marks_quests = SSCansweredQuestion()
            online_marks_quests.onlineMarks = online_marks
            online_marks_quests.quest = q
            for ch in q.choices_set.all():
                if ch.id in all_answers:
                    online_marks_quests.time = all_time[num]
                    num = num +1
                else:
                    times = times +1
                    if times == len(q.choices_set.all()):
                        online_marks_quests.time = -1
            try:
                online_marks_quests.save()
            except Exception as e:
                pass
        # calculate time to send to template
        try:
            hours = int(total_time/3600)
            t = int(total_time%3600)
            mins = int(t/60)
            seconds =int(t%60)
            if hours == 0:
                tt = '{} minutes and {} seconds'.format(mins,seconds)
            if hours == 0 and mins == 0:
                tt = '{} seconds'.format(seconds)
            if hours > 0:
                tt = '{} hours {} minutes and {}\
                seconds'.format(hours,mins,seconds)
        except Exception as e:
            pass

        # delete the temporary holders
        try:
            TemporaryAnswerHolder.objects.filter(stud=user.student,test__id=int(test_id)).delete()
        except Exception as e:
            pass
        return test_id
@shared_task
def teacher_test_analysis_new(test_id,user_id):
    user = User.objects.get(id = user_id)
    me = Teach(user)

    result_loader = SscTeacherTestResultLoader()
    res_test = SSCKlassTest.objects.get(id=test_id)
    result_loader.test = res_test
    result_loader.teacher = me.profile
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
@shared_task 
def teacher_test_analysis_already(test_id,user_id):
    user = User.objects.get(id = user_id)
    me = Teach(user)
    result_loader = SscTeacherTestResultLoader.objects.get(test__id = test_id)
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
    test = SSCKlassTest.objects.get(id = test_id)
    result_loader.test = test
    result_loader.teacher = me.profile
    result_loader.save()
    online_marks =\
    SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                              me.profile.school)


    for i in online_marks:
        result_loader.onlineMarks.add(i)

@shared_task
def generate_testRankTable(user_id,test_id):
    user = User.objects.get(id = user_id)
    me = Teach(user)
    me.generate_rankTable(test_id)
@shared_task
def teacher_return_tests(user_id,subject,klass):
    user = User.objects.get(id = user_id)
    me = Teach(user)
    kl = me.my_classes_objects(klass)
    online_tests = SSCKlassTest.objects.filter(creator =
                                               user,klas=kl,sub=subject,mode='BodhiOnline').order_by('published')
    if len(online_tests) == 0 and subject == 'Defence-MultipleSubjects':
        online_tests = SSCKlassTest.objects.filter(creator = user,sub =
                                                   subject).order_by('published')
    tests = serializers.serialize('json',online_tests)
    return tests

@shared_task
def teacher_home_weak_areas(user_id):
    user = User.objects.get(id = user_id)
    me = Teach(user)
    klasses = me.my_classes_names()
    subjects = me.my_subjects_names()
    return klasses,subjects
    #weak_links = {}
    #weak_klass = []
    #weak_subs = []
    #subs = []
    #print('at 289')
    #try:
    #    for sub in subjects:
    #        for i in klasses:
    #            try:
    #                weak_links[i]= \
    #                me.online_problematicAreasNames(user,sub,i)
    #                weak_subs.append(weak_links[i])
    #                weak_klass.append(i)
    #                subs.append(sub)
    #            except Exception as e:
    #                print(str(e))
    #    print('at 301')
    #    weak_subs_areas = list(zip(subs,weak_klass,weak_subs))
    #    weak_subs_areas = serializers.serialize('json',weak_subs_areas)
    #    return weak_subs_areas
    #except:
    #    weak_subs_areas = None

@shared_task
def test_get_QuestionPosition(user_id,testid,pos):
    user = User.objects.get(id = user_id)
    test = SSCKlassTest.objects.get(id = testid)
    quest = []
    # gets the number of questions in the test
    try:
        test_detail = TestDetails.objects.get(test = test)
        how_many = test_detail.num_questions
        quests = test_detail.questions
        tosend = quests[int(pos)]
        
    except:
        for q in test.sscquestions_set.all():
            quest.append(q)
        how_many = len(quest)
        tosend = quest[int(pos)]
        tosend = tosend.id
    try:
    # if this question was already answered then send the selected
    # choice to template
        temp_marks = TemporaryAnswerHolder.objects.filter(stud =
                                                      user.student,test__id
                                                      =testid,quests=tosend).order_by('-time')


        Quests = []
        for i in temp_marks:
            # try except block to get attempted answer of already
            # skipped answers (otherwise throws an error)
            try:
                #answer_sel = i.answers
                Quests.append(int(i.answers))
                break
            except Exception as e:
                pass
        answer_sel = Quests[-1]
        return tosend,testid,answer_sel,how_many
    except:
        return tosend,testid,-5,how_many

@shared_task
def test_get_next_question(user_id,test_id,question_id,choice_id,questTime):
    user = User.objects.get(id = user_id)
    test = SSCKlassTest.objects.get(id = test_id)
    questnum = []
# get the number of questions in the test
    try:
        test_detail = TestDetails.objects.get(test = test)
        how_many = test_detail.num_questions
    except:
        for q in test.sscquestions_set.all():
            questnum.append(q)
        how_many = len(questnum)

    try:
        temp_marks = TemporaryAnswerHolder.objects.filter(stud =
                                                      user.student,test__id=int(test_id))
       
    except:
        pass
# saves choice to temporary holder 
    my_marks = TemporaryAnswerHolder()
    my_marks.stud = user.student
    my_marks.test = test
    my_marks.quests= question_id
    my_marks.answers = choice_id
    try:
        my_marks.time = int(questTime)
    except:
        my_marks.time = int(0)
    my_marks.save()

    
@shared_task
def create_Normaltest(user_id,which_klass,questions_list):
    if len(questions_list)!=0:
        user = User.objects.get(id = user_id)
        me = Teach(user)
        klass = me.my_classes_objects(which_klass)
        tot = 0 
        for i in questions_list:
            tot = tot + i.max_marks
        newClassTest = SSCKlassTest()
        newClassTest.max_marks = tot
        newClassTest.published = timezone.now()
        newClassTest.name = str(me.profile) + str(timezone.now())
        newClassTest.klas = klass
        newClassTest.creator = user
        newClassTest.save()
        for zz in questions_list:
            zz.ktest.add(newClassTest)
        return newClassTest.id


@shared_task
def publish_NormalTest(user_id,testid,date,time):
    user = User.objects.get(id = user_id)
    me = Teach(user)
    if date is None:
        date = timezone.now()
    myTest = SSCKlassTest.objects.get(id = testid)
    
    due_date = datetime.strptime(date, "%m/%d/%Y")
    myTest.due_date = due_date
    if time:
        myTest.totalTime = time
    else:
        myTest.totalTime = 10000
    if me.institution == 'School':
        for sub in myTest.questions_set.all():
            subject = sub.sub
            break
        myTest.sub = subject
    elif me.institution == 'SSC':
        subs = []
        kl = myTest.klas
        all_questions = []
        for sub in myTest.sscquestions_set.all():
            all_questions.append(sub.id)
            timesus = TimesUsed.objects.filter(teacher =
                                              me.profile,quest =
                                              sub,batch = kl)
            if len(timesus) == 1:
                for i in timesus:
                    i.numUsed = i.numUsed + 1
                    i.save()
                    
            else:
                tused = TimesUsed()
                tused.numUsed = 1
                tused.teacher = me.profile
                tused.quest = sub
                tused.batch = kl
                tused.save()

            subs.append(sub.section_category)
        subs = list(unique_everseen(subs))
        test_details = TestDetails()
        test_details.test = myTest
        test_details.num_questions = len(all_questions)
        test_details.questions = all_questions
        test_details.save()

        if len(subs)==1:
            myTest.sub = subs[0]
            kl = myTest.klas
            students = Student.objects.filter(klass = kl,school =
                                              me.profile.school)
            for i in students:
                subjs = Subject.objects.filter(teacher =
                                              me.profile,student=i,name
                                              = myTest.sub)
                if subjs:
                    studs = Student.objects.get(subject = subjs)
                    myTest.testTakers.add(studs)
                    myTest.save()

        else:
            students = Student.objects.filter(klass = kl,school = me.profile.school)
            for i in students:
                all_subs = []
                for su in subs:
                    subjs = Subject.objects.filter(teacher =
                                              me.profile,student=i,name
                                              = su)
                    all_subs.append(subjs)
                if len(all_subs) != 0:
                    for s in all_subs:
                        try:
                            studs = Student.objects.get(subject = s)
                            myTest.testTakers.add(studs)
                            myTest.save()
                        except:
                            pass
            if 'Defence-Physics' in subs or 'Defence-English' in\
            subs or 'Defence-GK-CA' in subs:
                myTest.sub = 'Defence-MultipleSubjects'
            elif 'JEE10' in subs[0]:
                myTest.sub = 'IITJEE10-MultipleSubjects'
            elif 'JEE11' in subs[0]:
                myTest.sub = 'IITJEE11-MultipleSubjects'
            elif 'JEE12' in subs[0]:
                myTest.sub = 'IITJEE12-MultipleSubjects'

            else:
                myTest.sub = 'SSCMultipleSections'
        
    myTest.mode = 'BodhiOnline'
    myTest.save()

@shared_task
def signup_mail(mail,name,institute = None):
    subject = 'Welcome to BodhiAI'
    from_email = 'prashantbodhi@gmail.com'
    to_email = mail
    if institute != None:
        contact_message = '''
        Hello %s ! Welcome to %s  app- powered By:BodhiAI,
        the best Score Improvement platform for students.
        I am Prashant from BodhiAI, and I hope 
        that you have a fantastic time here. 
        If you have any feedback, just drop an email to me 
        or phone me at: +91-7003973879.
        Thanks!!
        '''%(name,institute)
    else:
        contact_message = '''
        Hello %s ! Welcome to BodhiAI,
        the best score improvement platform for students.
        I am Prashant from BodhiAI, and I hope 
        that you have a fantastic time here. 
        If you have any feedback, just drop an email to me 
        or phone me at: +91-7003973879.
        Thanks!!
        '''%(name)
    send_mail(subject,contact_message,from_email,[to_email],fail_silently
                        = False)

@shared_task
def student_score_email(subject,score,name,email,time,fatherName,phone,address):
    
    subject = subject
    from_email = 'prashantbodhi@gmail.com'
    to_email = email
    to_mail2 = 'jitohostelkota@gmail.com'
    contact_message = '''
    Hello %s , Welcome to BodhiAI. 
    You recently took a test for JITO. 
    Here is your result:
    You got  %s
    Total time taken : %s

    Thankyou !!
    '''%(name,score,time)
    contact_message2 = '''
    Hello Jito Hostel , Thankyou for using BodhiAI, a student just took a test,
    here are his/her details: 
        Name : %s
        Father\'s name:%s
        Email:%s
        Phone: %s
        Marks: %s
        Address: %s
    '''%(name,fatherName,to_email,phone,score,address)


    send_mail(subject,contact_message,from_email,[to_email],fail_silently
                        = False)
    send_mail(subject,contact_message2,from_email,[to_mail2],fail_silently
                        = False)

@shared_task
def add_to_database_questions_text(sheet_link,school,production=False,explanation_quest=False):
        for sh in sheet_link:
            if production:
                df=\
                pd.read_csv('/app/question_data/jen_content/general_science/'+sh,error_bad_lines=False )
            else:
                df=\
                pd.read_csv('/home/ubuntu/bodhiai/question_data/kiran_maths/'+sh,error_bad_lines=False )

            quests = []
            optA = []
            optB = []
            optC = []
            optD = []
            optE = []
            right_answer = []
            quest_category = []
            temp = []
            used_for = 'English siel'
            lang = "English"
            source = "SIEL"
            quest_text = df['Question']
            optA = df['optA']
            num_a = len(optA)
            optB = df['optB']
            optC = df['optC']
            optD = df['optD']
            try:
                direction = df['Direction']
            except:
                direction =['lll']

            try:
                optE = df['optE']
            except:
                optE = ['lll']
            sectionType = "English"
            quest_category = df['cat_num']
            for i in df['correct']:
                ichanged = str(i).replace(u'\\xa0',u' ')
                ichanged2 = ichanged.replace('Answer',' ')
                ichanged3 = ichanged2.replace('Explanation',' ')

                if 'a'  in ichanged.lower() or '1' in ichanged.lower():
                    right_answer.append(1)
                elif 'b'  in ichanged.lower() or '2' in ichanged.lower():
                    right_answer.append(2)
                elif 'c'  in ichanged.lower() or '3' in ichanged.lower():
                    right_answer.append(3)
                elif 'd'  in ichanged.lower() or '4' in ichanged.lower():
                    right_answer.append(4)
                elif 'e'  in ichanged.lower() or '5' in ichanged.lower():
                    right_answer.append(5)
            print('%s num quest text' %len(quest_text))
            print('%s optA' %len(optA))
            print('%s optB' %len(optB))
            print('%s optC' %len(optC))
            print('%s optD' %len(optD))
            try:
                print('%s optE' %len(optE))

            except Exception as e:
                print(str(e))
            print('%s correct answers' %len(right_answer))
            print('%s number of categories' %len(quest_category))
            for ind in range(len(optA)):
                try:
                    if str(optE[ind]).lower() == 'noopt':
                        print('only four options')
                        if direction[0] != 'lll':
                            write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],optD[ind],None,None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'4',direction[ind])
                        else:
                            write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],optD[ind],None,None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'4')
                
                    else:
                        if direction[0] != 'lll':
                            write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],optD[ind],optE[ind],None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'5',direction[ind])
                        else:
                            write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],optD[ind],optE[ind],None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'5')


                except Exception as e:
                    print(str(e))
                    if str(optD[ind]).lower() == 'noopt':
                        print('only 3 options')
                        if direction[0] != 'lll':
                            write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],None,None,None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'3',direction[ind])
                        else:
                            write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],None,None,None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'3')

                    else:
                        if direction[ind] != 'lll':
                            write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],optD[ind],None,None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'4',direction[ind])
                        else:
                            write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],optD[ind],None,None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'4')

                        print('most 4 options')



@shared_task
def add_to_database_questions(sheet_link,school,production=False,onlyImage =
                              False,fiveOptions=False,explanation_quest=False):
        for sh in sheet_link:
            if production:
                df=\
                pd.read_csv('/home/ubuntu/bodhiai/question_data/jen_content/basic_science_ssc/'+sh,error_bad_lines=False )
            else:
                df=\
                pd.read_csv('/home/ubuntu/bodhiai/question_data/jen_content/basic_science_ssc/'+sh,error_bad_lines=False )

            quests = []
            optA = []
            optB = []
            optC = []
            optD = []
            optE = []
            right_answer = []
            quest_category = []
            temp = []
            optA = df['optA']
            optB = df['optB']
            optC = df['optC']
            optD = df['optD']
           
            try:
                direction = df['direction']
            except:
                direction = len(optD) * ['None']
            try:
                difficulty = df['difficulty']
            except:
                difficulty = len(optD) * ['None']
            used_for = df['usedFor']
            lang = df['lang']
            source = df['usedFor']
            if onlyImage:
                images = df['QuestionLink']
            else:
                quest_text = df['Question']
            sectionType = df['section_type']
            #direction = df['Direction']
            try:
                exp = df['explanation']
            except:
                exp = len(optD) * ['None']
            quest_category = df['category']
            for i in df['correct']:
                ichanged = str(i).replace(u'\\xa0',u' ')
                ichanged2 = ichanged.replace('Answer',' ')
                ichanged3 = ichanged2.replace('Explanation',' ')

                if 'a'  in ichanged.lower() or '1' in ichanged.lower():
                    right_answer.append(1)
                elif 'b'  in ichanged.lower() or '2' in ichanged.lower():
                    right_answer.append(2)
                elif 'c'  in ichanged.lower() or '3' in ichanged.lower():
                    right_answer.append(3)
                elif 'd'  in ichanged.lower() or '4' in ichanged.lower():
                    right_answer.append(4)
                elif 'e'  in ichanged.lower() or '5' in ichanged.lower():
                    right_answer.append(5)
            if fiveOptions:
                optE = df['optE']

            if onlyImage:
                print('%s num images' %len(images))
            else:
                print('%s num quest text' %len(quest_text))
            print('%s optA' %len(optA))
            print('%s optB' %len(optB))
            print('%s optC' %len(optC))
            print('%s optD' %len(optD))
            try:
                print('%s optE' %len(optE))
            except Exception as e:
                print(str(e))
            print('%s correct answers' %len(right_answer))
            print('%s number of categories' %len(quest_category))
            #print('%s languages ' %len(lang))
            print('%s sources' %len(source))
            print('%s sheet ' %sh)
            try:
                print('{} exp link'.format(len(exp)))
            except Exception as e:
                print('explanation not found')
   
            for ind in range(len(optA)):
                if onlyImage and fiveOptions:
                    write_questions(school,None,optA[ind],optB[ind],optC[ind],optD[ind],optE[ind],images[ind],right_answer[ind],quest_category[ind],exp[ind],sectionType[ind],str(lang[ind]),used_for[ind],source[ind],fouroptions='5',direction
                                    = direction[ind],difficulty= difficulty[ind] )
                else:

                #if onlyImage:
                    write_questions(school,None,optA[ind],optB[ind],optC[ind],optD[ind],None,images[ind],right_answer[ind],quest_category[ind],exp[ind],sectionType[ind],str(lang[ind]),used_for[ind],source[ind],fouroptions='4',direction
                                    = direction[ind],difficulty= difficulty[ind] )
                #else:
                #    write_questions(school,quest_text,optA[ind],optB[ind],optC[ind],optD[ind],None,None,right_answer[ind],quest_category[ind],None,sectionType[ind],lang[ind],used_for[ind],source[ind],direction[ind],fouroptions='3')








@shared_task
def\
write_questions(school,question,optA,optB,optC,optD,optE,image,correctOpt,questCategory,exp,sectionType,lang,used_for,source,fouroptions,direction=False,replace=False,difficulty=None):
    print('{} this is the exp link'.format(exp))
    try:
        old_question = SSCquestions.objects.get(picture=image)
        return
    except:
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
            if fouroptions == '4':
                all_options = [optA,optB,optC,optD]
            elif fouroptions == '3':
                all_options = [optA,optB,optC]
            elif fouroptions == '5':
                all_options = [optA,optB,optC,optD,optE]


            else:
                try:
                    if optE:
                        print('Found optE in final')
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
            new_questions.language = lang

            new_questions.usedFor = used_for

            if source:
                new_questions.source = source

            new_questions.tier_category = '1'
            new_questions.max_marks = int(1)
            new_questions.negative_marks = 0.0
            print('{} is the section cateogry'.format(sectionType))
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
            elif sectionType == 'jeeMaths10':
                new_questions.section_category = 'MathsIITJEE10'
            elif sectionType == 'jeeMaths11':
                new_questions.section_category = 'MathsIITJEE11'
            elif sectionType == 'jeeMaths12':
                new_questions.section_category = 'MathsIITJEE12'
            elif sectionType == 'jeePhysics10':
                new_questions.section_category = 'PhysicsIITJEE10'
            elif sectionType == 'jeePhysics11':
                new_questions.section_category = 'PhysicsIITJEE11'
            elif sectionType == 'jeePhysics12':
                new_questions.section_category = 'PhysicsIITJEE12'
            elif sectionType == 'jeeChemistry10':
                new_questions.section_category = 'ChemistryIITJEE10'
            elif sectionType == 'jeeChemistry11':
                new_questions.section_category = 'ChemistryIITJEE11'
            elif sectionType == 'jeeChemistry12':
                new_questions.section_category = 'ChemistryIITJEE12'
            elif sectionType == 'locopilot_electrical':
                new_questions.section_category = 'ElectricalLocoPilot'
            elif sectionType == 'locopilot_fitter':
                new_questions.section_category = 'FitterLocoPilot'
            elif sectionType == 'general_science':
                new_questions.section_category = 'General-Science'
            elif sectionType == 'locopilot_diesel':
                new_questions.section_category = 'LocoPilot_Diesel'
            elif sectionType.strip() == 'cat_quant':
                new_questions.section_category = 'CAT_Quantitative_Aptitude'
            elif sectionType.strip() == 'loco_civil':
                new_questions.section_category = 'Civil_Loco_Pilot_Tech'
            elif sectionType.strip() == 'ssc_electrical':
                new_questions.section_category = 'SSC_Electronics1'
            elif sectionType.strip() == 'BasicScienceLocopilot':
                new_questions.section_category = 'Basic-Science'
            elif sectionType.strip() == 'EnvironmentStudyLocopilot':
                new_questions.section_category = 'Environment-Study'
            elif sectionType.strip() == 'EngineeringDrawingLocopilot':
                new_questions.section_category = 'Engineering-Drawing'










            #if question != None:
            #    new_questions.text = str(question)
            print('%s direction, %s question' %(direction,question))
            if direction!='None' and question is None:
                new_questions.text = str(direction)
            elif question != None and direction:
                new_questions.text = str(direction) +'\n'+str(question)
            elif direction == None or direction == '' or direction == 'lll':
                new_questions.text = str(question)
            elif question and direction == False:
                new_questions.text = str(question)

            new_questions.topic_category = str(questCategory)
            if direction:
                try:
                    if direction != 'None' :
                        print('%s inside' %direction)
                        print(type(direction))
                        direct = Comprehension()
                        direct.picture = direction
                        direct.save()
                    else:
                        print('%s outside' %direction)
                except:
                    pass
            if difficulty:
                if difficulty != 'None':
                    new_questions.diffculty_category = difficulty
                else:
                    print('direction but something wrong')
            if image:
                new_questions.picture = image
                #try:
                #    new_questions.comprehension = direct
                #except:
                #    pass
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
                #if 'https:' in str(exp):
                #    pass
                #else:
                #    exptext = str(exp).replace('[','')
                #    exptext2 = exptext.replace(']','')
                #    exptext3 = exptext2.replace(u'\\xa0',u' ')
                #    exptext4 = exptext3.replace('\"','')
                if correctOpt == n+1:
                    new_choices.predicament = 'Correct'
                    #if 'https:' in str(exp):
                    new_choices.explanationPicture = exp
                    #else:
                    #    new_choices.explanation = exptext4
                else:
                    new_choices.predicament = 'Wrong'
                new_choices.save()
@shared_task
def allquestions_institute(subject,institute):
    sch = School.objects.get(name=institute)
    questions =\
    SSCquestions.objects.filter(section_category=subject,)
    for i in questions:
        i.school.add(sch)
    print('{} questions added to {}'.format(len(questions),institute))

@shared_task
def delete_sectionQuestions(section,school,topic = None):
    if topic:
        for tp in topic:
            questions = SSCquestions.objects.filter(section_category =
                                                section,school__name=school,topic_category =
                                               tp)
            print(len(questions))
            for i in questions:
                print('Deleting %s' %i.id)
                i.delete()
@shared_task
def addsubjects(school,batch,teacher):
    school = School.objects.get(name=school)
    batch = klass.objects.get(school=school,name=batch)
    students = Student.objects.filter(school=school,klass=batch)
    teacher = Teacher.objects.get(school=school,name=teacher)
    for i in students:
        sub = Subject()
        sub.teacher = teacher
        sub.name = 'SSC_Electronics1'
        sub.student = i
        sub.save()

@shared_task
def delete_allQuestions(school):
    questions =\
    SSCquestions.objects.filter(school__name=school,section_category='ElectricalLocoPilot',topic_category='1.1')
    for i in questions:
        i.delete()
    print('{} questions deleted'.format(len(questions)))

@shared_task
def ai_tukka_questions(user_id):
        user = User.objects.get(id = user_id)
        me = Teach(user)
        profile = user.teacher
        marks = SSCOnlineMarks.objects.filter(test__creator= user)
        questions = []

        for mark in marks:
            for chid in mark.rightAnswers:
                question = SSCquestions.objects.get(choices__id = chid)
                questions.append(question.id)
            for chid in mark.wrongAnswers:
                question = SSCquestions.objects.get(choices__id = chid)
                questions.append(question.id)
            for quid in mark.skippedAnswers:
                questions.append(quid)

        unique,counts = np.unique(questions,return_counts=True)
        cat_quests = np.asarray((unique,counts)).T
        right_answers = []
        wrong_answers = []
        skipped_answers = []
        tp_category = []
        for i,j in cat_quests:
            right = 0
            wrong = 0
            skipped = 0
            qu = SSCOnlineMarks.objects.filter(test__creator = user)
            for ma in qu:
                for chid in ma.rightAnswers:
                    quest_obj = SSCquestions.objects.get(choices__id = chid)
                    quid = quest_obj.id
                    if i == quid:
                        tp_category.append(quest_obj.topic_category)
                        print('right')
                        right = right + 1
                for chid in ma.wrongAnswers:
                    quest_obj = SSCquestions.objects.get(choices__id = chid)
                    quid = quest_obj.id
                    if i == quid:
                        tp_category.append(quest_obj.topic_category)
                        print('wrong')
                        wrong = wrong + 1
                if i in ma.skippedAnswers:
                    skipped = skipped + 1
                    que = SSCquestions.objects.get(id = i)
                    tp_category.append(que.topic_category)
                    print('skipped')
            right_answers.append(right)
            wrong_answers.append(wrong)
            skipped_answers.append(skipped)
        overall =\
        list(zip(cat_quests,right_answers,wrong_answers,skipped_answers,tp_category))
        overall = np.array(overall)
        print('found overall')
        df = pd.DataFrame(overall)
        df.to_csv("questions2.csv")

@shared_task
def Teacher_Classes(user_id):
    user = User.objects.get(id = user_id)
    me = Teach(user)
    klasses = me.my_classes_names()
    if len(klasses) != None:
        for kl in klasses:
            try:
                dc = TeacherClasses.objects.get(teacher = me.profile,klass=kl)
                print('found the classes')
            except:
                database_class = TeacherClasses()
                database_class.numStudents = 0
                database_class.klass = kl
                database_class.teacher = me.profile
                database_class.save()
                print('class not found but saved in database')


@shared_task
def ai_sharedTask(user_id):
    user = User.objects.get(id = user_id)
    me = Teach(user)
    my_students = Student.objects.filter(school = me.profile.school)
    subject = 'General-Intelligence'
    student_accuracy = {}
    all_sections = []
    all_quests = SSCquestions.objects.filter(section_category = subject)
    for i in all_quests:
        all_sections.append(i.topic_category)
        print(i.topic_category)

    all_sections = list(unique_everseen(all_sections))
    overall_dict = {}
    for which_student,student in enumerate(my_students):
        #sub = Subjects.objects.filter(teacher=
        #                              me.profile,name=subject,student=student)
        marks = SSCOnlineMarks.objects.filter(student= student,test__creator =
                                              user)
        acc_dict = {}
        for topic in all_sections:
            right = 0
            wrong = 0
            skipped = 0
            quest_count = 0
            right_timing = 0
            wrong_timing = 0
            all_right_questions = []
            all_wrong_questions = []
            all_skipped_questions = []
            all_marks_right = []
            all_marks_wrong = []
            attempt = 0
            for which_mark,mark in enumerate(marks):
                for chid in mark.rightAnswers:
                    quest = SSCquestions.objects.get(choices__id = chid)
                    all_right_questions.append(quest)
                    all_marks_right.append(mark)
                for chid in mark.wrongAnswers:
                    quest = SSCquestions.objects.get(choices__id = chid)
                    all_wrong_questions.append(quest)
                    all_marks_wrong.append(mark)
                for quid in mark.skippedAnswers:
                    quest = SSCquestions.objects.get(id = quid)
                    all_skipped_questions.append(quest)
        # find the number of tests attemped in a topic
                for q in mark.test.sscquestions_set.all():
                    if q.topic_category == str(topic):
                        attempt = attempt + 1
                        break
            


            for num,quest in enumerate(all_right_questions):
                if str(quest.topic_category) == str(topic):
                    try:

                        right_ind_time =\
                        SSCansweredQuestion.objects.get(onlineMarks =
                                                        all_marks_right[num],quest = quest)
                        right_ind_timing = right_ind_time.time
                        print('%s right timing' %right_ind_timing)
                    except Exception as e:
                        print(str(e))
                        right_ind_timing = 0
                    
                    right_timing = right_timing + right_ind_timing
                    right = right + 1
            for num2,quest in enumerate(all_wrong_questions):
                if str(quest.topic_category) == str(topic):
                    wrong = wrong + 1 
                    try:
                        wrong_ind_time = \
                        SSCansweredQuestion.objects.get(onlineMarks =
                                                        all_marks_wrong[num2],quest=quest)
                        wrong_ind_timing = wrong_ind_time.time
                        print('%s wrong timing' %wrong_ind_timing)
                    except Exception as e:
                        print(str(e))
                        wrong_ind_timing = 0
                    wrong_timing = wrong_timing + wrong_ind_timing
            for quest in all_skipped_questions:
                if str(quest.topic_category) == str(topic):
                    skipped = skipped + 1
            try:
                overall_right_timing = right_timing/len(all_right_questions)
            except:
                overall_right_timing = None
            try:
                overall_wrong_timing = wrong_timing/len(all_wrong_questions)
            except:
                overall_wrong_timing = None
            try:
                total_attempted = right + wrong + skipped
                only_attempted = right + wrong
                right_percent = (right / total_attempted)* 100
                wrong_percent = (wrong / total_attempted)* 100
                skipped_percent = (skipped / total_attempted)* 100
                only_right_percent = (right / only_attempted)* 100
                only_wrong_percent = (right / only_attempted)* 100

                accuracy = ((right - wrong) / (right + wrong))*100
                acc_dict[topic] =\
                        {'accuracy':accuracy,'skipped':skipped,'rightTiming':overall_right_timing,'wrongTiming':overall_wrong_timing,'RightPercentofTotal':right_percent,'WrongPercentofTotal':wrong_percent,'SkippedPercent':skipped_percent,'RightPercentAttempted':only_right_percent,'WrongPercentAttempted':only_wrong_percent,'TotalAppeared':total_attempted,'TestAttempted':attempt}
            except:
                accuracy = None

        overall_dict[student.id] = acc_dict
        dump_file = json.dumps(overall_dict)

    with open('student_details.pickle','wb') as od:
        pickle.dump(overall_dict,od)

#@shared_task
#def ai_average_timing(user_id):
#    user = User.objects.get(id = user_id)
#    me = Teach(user)
#    my_students = Student.objects.filter(school = me.profile.school)
#    subject = 'General-Intelligence'
#    all_quests = SSCquestions.objects.filter(section_category = subject)
#    for i in all_quests:
#        all_sections.append(i.topic_category)
#        print(i.topic_category)
#
#    all_sections = list(unique_everseen(all_sections))
#    for topic in all_sections:


#__________________________________________________________________________________________--
# All APIs
@shared_task
def TeacherWeakAreasBriefAsync(user_id):
    user = User.objects.get(id = user_id)
    me = Teach(user)
    try:
        saved_areas = TeacherBatchWeakAreas.objects.filter(teacher =
                                                    me.profile).order_by('-date')[0]

        latest_test = SSCOnlineMarks.objects.filter(test__creator =
                                             user).order_by('-test__published')[0]
        if latest_test.test.published <= saved_areas.date:
            final = []
            weak_response = {}
            all_saved_areas =\
            TeacherBatchWeakAreas.objects.filter(teacher=me.profile,date=saved_areas.date)
            for sar in all_saved_areas:
                weak_response =\
                {'subject':sar.subject,'klass':sar.batch,'weakTopics':sar.weak_sections}
                final.append(weak_response)
            weak_subs_areas_serialized = pickle.dumps(final,protocol = 0)
            wsas = weak_subs_areas_serialized.decode('utf-8')
            return wsas
        else:
            subjects = me.my_subjects_names()
            weak_subs_areas_dict = []
            teach_klass = TeacherClasses.objects.filter(teacher=me.profile)
            klasses = []
            if len(teach_klass) != 0:
                for kl in teach_klass:
                    klasses.append(kl.klass)
            else:
                klasses = me.my_classes_names()
                for kl in klasses:
                    new_teach_klass = TeacherClasses()
                    new_teach_klass.teacher = me.profile
                    new_teach_klass.klass = kl
                    new_teach_klass.numStudents = 0
                    new_teach_klass.save()


            final = []
            weak_response = {}
            weak_links = {}
            weak_klass = []
            weak_subs = []
            subs = []
            try:
                for num,sub in enumerate(subjects):
                    for i in klasses:
                        try:
                            weak_links[i]= \
                            me.online_problematicAreasNames(user,sub,i)
                            weak_response =\
                            {'subject':sub,'klass':i,'weakTopics':weak_links[i]}
                            new_saved_area = TeacherBatchWeakAreas()
                            new_saved_area.batch = i
                            new_saved_area.subject = sub
                            new_saved_area.weak_sections =\
                            weak_links[i].tolist()
                            new_saved_area.teacher = me.profile
                            new_saved_area.save()
                            final.append(weak_response)
                        except Exception as e:
                            print(str(e))
            except:
                pass
            
            weak_subs_areas_serialized = pickle.dumps(final,protocol = 0)
            wsas = weak_subs_areas_serialized.decode('utf-8')
            return wsas



    except Exception as e:
        print(str(e))
        subjects = me.my_subjects_names()
        weak_subs_areas_dict = []
        teach_klass = TeacherClasses.objects.filter(teacher=me.profile)
        klasses = []
        if len(teach_klass) != 0:
            for kl in teach_klass:
                klasses.append(kl.klass)
        else:
            klasses = me.my_classes_names()
            for kl in klasses:
                new_teach_klass = TeacherClasses()
                new_teach_klass.teacher = me.profile
                new_teach_klass.klass = kl
                new_teach_klass.numStudents = 0
                new_teach_klass.save()


        final = []
        weak_response = {}
        weak_links = {}
        weak_klass = []
        weak_subs = []
        subs = []
        try:
            for num,sub in enumerate(subjects):
                for i in klasses:
                    try:
                        weak_links[i]= \
                        me.online_problematicAreasNames(user,sub,i)
                        weak_response =\
                        {'subject':sub,'klass':i,'weakTopics':weak_links[i]}
                        new_saved_area = TeacherBatchWeakAreas()
                        new_saved_area.batch = i
                        new_saved_area.subject = sub
                        new_saved_area.weak_sections =\
                        weak_links[i].tolist()
                        new_saved_area.teacher = me.profile
                        new_saved_area.save()
                        final.append(weak_response)
                    except Exception as e:
                        pass
        except:
            pass
        
        weak_subs_areas_serialized = pickle.dumps(final,protocol = 0)
        wsas = weak_subs_areas_serialized.decode('utf-8')
        return wsas




#@shared_task
#def online_problematicAreasAsync(user_id,subject,klass):
#        user = User.objects.get(id = user_id)
#        if self.institution == 'School':
#            online_marks = OnlineMarks.objects.filter(test__creator= user,test__sub=
#                                                  subject,test__klas__name = klass)
#        elif self.institution == 'SSC':
#            online_marks = SSCOnlineMarks.objects.filter(test__creator= user,test__sub=
#                                                  subject,test__klas__name = klass)
#
#            if 'Defence' in klass:
#                all_onlineMarks = SSCOnlineMarks.objects.filter(test__creator =
#                                                                user,test__sub =
#                                                                'Defence-MultipleSubjects',test__klas__name=
#                                                                klass)
#            else:
#
#                all_onlineMarks = SSCOnlineMarks.objects.filter(test__creator =
#                                                                user,test__sub =
#                                                                'SSCMultipleSections',test__klas__name=
#                                                                klass)
#            offline_marks = SSCOfflineMarks.objects.filter(test__creator =
#                                                           user,test__sub =
#                                                           subject,test__klas__name
#                                                           = klass)
#
#            all_offlinemarks = SSCOfflineMarks.objects.filter(test__creator =
#                                                               user,test__sub =
#                                                               'SSCMultipleSections',test__klas__name
#                                                            = klass)
#
#        wrong_answers = []
#        skipped_answers = []
#        if online_marks:
#            for om in online_marks:
#                for wa in om.wrongAnswers:
#                    wrong_answers.append(wa)
#                for sp in om.skippedAnswers:
#                    skipped_answers.append(sp) 
#            
#            
#        if all_onlineMarks:
#            for om in all_onlineMarks:
#                for wa in om.wrongAnswers:
#                    wrong_answers.append(wa)
#                for sp in om.skippedAnswers:
#                    skipped_answers.append(sp)
#        if offline_marks:
#            for om in offline_marks:
#                for wa in om.wrongAnswers:
#                    wrong_answers.append(wa)
#                for sp in om.skippedAnswers:
#                    skipped_answers.append(sp) 
#        if all_offlinemarks:
#            for om in all_offlinemarks:
#                for wa in om.wrongAnswers:
#                    wrong_answers.append(wa)
#                for sp in om.skippedAnswers:
#                    skipped_answers.append(sp)
#
#
#        wq = []
#        for i in wrong_answers:
#            if self.institution == 'School':
#                qu = Questions.objects.get(choices__id = i)
#            elif self.institution == 'SSC':
#                try:
#                    qu = SSCquestions.objects.get(choices__id = i)
#                except Exception as e:
#                    print(str(e))
#                    continue
#            if qu.section_category == subject:
#                quid = qu.id
#                wq.append(quid)
#        for i in skipped_answers:
#            if self.institution == 'School':
#                try:
#                    qu = Questions.objects.get(id = i)
#                except Exception as e:
#                    print(str(e))
#                    continue
#            elif self.institution == 'SSC':
#                try:
#                    qu = SSCquestions.objects.get(id = i)
#                except Exception as e:
#                    print(str(e))
#                    continue
#            if qu.section_category == subject:
#                quid = qu.id
#                wq.append(quid)
#
#        unique, counts = np.unique(wq, return_counts=True)
#        waf = np.asarray((unique, counts)).T
#        nw_ind = []
#        kk = np.sort(waf,0)[::-1]
#        for u in kk[:,1]:
#            for z,w in waf:
#                if u == w:
#                    if z in nw_ind:
#                        continue
#                    else:
#                        nw_ind.append(z)
#                        break
#        final_freq = np.asarray((nw_ind,kk[:,1])).T
#        final_freq_serialized = pickle.dumps(final_freq,protocol = 0)
#        wsas = final_freq_serialized.decode('utf-8')
#        return ff_serialized


@shared_task
def TeacherHardQuestionsAsync(user_id):
    user = User.objects.get(id = user_id)
    my_tests_marks = SSCOnlineMarks.objects.filter(test__creator =
                                                   user)

    all_wrong_answers = []
    for mark in my_tests_marks:
        if mark.wrongAnswers:
            for choiceid in mark.wrongAnswers:
                try:
                    question = SSCquestions.objects.get(choices__id = choiceid)
                except:
                    continue
                all_wrong_answers.append(question.id)

    unique,counts = np.unique(all_wrong_answers,return_counts = True)
    hard_quests_freq = np.asarray((unique,counts)).T
    hard_quests_freq_final = np.sort(hard_quests_freq,0)[::1]
    hard_quest_ids = hard_quests_freq_final[-10:]
    text = []
    picture = []
    choice = []
    wrong_freq = []
    all_questions = []
    for i,j in hard_quest_ids:
        choices_list = []
        question = SSCquestions.objects.get(id = i)
        text.append(question.text)
        picture.append(question.picture)
        choices = Choices.objects.filter(sscquest = question)
        for ch in choices:
            if ch.text:
                choices_list.append(ch.text)
            elif ch.picture:
                choices_list.append(ch.picture)
        choice.append(choices_list)
        wrong_freq.append(j)
        hard_quest_dict =\
        {'text':question.text,'picture':question.picture,'choices':choices_list,'wrong_frequency':int(j)}
        all_questions.append(hard_quest_dict)
    return all_questions
 
@shared_task
def TeacherHardQuestionsLast3TestsAsync(user_id):
    user = User.objects.get(id = user_id)
    last_three_tests = SSCKlassTest.objects.filter(creator =
                                                   user).order_by('-published')
    all_marks = []
    all_questions = []
    cont = 0
    for counter,ltt in enumerate(last_three_tests):
        if cont ==3 :
            break
        online_tests = SSCOnlineMarks.objects.filter(test =
                                                 ltt)
        if len(online_tests) == 0:
            continue
        else:
            cont = cont + 1
            wrong_quests_test = []
            for te in online_tests:
                date =te.test.published
                if te.wrongAnswers:
                    for choiceid in te.wrongAnswers:
                        try:
                            question = SSCquestions.objects.get(choices__id = choiceid)
                        except:
                            continue
                        wrong_quests_test.append(question.id)


            unique,counts = np.unique(wrong_quests_test,return_counts = True)
            hard_quests_freq = np.asarray((unique,counts)).T
            hard_quests_freq_final = np.sort(hard_quests_freq,0)[::1]
            hard_quest_ids = hard_quests_freq_final[-3:]
            text = []
            picture = []
            choice = []
            wrong_freq = []
            for i,j in hard_quest_ids:
                choices_list = []
                try:
                    question = SSCquestions.objects.get(id = i)
                    text.append(question.text)
                    picture.append(question.picture)
                    choices = Choices.objects.filter(sscquest = question)
                    for ch in choices:
                        if ch.text:
                            choices_list.append(ch.text)
                        elif ch.picture:
                            choices_list.append(ch.picture)
                    choice.append(choices_list)
                    wrong_freq.append(j)
                    hard_quest_dict =\
                            {'text':question.text,'picture':question.picture,'choices':choices_list,'wrong_frequency':int(j),'date':date}
                    all_questions.append(hard_quest_dict)

                except:
                    pass
    return all_questions[::-1]



@shared_task
def deleteBadTests():
    quest_bad = SSCKlassTest.objects.all()
    for quest in quest_bad:
        if quest.sub == "":
            quest.delete()
        if len(quest.sscquestions_set.all()) == 0:
            quest.delete()
        if quest.totalTime == 0:
            quest.delete()
@shared_task
def add_questions(institute,section):
    if institute == 'JEN':
        questions = SSCquestions.objects.filter(school__name =
                                                'BodhiAI',section_category
                                                = 'Basic-Science')
        school = School.objects.get(name=institute)
        print('%s --num quests' %len(questions))
        for i in questions:
            i.school.add(school)
    if institute == 'YSM':
        if section == 'English':
            copy_institute = 'SIEL'
        else:
            copy_institute = 'BodhiAI'
        questions = SSCquestions.objects.filter(school__name =
                                                copy_institute,section_category
                                                = section)
        school = School.objects.get(name=institute)
        print('%s --num quests' %len(questions))
        for i in questions:
            i.school.add(school)

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
    elif institute == 'Swami Reasoning World':
       questions = SSCquestions.objects.filter(school__name =
                                               'BodhiAI',section_category=section)
       school = School.objects.get(name = institute)
       print('%s --num quests' %len(questions))
       for i in questions:
           i.school.add(school)
       
    else:
        print('here in jito')
        questions =\
        SSCquestions.objects.filter(section_category=section)
        school = School.objects.get(name = institute)
        print(len(questions))
        for i in questions:
            i.school.add(school)
        print('%s num questions' %len(questions))


@shared_task
def add_png():
    questions = SSCquestions.objects.all()
    for i in questions:
        if i.picture:
            if i.picture.endswith('.png'):
                pass
            else:
                print('found without png')
                url = i.picture + '.png'
                i.picture = url
                i.save()

@shared_task
def addOldTests(stud_id,teacher_id,kl):
    student = Student.objects.get(id = stud_id)
    teacher = Teacher.objects.get(id = teacher_id)
    batch = klass.objects.get(id = kl)
    print(student,teacher,batch)
    all_tests = SSCKlassTest.objects.filter(creator = teacher.teacheruser,klas
                                            = batch)
    print('{} tests found'.format(len(all_tests)))
    for i in all_tests:
        i.testTakers.add(student)
   
@shared_task
def CreateOneClickTestFinal(user_id,batch,subject,quest_ids,patternTest =False):
        user = User.objects.get(id = user_id)
        me = Teach(user)
        test = SSCKlassTest()
        test_quest = []
        if patternTest:
            test.name = 'pattern_test'+str(me.profile)+str(batch)
        else:
            test.name=str('oneclick')+str(me.profile)+str(batch)+str(timezone.now())
        test.mode = 'BodhiOnline'
        marks = 0
        if patternTest:
            for qu in quest_ids:
                quest = SSCquestions.objects.get(id = qu)
                test_quest.append(quest)
        else:
            quest_ids1 = quest_ids.replace('[','')
            quest_ids2 = quest_ids1.replace(']','')
            quest_ids_list = quest_ids2.split(',')
            print('{} quests list'.format(quest_ids_list))
            for qu in quest_ids_list:
                qu = qu.strip()
                qid = int(qu)
                quest = SSCquestions.objects.get(id = qid)
                test_quest.append(quest)
        for qu in test_quest:
            marks += qu.max_marks
        test.max_marks = marks
        test.course = 'SSC'
        test.creator = user
        test.sub = subject
        if patternTest:
            test.pattern_test = True
        kl = klass.objects.get(school = me.my_school(),name= batch)
        test.klas = kl
        totalTime = len(test_quest)*0.6 # one question requires 36 secs
        print('{} total time of test, {} for batch'.format(totalTime,kl))
        test.totalTime = totalTime
        test.save()
        # add questions to testpaper
        for q in test_quest:
            try:
                # modify times used object associated with each question as
                # they are added to the test paper
                times_used = TimesUsed.objects.get(batch =
                                               kl,quest=q,teacher=me.profile)
                times_used.numUsed += 1
                times_used.save()
            except:
                # if new question then create the TimesUsed object for that
                # question
                times_used = TimesUsed()
                times_used.batch = kl
                times_used.numUsed =1
                times_used.quest = q
                times_used.teacher = me.profile
                times_used.save()
            
            # add many to many field of question to specific test
            q.ktest.add(test)

        # getting all the students in a specific class to be given the test
        # to
        students = Student.objects.filter(klass = kl,school =
                                          me.my_school())
        # add testtakers(students of a specific batch) to test paper
        for st in students:
            test.testTakers.add(st)
            test.save()


@shared_task
def CreateUpdateStudentAverageTimingDetail(student_id,subject,mark_id):
    student = Student.objects.get(id = student_id)
    this_marks = SSCOnlineMarks.objects.get(id = mark_id)
    chapters = []
    for quest in this_marks.test.sscquestions_set.all():
        chapters.append(quest.topic_category)
    chapters = list(unique_everseen(chapters))
    for chapter in chapters:

        try:
            timing_cache = StudentAverageTimingDetailCache.objects.get(student =
                                                                     student,subject
                                                                     =
                                                                     subject,chapter
                                                                     =
                                                                       str(chapter))

            old_right_ave = timing_cache.rightAverage
            old_wrong_ave = timing_cache.wrongAverage
            old_total_attempted = timing_cache.totalAttempted
            old_total_ids = timing_cache.allMarksIds
            old_right_total = timing_cache.rightTotalTime
            old_wrong_total = timing_cache.wrongTotalTime
            old_total_right = timing_cache.rightTotal
            old_total_wrong = timing_cache.wrongTotal
            old_total_average = timing_cache.totalAverage



            right_time = []
            wrong_time = []
            for rid in this_marks.rightAnswers:
                quest = SSCquestions.objects.get(choices__id = rid)
                if quest.section_category == subject and quest.topic_category\
                == chapter:
                    answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                               this_marks,quest=quest)
                    right_time.append(answered.time)
            for wid in this_marks.wrongAnswers:
                quest = SSCquestions.objects.get(choices__id = wid)
                if quest.section_category == subject and quest.topic_category\
                == chapter:
                    answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                               this_marks,quest=quest)
                    wrong_time.append(answered.time)
            len_right = len(right_time)
            len_wrong = len(wrong_time)
            total = len_right +  len_wrong
            if total == 0:
                return
            if len_right == 0:
                ave_right = 0
            else:
                ave_right = sum(right_time) / len_right
            if len_wrong == 0:
                ave_wrong = 0
            else:
                ave_wrong = sum(wrong_time) / len_wrong
            new_right_total = len_right + old_total_right
            new_wrong_total = len_wrong + old_total_wrong
            new_average_right = sum(right_time) + old_right_total
            new_average_wrong = sum(wrong_time) + old_wrong_total
            new_right_average_timing = new_average_right / new_right_total
            new_wrong_average_timing = new_average_wrong / new_wrong_total
            new_total_attempted = total + old_total_attempted
            new_average_total = (old_total_average / new_total_attempted)
            timing_cache.rightTotal = new_right_total
            timing_cache.wrongTotal = new_wrong_total
            timing_cache.totalAttempted = new_total_attempted
            timing_cache.rightTotalTime = new_average_right
            timing_cache.wrongTotalTime = new_average_wrong
            timing_cache.rightAverage = new_right_average_timing
            timing_cache.wrongAverage = new_wrong_average_timing
            timing_cache.totalAverage = new_average_total
            timing_cache.save()

        except Exception as e:
            print(str(e))

            right_time = []
            wrong_time = []
            for rid in this_marks.rightAnswers:
                quest = SSCquestions.objects.get(choices__id = rid)
                if quest.section_category == subject and quest.topic_category\
                == chapter:
                    answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                               this_marks,quest=quest)
                    right_time.append(answered.time)
            for wid in this_marks.wrongAnswers:
                quest = SSCquestions.objects.get(choices__id = wid)
                if quest.section_category == subject and quest.topic_category\
                == chapter:
                    answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                               this_marks,quest=quest)
                    wrong_time.append(answered.time)
            len_right = len(right_time)
            len_wrong = len(wrong_time)
            total = len_right + len_wrong
            if total == 0:
                return
            if len_right == 0:
                ave_right = 0
            else:
                ave_right = sum(right_time) / len_right
            if len_wrong == 0:
                ave_wrong = 0
            else:
                ave_wrong = sum(wrong_time) / len_wrong
            print('{} averageright,{} ave wrong'.format(ave_right,ave_wrong))
            new_timing_cache = StudentAverageTimingDetailCache()
            new_timing_cache.student = student
            new_timing_cache.chapter = chapter
            new_timing_cache.subject = subject
            new_timing_cache.rightAverage = ave_right
            new_timing_cache.wrongAverage = ave_wrong
            new_timing_cache.totalAttempted = len_right + len_wrong
            new_timing_cache.totalAverage = ((sum(right_time) + sum(wrong_time))/(total))

            new_timing_cache.rightTotal = int(len_right)
            new_timing_cache.wrongTotal = int(len_wrong)
            new_timing_cache.rightTotalTime = sum(right_time)
            new_timing_cache.wrongTotalTime = sum(wrong_time)
            new_timing_cache.save()
@shared_task
def CreateCacheForTimingDetail(student_id,subject,chapter):
        student = Student.objects.get(id = student_id)
        marks = SSCOnlineMarks.objects.filter(student=student,test__sub = subject)
        if len(marks) != 0:
            try:
                cache = StudentAverageTimingDetailCache.objects.get(subject
                                                                    =subject,chapter
                                                                    =
                                                                    chapter,student
                                                                    = student)
                return
            except:
                right_time = []
                wrong_time = []
                for ma in marks:
                    for rid in ma.rightAnswers:
                        quest = SSCquestions.objects.get(choices__id = rid)
                        if quest.section_category == subject and quest.topic_category\
                        == chapter:
                            answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                                       ma,quest=quest)
                            right_time.append(answered.time)
                    for wid in ma.wrongAnswers:
                        quest = SSCquestions.objects.get(choices__id = wid)
                        if quest.section_category == subject and quest.topic_category\
                        == chapter:
                            answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                                       ma,quest=quest)
                            wrong_time.append(answered.time)
                len_right = len(right_time)
                len_wrong = len(wrong_time)
                total = len_right + len_wrong
                if total == 0:
                    return
                if len_right == 0:
                    ave_right = 0
                else:
                    ave_right = sum(right_time) / len_right
                if len_wrong == 0:
                    ave_wrong = 0
                else:
                    ave_wrong = sum(wrong_time) / len_wrong
                print('{} averageright,{} ave wrong'.format(ave_right,ave_wrong))
                new_timing_cache = StudentAverageTimingDetailCache()
                new_timing_cache.student = student
                new_timing_cache.chapter = chapter
                new_timing_cache.subject = subject
                new_timing_cache.rightAverage = ave_right
                new_timing_cache.wrongAverage = ave_wrong
                new_timing_cache.totalAttempted = len_right + len_wrong
                new_timing_cache.rightTotal = int(len_right)
                new_timing_cache.wrongTotal = int(len_wrong)
                new_timing_cache.totalAverage = ((sum(right_time) +
                                                  sum(wrong_time))
                                                 /(total))
                new_timing_cache.rightTotalTime = sum(right_time)
                new_timing_cache.wrongTotalTime = sum(wrong_time)
                new_timing_cache.save()

@shared_task
def delete_timing_cache():
    cache = StudentAverageTimingDetailCache.objects.all()[:500000]
    print('{} len of cache'.format(len(cache)))
    for i in cache:
        i.delete()
        print('i deleted')
@shared_task
def create_timing_cache_detail():
    students = Student.objects.filter(school__name="JEN")
    for n,student in enumerate(students):
        print('{} -- calculating for {}'.format(n,student))
        subjects = student.subject_set.all()
        u_subjects = []
        for i in subjects:
            u_subjects.append(i.name)
        unique_subjects = list(unique_everseen(u_subjects))

        for subject in unique_subjects:
            chapters = get_chapters(subject)
            for chapter in chapters:
                CreateCacheForTimingDetail.delay(student.id,subject,chapter)



@shared_task
def CreateUpdateStudentWeakAreas(student_id,subject,mark_id):
    student = Student.objects.get(id = student_id)
    marks = SSCOnlineMarks.objects.get(id = mark_id)
    chapters = []
    for quest in marks.test.sscquestions_set.all():
        chapters.append(quest.topic_category)

    chapters =list(unique_everseen(chapters))
    for chapter in chapters:
        try:
            old_cache =\
                    StudentWeakAreasChapterCache.objects.get(student = student,
                                                             subject =
                                                             subject,chapter =
                                                             str(chapter))
            old_total_right = old_cache.totalRight
            old_total_wrong = old_cache.totalWrong
            old_skipped = old_cache.totalSkipped
            old_total_accuracy = old_cache.accuracy
            old_total_attempted = old_cache.totalAttempted
            right = 0
            wrong = 0
            skipped = 0
            for quest_id in marks.rightAnswers:
                quest = SSCquestions.objects.get(choices__id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chapter:
                    right += 1
            for quest_id in marks.wrongAnswers:
                quest = SSCquestions.objects.get(choices__id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chapter:
                    wrong += 1
            for quest_id in marks.skippedAnswers:
                quest = SSCquestions.objects.get(id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chapter:
                    skipped += 1
            total_attempted = right + wrong
            all_questions_attempted = total_attempted + skipped
            if all_questions_attempted == 0:
                return 
            if total_attempted == 0:
                accuracy = 0
            else:
                accuracy = (right / (total_attempted))* 100

            new_total_right = old_total_right + right
            new_total_wrong = old_total_wrong + wrong
            new_total_attempted = old_total_attempted + total_attempted
            new_total_skipped = old_skipped + skipped
            new_skipped_percent = (new_total_skipped /(new_total_attempted+all_questions_attempted))*100
            new_total_accuracy = (new_total_right / new_total_attempted)*100
            old_cache.totalRight = new_total_right
            old_cache.totalWrong = new_total_wrong
            old_cache.totalSkipped = new_total_skipped
            old_cache.skippedPercent = new_skipped_percent
            old_cache.accuracy = new_total_accuracy
            old_cache.totalAttempted = new_total_attempted
            old_cache.save()
        except Exception as e:
            print(str(e))
            right = 0
            wrong = 0
            skipped = 0
            for quest_id in marks.rightAnswers:
                quest = SSCquestions.objects.get(choices__id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chapter:
                    right += 1
            for quest_id in marks.wrongAnswers:
                quest = SSCquestions.objects.get(choices__id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chapter:
                    wrong += 1
            for quest_id in marks.skippedAnswers:
                quest = SSCquestions.objects.get(id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chapter:
                    skipped += 1
            total_attempted = right + wrong
            all_questions_attempted = total_attempted + skipped
            if all_questions_attempted == 0:
                return 
            if total_attempted == 0:
                accuracy = 0
            else:
                accuracy = (right / (total_attempted))* 100
            skippedPercent = (skipped / (all_questions_attempted))*100

            new_cache = StudentWeakAreasChapterCache()
            new_cache.student = student
            new_cache.subject = subject
            new_cache.chapter = chapter
            new_cache.totalRight = right
            new_cache.totalWrong = wrong
            new_cache.totalSkipped = skipped
            new_cache.skippedPercent = skippedPercent
            new_cache.accuracy = accuracy
            new_cache.totalAttempted = total_attempted
            new_cache.save()





@shared_task
def createCacheStudentWeakAreasCache(student_id,subject,chapter):
    student = Student.objects.get(id = student_id)
    try:
        old_cache = StudentWeakAreasChapterCache.objects.get(student =
                                                             student,subject =
                                                             subject,chapter =
                                                             chapter)
        print('for student {} already cache for {} and\
              {}'.format(student,chapter,subject))
    except:
        all_marks = SSCOnlineMarks.objects.filter(student = student,test__sub =
                                                  subject)
        right = 0
        wrong = 0
        skipped = 0
        for marks in all_marks:
            for quest_id in marks.rightAnswers:
                quest = SSCquestions.objects.get(choices__id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chapter:
                    right += 1
            for quest_id in marks.wrongAnswers:
                quest = SSCquestions.objects.get(choices__id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chapter:
                    wrong += 1
            for quest_id in marks.skippedAnswers:
                quest = SSCquestions.objects.get(id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chapter:
                    skipped += 1
        total_attempted = right + wrong
        all_questions_attempted = total_attempted + skipped
        if all_questions_attempted == 0:
            return 
        if total_attempted == 0:
            accuracy = 0
        else:
            accuracy = (right / (total_attempted))* 100
        skipped_percent = (skipped / (all_questions_attempted))*100
        new_cache = StudentWeakAreasChapterCache()
        new_cache.totalRight = right
        new_cache.totalWrong = wrong
        new_cache.totalSkipped = skipped
        new_cache.skippedPercent = skipped_percent
        new_cache.accuracy = accuracy
        new_cache.totalAttempted = total_attempted
        new_cache.subject =subject
        new_cache.chapter = chapter
        new_cache.student = student
        new_cache.save()
        print('for student {} new cache for {} and\
              {}'.format(student,chapter,subject))

@shared_task
def get_chapters(subject):
    topic_choice = []
    for ch in range(1,50):
        for tp in range(1,20):
            topic_choice.append(str(ch) + '.' + str(tp))
    all_chapters = []
    for tp in topic_choice:
        chap = changeIndividualNames(tp,subject)
        if chap is not None:
            all_chapters.append(tp)
    return all_chapters

def get_chapters_withCode(subject):
    topic_choice = []
    for ch in range(1,50):
        for tp in range(1,20):
            topic_choice.append(str(ch) + '.' + str(tp))
    all_chapters = []
    chapter_names = []
    for tp in topic_choice:
        chap = changeIndividualNames(tp,subject)
        if chap is not None:
            all_chapters.append(tp)
            chapter_names.append(chap)
    final_chapter = list(zip(all_chapters,chapter_names))
    return final_chapter


@shared_task
def create_cache_weak_areas():
    students = Student.objects.filter(school__name = 'JEN')
    for n,student in enumerate(students):
        print('{} -- calculating for {}'.format(n,student))
        subjects = student.subject_set.all()
        for subject in subjects:
            subject = subject.name
            chapters = get_chapters(subject)
            for chapter in chapters:
                createCacheStudentWeakAreasCache.delay(student.id,subject,chapter)


@shared_task
def add_subjects_change_batch(course,stud_id,teacher_id,kl_id):
    stud = Student.objects.get(id = stud_id)
    teacher = Teacher.objects.get(id = teacher_id)
    try:
        custom_batch = CustomBatch.objects.get(klass__id = kl_id,teacher =
                                               teacher)
        print('in custom batch')
        for sub in custom_batch.subjects:
            custom_sub = Subject(name=sub,student = stud,teacher=teacher)
            custom_sub.save()
            print('{} sub saved'.format(sub))
    except Exception as e:
        print(str(e))

        if course == 'SSC':
            subGenInte =\
            Subject(name="General-Intelligence",student=stud,teacher=teacher)
            subGenInte.save()
            subMaths =\
            Subject(name="Quantitative-Analysis",student=stud,teacher=teacher)
            subEnglish = Subject(name="English",student=stud,teacher=teacher)
            subGenKnow =\
            Subject(name="General-Knowledge",student=stud,teacher=teacher)
            subGenSci = Subject(name="General-Science",student=stud,teacher=teacher)
            subMaths.save()
            subGenSci.save()
            subEnglish.save()
            subGenKnow.save()
        elif course == 'Loco':
           subGenInte =\
           Subject(name="General-Intelligence",student=stud,teacher=teacher)
           subGenInte.save()
           subMaths =\
           Subject(name="Quantitative-Analysis",student=stud,teacher=teacher)
           subEnglish =\
           Subject(name="English",student=stud,teacher=teacher)
           subGenKnow =\
           Subject(name="General-Knowledge",student=stud,teacher=teacher)
           subGenSci =\
           Subject(name="General-Science",student=stud,teacher=teacher)
           subLocoPilot =\
           Subject(name="ElectricalLocoPilot",student=stud,teacher=teacher)
           subLocoPilot.save()
           subLocoPilot_diesel =\
           Subject(name="LocoPilot_Diesel",student=stud,teacher=teacher)
           subLocoPilot_diesel.save()



           subMaths.save()
           subEnglish.save()
           subGenSci.save()
           subGenKnow.save()

@shared_task
def add_subjects_new(course,stud_id,teacher_id):
    stud = Student.objects.get(id = stud_id)
    teacher = Teacher.objects.get(id = teacher_id)
    sub =\
    Subject(name=course,student=stud,teacher=teacher)
    sub.save()

@shared_task
def addChapter(subject):
    chapts = get_chapters_withCode(subject)
    for cd,na in chapts:
        try:
            custom_chap = SubjectChapters.objects.get(subject = subject,code  =
                                                      cd)
        except:
            custom_chap = SubjectChapters()
            custom_chap.subject = subject
            custom_chap.code = cd
            custom_chap.name = na
            custom_chap.save()

@shared_task
def track_progress_cache(student_id,subject,marks_id):
    student = Student.objects.get(id = student_id)
    chapters = get_chapters(subject)
    subject = subject.strip()
    for chap in chapters:
        marks = SSCOnlineMarks.objects.get(id = marks_id)
        test = marks.test
        #total_marks = 0
        #for qu in test.sscquestions_set.all():
        #    total_marks = total_marks + qu.max_marks



        try:
            progress = StudentProgressChapterCache.objects.get(student =
                                                               student,subject =
                                                               subject,chapter =
                                                               chap)
            marks_old = progress.marks
            dates_old = progress.dates
            skipped_old = progress.skippedPercent
            rightPercent_old = progress.rightPercent
            wrongPercent_old = progress.wrongPercent
            right_timing_old = progress.rightTime
            wrong_timing_old = progress.wrongTime
            totalRight_old = progress.totalRight
            totalWrong_old = progress.totalWrong
            totalSkipped_old = progress.totalSkipped
            right = 0
            wrong = 0
            skipped = 0 
            chapter_mark = 0
            wrong_time = []
            right_time = []
            total_marks = 0
            for quest_id in marks.rightAnswers:
                quest = SSCquestions.objects.get(choices__id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chap:
                    right = right + 1
                    total_marks = total_marks + quest.max_marks
                    chapter_mark = chapter_mark +  quest.max_marks

                    answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                               marks,quest=quest)
                    right_time.append(answered.time)

            for quest_id in marks.wrongAnswers:
                quest = SSCquestions.objects.get(choices__id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chap:
                    wrong = wrong + 1
                    total_marks = total_marks + quest.max_marks
                    chapter_mark = chapter_mark -  quest.max_marks

                    answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                               marks,quest=quest)
                    wrong_time.append(answered.time)


            for quest_id in marks.skippedAnswers:
                quest = SSCquestions.objects.get(id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chap:
                    skipped = skipped + 1
            total_overall = right + wrong + skipped
            if total_overall == 0:
                continue
       # right percent
            if right+wrong == 0:
                right_percent = 0
                wrong_percent =0
            else:
                right_percent = (right / (right+wrong))*100

    # wrong percent
                wrong_percent = (wrong / (right+wrong))*100
    # skipped percent
            skipped_percent = (skipped / (right+wrong+skipped)) * 100
    #adding current marks to old marks list
            mark_percent = (chapter_mark / total_marks) *100
            marks_old.append(mark_percent)
    # adding current test date to old dates list
            dates_old.append(str(marks.testTaken))
    # calculating the average timing when question is right or wrong
            if right != 0:
                right_ave_timing = (sum(right_time) / right)
            else:
                right_ave_timing = 0
            if wrong != 0:
                wrong_ave_timing = (sum(wrong_time) / wrong)
            else:
                wrong_ave_timing = 0
    # adding average right or wrong timing to the old list
            right_timing_old.append(right_ave_timing)
            wrong_timing_old.append(wrong_ave_timing)
    # saving lists to cached progress
            progress.marks = marks_old
            progress.dates = dates_old
            skipped_old.append(skipped_percent)
            totalRight_old.append(right)
            totalWrong_old.append(wrong)
            totalSkipped_old.append(skipped)
            progress.skippedPercent = skipped_old
            rightPercent_old.append(right_percent)
            wrongPercent_old.append(wrong_percent)
            progress.rightPercent = rightPercent_old
            progress.wrongPercent = wrongPercent_old
            progress.rightTime = right_timing_old
            progress.wrongTime = wrong_timing_old
            progress.save()
            
        except Exception as e:
            print(str(e))
            right = 0
            wrong = 0
            skipped = 0 
            chapter_mark = 0
            wrong_time = []
            right_time = []
            total_marks = 0
            #total_marks = 0
            #for qu in test.sscquestions_set.all():
            #    total_marks = total_marks + qu.max_marks

           
            for quest_id in marks.rightAnswers:
                quest = SSCquestions.objects.get(choices__id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chap:
                    right = right + 1
                    total_marks = total_marks + quest.max_marks
                    chapter_mark = chapter_mark +  quest.max_marks

                    answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                               marks,quest=quest)
                    right_time.append(answered.time)


            for quest_id in marks.wrongAnswers:
                quest = SSCquestions.objects.get(choices__id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chap:
                    wrong = wrong + 1
                    total_marks = total_marks + quest.max_marks
                    chapter_mark = chapter_mark -  quest.max_marks

                    answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                               marks,quest=quest)
                    wrong_time.append(answered.time)


            for quest_id in marks.skippedAnswers:
                quest = SSCquestions.objects.get(id = quest_id)
                if quest.section_category == subject and quest.topic_category\
                ==chap:
                    skipped = skipped + 1
            total_overall = (right + wrong + skipped)
            if total_overall == 0:
                continue
            if right + wrong == 0:
                right_percent = 0
                wrong_percent = 0
            else:
                right_percent = (right / (right+wrong))*100
                wrong_percent = (wrong / (right+wrong))*100
            skipped_percent = (skipped / (right+wrong+skipped)) * 100
            if len(right_time) == 0:
                right_ave_timing = [0]
            else:
                right_ave_timing = [(sum(right_time) / right)]
            if len(wrong_time) == 0:
                wrong_ave_timing = [0]
            else:
                wrong_ave_timing = [(sum(wrong_time) / wrong)]

            progress = StudentProgressChapterCache()
            totalRight = [right]
            totalWrong = [wrong]
            totalSkipped = [skipped]
            right_list = [right_percent]
            wrong_list = [wrong_percent]
            dates = [str(marks.testTaken)]
            mark_percent = (chapter_mark / total_marks) *100
            test_mark = [mark_percent]
            skipped_percent_list = [skipped_percent]
            progress.marks = test_mark
            progress.rightPercent = right_list
            progress.wrongPercent = wrong_list
            progress.skippedPercent = skipped_percent_list
            progress.chapter = chap
            progress.subject = subject
            progress.dates = dates
            progress.student = student
            progress.rightTime =right_ave_timing
            progress.wrongTime = wrong_ave_timing
            progress.totalRight = totalRight
            progress.totalWrong = totalWrong
            progress.totalSkipped = totalSkipped
            progress.save()

@shared_task
def start_caching_prgress():
    students = Student.objects.filter(school__name = "JEN")
    for stud in students:
        subjects = stud.subject_set.all()
        for sub in subjects:
            chapters = get_chapters(sub.name)
            for chap in chapters:
                createProgressCache.delay(stud.id,sub.name,chap)


@shared_task
def createProgressCache(student_id,subject,chap):
    student = Student.objects.get(id = student_id)
    try:
        progress_cache = StudentProgressChapterCache.objects.get(student =
                                                                 student,subject
                                                                 =
                                                                 subject,chapter=chap)
    except Exception as e:
        print(str(e))
        marks = SSCOnlineMarks.objects.filter(student = student,test__sub =
                                              subject).order_by('-testTaken')
        if len(marks) == 0:
            return
        else:
        
            list_right_percent = []
            list_wrong_percent = []
            list_date = []
            list_skipped_percent = []
            list_right_ave_timing = []
            list_wrong_ave_timing = []
            list_chapter_mark = []
            for ma in marks:
                right = 0
                wrong = 0
                skipped = 0 
                chapter_mark = 0
                wrong_time = []
                right_time = []

                for quest_id in ma.rightAnswers:
                    quest = SSCquestions.objects.get(choices__id = quest_id)
                    if quest.section_category == subject and quest.topic_category\
                    ==chap:
                        answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                                   ma,quest=quest)
                        right_time.append(answered.time)
                        right = right + 1
                        chapter_mark = chapter_mark +  quest.max_marks
                for quest_id in ma.wrongAnswers:
                    quest = SSCquestions.objects.get(choices__id = quest_id)
                    if quest.section_category == subject and quest.topic_category\
                    ==chap:
                        answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                                   ma,quest=quest)
                        wrong_time.append(answered.time)


                        wrong = wrong +1

                        chapter_mark = chapter_mark -  quest.negative_marks
                for quest_id in ma.skippedAnswers:
                    quest = SSCquestions.objects.get(id = quest_id)
                    if quest.section_category == subject and quest.topic_category\
                    ==chap:
                        skipped += 1
                if right + wrong + skipped == 0:
                    continue
                elif right + wrong == 0:
                    right_percent = 0
                    wrong_percent = 0
                    skipped_percent = (skipped / (right+wrong+skipped)) * 100
                    right_ave_timing = 0
                    wrong_ave_timing = 0
                    this_test_date = str(ma.testTaken)
                    list_skipped_percent.append(skipped_percent)
                    list_right_ave_timing.append(right_ave_timing)
                    list_wrong_ave_timing.append(wrong_ave_timing)
                    list_date.append(this_test_date)
                    list_right_percent.append(right_percent)
                    list_wrong_percent.append(wrong_percent)
                    list_chapter_mark.append(chapter_mark)


                else:
                    right_percent = (right / (right+wrong))*100
                    wrong_percent = (wrong / (right+wrong))*100
                    skipped_percent = (skipped / (right+wrong+skipped)) * 100
                    right_ave_timing = (sum(right_time) / len(right_time))
                    wrong_ave_timing = (sum(wrong_time) / len(wrong_time))
                    this_test_date = str(ma.testTaken)
                    list_skipped_percent.append(skipped_percent)
                    list_right_ave_timing.append(right_ave_timing)
                    list_wrong_ave_timing.append(wrong_ave_timing)
                    list_date.append(this_test_date)
                    list_right_percent.append(right_percent)
                    list_wrong_percent.append(wrong_percent)
                    list_chapter_mark.append(chapter_mark)

            if len(list_chapter_mark) != 0:
                progress = StudentProgressChapterCache()
                progress.marks = list_chapter_mark
                progress.rightPercent = list_right_percent
                progress.wrongPercent = list_wrong_percent
                progress.skippedPercent = list_skipped_percent
                progress.chapter = chap
                progress.subject = subject
                progress.dates = list_date
                progress.student = student
                progress.rightTime =list_right_ave_timing
                progress.wrongTime = list_wrong_ave_timing
                progress.save()

def get_section(sectionType):
        if sectionType == 'English':
            return('English')
        elif sectionType == 'Reasoning':
            return('General-Intelligence')
        elif sectionType == 'Maths':
            return('Quantitative-Analysis')
        elif sectionType == 'GK':
            return('General-Knowledge')
        elif sectionType == 'groupxen':
            return('Defence-English')
        elif sectionType == 'groupxphy':
            return('Defence-Physics')
        elif sectionType == 'groupxmath':
            return('GroupX-Maths')
        elif sectionType == 'groupgk':
            return('Defence-GK-CA')
        elif sectionType == 'jeeMaths10':
            return('MathsIITJEE10')
        elif sectionType == 'jeeMaths11':
            return('MathsIITJEE11')
        elif sectionType == 'jeeMaths12':
            return('MathsIITJEE12')
        elif sectionType == 'jeePhysics10':
            return('PhysicsIITJEE10')
        elif sectionType == 'jeePhysics11':
            return('PhysicsIITJEE11')
        elif sectionType == 'jeePhysics12':
            return('PhysicsIITJEE12')
        elif sectionType == 'jeeChemistry10':
            return('ChemistryIITJEE10')
        elif sectionType == 'jeeChemistry11':
            return('ChemistryIITJEE11')
        elif sectionType == 'jeeChemistry12':
            return('ChemistryIITJEE12')
        elif sectionType == 'locopilot_electrical':
            return('ElectricalLocoPilot')
        elif sectionType == 'locopilot_fitter':
            return('FitterLocoPilot')
        elif sectionType == 'general_science':
            return('General-Science')
        elif sectionType == 'locopilot_diesel':
            return('LocoPilot_Diesel')
        elif sectionType.strip() == 'cat_quant':
            return('CAT_Quantitative_Aptitude')
        elif sectionType.strip() == 'loco_civil':
            return('Civil_Loco_Pilot_Tech')
        elif sectionType.strip() == 'ssc_electrical':
            return('SSC_Electronics1')

@shared_task
def create_Subject_topics(sheet_link):
    for sh in sheet_link:
        df=\
        pd.read_csv('/app/question_data/jen_content/iit_jee_physics/jee_phy/'+sh,error_bad_lines=False )
        sectionType = df['section_type']
        code = df['category']
        name = df['name']
        final = list(zip(sectionType,code,name))
        for s,c,n in final:
            subject = get_section(s)
            co = float(c)


            try:
                chapter = SubjectChapters.objects.get(subject = subject,code =
                                                      co)
            except:
                chapter = SubjectChapters()
                chapter.name = n
                chapter.subject = subject
                chapter.code = co
                chapter.save()

@shared_task
def add_announcements_newStudent(stud_id,kl_id):
    student = Student.objects.get(id = stud_id)
    klass_obj = klass.objects.get(id = kl_id)
    announcements = Announcement.objects.filter(klass = klass_obj)
    for ann in announcements:
        ann.listener.add(student)
@shared_task
def delete_questions():
    df =\
    pd.read_csv('/app/question_data/jen_content/delete/question_delete.csv')
    quest_ids = df['delete']
    print('{} questions to be deleted'.format(len(quest_ids)))
    for i in quest_ids:
        try:
            question = SSCquestions.objects.get(id = int(i))
            question.delete()
        except Exception as e:
            print(str(e))

@shared_task
def add_jobs(path):
    with open(path,'rb') as fi:
        jobs = pickle.load(fi)
    json_jobs = json.dumps(jobs[11:])
    print(json_jobs)
@shared_task
def fill_taken_subjects():
    students = Student.objects.all()
    for stud in students:
        try:
            cache = StudentTakenSubjectsCache.objects.get(student = stud)
        except:
            cache = StudentTakenSubjectsCache()
            cache.student = stud
            tests = SSCOnlineMarks.objects.filter(student = stud)
            subjects = []
            for te in tests:
                subjects.append(te.test.sub)
            if len(subjects) > 1:
                subjects = list(unique_everseen(subjects))
            if len(subjects) == 0:
                continue
            cache.subjects = subjects
            cache.save()

@shared_task
def fill_subjects(student_id,subject):
    student = Student.objects.get(id = student_id)
    try:
        cache = StudentTakenSubjectsCache.objects.get(student = student)
        subs = cache.subjects
        if subject in subs:
            return
        else:
            subs.append(subject)
            cache.subjects = subs
            cache.save()
    except:
        cache = StudentTakenSubjectsCache()
        cache.student = student
        cache.subjects = [subject]
        cache.save()

@shared_task
def notification_onetoone_message(title,body,sender_id,receiver_id):
    user_send = User.objects.get(id = sender_id)
    user_receiver = User.objects.get(id = receiver_id)
    try:
        sender_query = FirebaseToken.objects.get(user = user_send)
        receiver_query = FirebaseToken.objects.get(user = user_send)
        sender_token = sender_query.token
        receiver_token = receiver_query.token
        OneToOneMessageAPIView(title,body,sender_token,receiver_token)
    except Exception as e:
        print(str(e))

    
@shared_task
def notification_announcement(title,body,sender_id,batch):
    user = User.objects.get(id = sender_id)
    me = Teach(user)
    school = me.my_school()
    AnnouncementNotification(title,body,school.name,batch)

@shared_task
def notification_create_test(title,body,sender_id,batch):
    user = User.objects.get(id = sender_id)
    me = Teach(user)
    school = me.my_school()
    CreateTestNotification(title,body,school.name,batch)

@shared_task
def notification_create_timetable(title,body,sender_id,batch):
    user = User.objects.get(id = sender_id)
    me = Teach(user)
    school = me.my_school()
    TimeTableNotification(title,body,school.name,batch)



def\
youtube_search(q,max_results=5,order='relevance',token=None,location=None,location_radius=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=
                    DEVELOPER_KEY)
    search_response = youtube.search().list(
        q = q,
        type = "video",
        pageToken = token,
        order = order,
        part = "id,snippet",
        maxResults = max_results,
        location = location,
        locationRadius = location_radius).execute()

    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    favoriteCount = []
    category = []
    tags = []
    videos = []
    thumbnail = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title.append(search_result['snippet']['title'])
            thumbnail.append(search_result['snippet']['thumbnails'])

            videoId.append(search_result['id']['videoId'])

            response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()

            channelId.append(response['items'][0]['snippet']['channelId'])
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
            categoryId.append(response['items'][0]['snippet']['categoryId'])
            favoriteCount.append(response['items'][0]['statistics']['favoriteCount'])
            viewCount.append(response['items'][0]['statistics']['viewCount'])
            likeCount.append(response['items'][0]['statistics']['likeCount'])
            dislikeCount.append(response['items'][0]['statistics']['dislikeCount'])

        if 'commentCount' in response['items'][0]['statistics'].keys():
            commentCount.append(response['items'][0]['statistics']['commentCount'])

        else:
            commentCount.append([])

        if 'tags' in response['items'][0]['snippet'].keys():
            tags.append(response['items'][0]['snippet']['tags'])
        else:
            tags.append([])

    youtube_dict = {'tags':tags,'channelId': channelId,'channelTitle':
                    channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'likeCount':likeCount,'dislikeCount':dislikeCount,'commentCount':commentCount,'favoriteCount':favoriteCount,'thumbnail':thumbnail}
    print('youtube searched videos {}'.format(youtube_dict))

    return youtube_dict




@shared_task
def get_youtube_videos(subject,chapter):
    se = str(chapter) + ' ' + 'ssc'
    result = youtube_search(se)

    print(result['title'])
    print(result['videoId'])
    li = result['videoId']
    title = result['title']
    thumbnail = result['thumbnail'][0]['medium']['url']
    print('this is the thumbnail youtube {}'.format(thumbnail))
    title_list = []
    link_list = []
    for i in title:
        title_list.append(i)
    for i in li:
        link_list.append(i)
    both = list(zip(title_list,link_list))
    for i,j in both:
    
        try:
            vid = YoutubeExternalVideos.objects.get(link = j)
        except Exception as e:
            print(str(e))
            save_vid = YoutubeExternalVideos()
            save_vid.title = i[:150]
            save_vid.chapter = chapter
            save_vid.subject = subject
            save_vid.link = j
            save_vid.thumbnail = thumbnail
            save_vid.save()
            print('new youtube video saved')


@shared_task
def create_test_api(user_id,quest_list,date,time,kl):
    user = User.objects.get(id = user_id)
    me = Teach(user)
    kl = klass.objects.get(school = me.my_school(),name=kl)
    date = datetime.strptime(date,"%d-%m-%Y")
    all_questions = []
    total_marks = 0
    if ',' in quest_list:
        quest_list = quest_list.split(',')
        for qu in quest_list:
            questions = SSCquestions.objects.get(id = int(qu))
            total_marks = total_marks + questions.max_marks
            all_questions.append(questions)

    else:
            questions = SSCquestions.objects.get(id = int(quest_list))
            total_marks = total_marks + questions.max_marks
            all_questions.append(questions)
    test = SSCKlassTest()
    test.due_date = date
    test.totalTime = time
    subs = []
    test.klas = kl
    test.max_marks = total_marks
    test.name = str(me.profile)+ str(timezone.now())
    test.creator = user
    test.save()
    for qu in all_questions:
        qu.ktest.add(test)

    for sub in test.sscquestions_set.all():
        timesus = TimesUsed.objects.filter(teacher =
                                          me.profile,quest =
                                          sub,batch = kl)
        if len(timesus) == 1:
            for i in timesus:
                i.numUsed = i.numUsed + 1
                i.save()
                
        else:
            tused = TimesUsed()
            tused.numUsed = 1
            tused.teacher = me.profile
            tused.quest = sub
            tused.batch = kl
            tused.save()

        subs.append(sub.section_category)
    
    subs = list(unique_everseen(subs))
    test_details = TestDetails()
    test_details.test = test
    test_details.num_questions = len(all_questions)
    test_details.questions = quest_list
    test_details.save()

    if len(subs)==1:
        test.sub = subs[0]
        kl = test.klas
        students = Student.objects.filter(klass = kl,school =
                                          me.profile.school)
        for i in students:
            test.testTakers.add(i)
            test.save()

    else:
        students = Student.objects.filter(klass = kl,school = me.profile.school)
        for i in students:
            test.testTakers.add(i)
            test.save()


        if 'Defence-Physics' in subs or 'Defence-English' in\
        subs or 'Defence-GK-CA' in subs:
            test.sub = 'Defence-MultipleSubjects'
        elif 'JEE10' in subs[0]:
            test.sub = 'IITJEE10-MultipleSubjects'
        elif 'JEE11' in subs[0]:
            test.sub = 'IITJEE11-MultipleSubjects'
        elif 'JEE12' in subs[0]:
            test.sub = 'IITJEE12-MultipleSubjects'
        elif 'FitterLocoPilot' in subs:
            test.sub = 'LocoPilot-MultipleSubjects'

        else:
            test.sub = 'MultipleSections'
    
    test.mode = 'BodhiOnline'
    test.save()
    title = "New test for you on "+str(test.sub)
    body = "Total number of questions " + str(len(all_questions))
    notification_create_test(title,body,user.id,kl.name)

@shared_task
def delete_repeat_questions():
    questions = SSCquestions.objects.all()
    for quest in questions:
        quest_id = quest.id
        already_question = SSCquestions.objects.filter(picture = quest.picture)
        if len(already_question) > 1:
            print('{} id of question deleted'.format(quest.id))
            quest.delete()


@shared_task
def delete_duplicate_marks():
    students = Student.objects.all()
    print('number of students {}'.format(len(students)))
    for stud in students:
        tests = SSCKlassTest.objects.all()
        print('number of tests {}'.format(len(tests)))
        for te in tests:
            marks = SSCOnlineMarks.objects.filter(student =
                                                  stud,test=te)
            if len(marks) > 1:
                print('number of tests = {}'.format(len(marks)))
                for ma in marks:
                    ma.delete()
                    print('marks deleted')
                    if len(marks) == 1:
                        break


@shared_task
def saveTestRank(test_id):
    specific_test = SSCKlassTest.objects.get(id = test_id)
    try:
        test_ranking_table = TestRank.objects.get(test = specific_test)
        test_ranking_table.delete()
    except:
        pass
    all_mark = SSCOnlineMarks.objects.filter(test__id = test_id)
    my_marks = 0

    others_marks = []
    others_students = []
    for i in all_mark:
        others_marks.append(i.marks)
        others_students.append(i.student.id)
    total_ranking_list = list(zip(others_marks,others_students))
    #ranked_marks = sorted(others_marks,reverse = True)
    sorted_ranked_marks = sorted(total_ranking_list, key=lambda x:\
                                 x[0],reverse=True)
    sorted_ranked_marks = np.array(sorted_ranked_marks)
    total = len(sorted_ranked_marks)
    new_ranking_table = TestRank()
    new_ranking_table.sortedMarks = list(sorted_ranked_marks[:,0])
    new_ranking_table.students = list(sorted_ranked_marks[:,1])
    new_ranking_table.test = specific_test
    new_ranking_table.save()

@shared_task
def delete_bad_Online_Marks(user_id):
    user = User.objects.get(id = user_id)
    student = Student.objects.get(studentuser=user)
    my_tests = SSCKlassTest.objects.filter(testTakers = student)
    for test in my_tests:
        online_marks = SSCOnlineMarks.objects.filter(student = student,test__id = test.id)
        if len(online_marks) != 0:
            for om in online_marks:
                om.delete()
                if len(online_marks) == 1:
                    break

@shared_task
def saveSubjectWiseAccuracyCache(user_id,test_id,subject):
    user = User.objects.get(id = user_id)
    me = Studs(user)
    test = SSCKlassTest.objects.get(id = test_id)
    marks = SSCOnlineMarks.objects.get(student = me.profile,test = test)
    rightAnswers = marks.rightAnswers
    wrongAnswers = marks.wrongAnswers
    numberAttempted = len(rightAnswers) + len(wrongAnswers)
    if numberAttempted == 0:
        return
    try:
        accuracyCache = SubjectAccuracyStudent.objects.get(student =
                                                             me.profile,subject
                                                            = subject)
        pastNumberRightAnswers = accuracyCache.rightAnswers
        pastNumberTotalAttempted = accuracyCache.totalAttempted
        numberOfTests = accuracyCache.testNumbers
        numberOfTests = numberOfTests + 1
        countRightAnswers = 0
        countSubjectAttempted = 0
        for ra in rightAnswers:
            question = SSCquestions.objects.get(choices__id = ra)
            if question.section_category == subject:
                countRightAnswers += 1
                countSubjectAttempted += 1

        for wa in wrongAnswers:
            question = SSCquestions.objects.get(choices__id = wa)
            if question.section_category == subject:
                countSubjectAttempted += 1
        if countSubjectAttempted == 0:
            accuracyCache.save()
            return
        totalRightAnswers = pastNumberRightAnswers + countRightAnswers
        totalNumberAttempted = pastNumberTotalAttempted + countSubjectAttempted
        newAccuracy = (totalRightAnswers / totalNumberAttempted) * 100

        accuracyCache.accuracy = newAccuracy
        accuracyCache.rightAnswers = totalRightAnswers
        accuracyCache.totalAttempted = totalNumberAttempted
        accuracyCache.testNumbers = numberOfTests
        accuracyCache.save()



    except Exception as e:
        accuracyCache = SubjectAccuracyStudent()
        countRightAnswers = 0
        countSubjectAttempted = 0
        for ra in rightAnswers:
            question = SSCquestions.objects.get(choices__id = ra)
            if question.section_category == subject:
                countRightAnswers += 1
                countSubjectAttempted += 1

        for wa in wrongAnswers:
            question = SSCquestions.objects.get(choices__id = wa)
            if question.section_category == subject:
                countSubjectAttempted += 1


        if countSubjectAttempted == 0:
            return
       
        accuracy = (countRightAnswers / countSubjectAttempted) * 100 
 
        accuracyCache.student = me.profile
        accuracyCache.subject = subject
        accuracyCache.rightAnswers = countRightAnswers
        accuracyCache.totalAttempted = countSubjectAttempted
        accuracyCache.testNumbers = int(1)
        accuracyCache.accuracy = accuracy
        accuracyCache.save()

@shared_task
def saveSubjectWiseAccuracyRanking(user_id,subject):
    try:
        subject_ranking = SubjectRank.objects.get(subject = subject)
        subject_ranking.delete()
        
    except Exception as e:
        print(str(e))

    subject_ranking_model = SubjectRank()
    subject_accuracy_list = []
    total_attempted_list = []
    number_test_list = []
    student_id_list = []
    all_accuracy = SubjectAccuracyStudent.objects.filter(subject
                                                        = subject)
    student_object = Student.objects.get(studentuser__id = user_id)
    print('student object id {}'.format(student_object.id))
    for sub_acc in all_accuracy:
        #sub_acc =\
        #SubjectAccuracyStudent.objects.filter(subject=subject,student=marks.student)
        accuracy = sub_acc.accuracy
        my_student_id = student_object.id
        question_attempted = sub_acc.totalAttempted
        number_tests = sub_acc.testNumbers
        stud = sub_acc.student
        subject_accuracy_list.append(accuracy)
        total_attempted_list.append(question_attempted)
        number_test_list.append(number_tests)
        student_id_list.append(stud.id)



    subject_ranking =\
    list(zip(student_id_list,subject_accuracy_list,total_attempted_list,number_test_list))
    sorted_ranked_marks = sorted(subject_ranking, key=lambda x:\
                                 x[1],reverse=True)
    sorted_ranked_marks = np.array(sorted_ranked_marks)
    subject_ranking_model.subject = subject
    subject_ranking_model.sortedAccuracies = list(sorted_ranked_marks[:,1])
    subject_ranking_model.students = list(sorted_ranked_marks[:,0])
    subject_ranking_model.minimumTests = min(sorted_ranked_marks[:,3])
    subject_ranking_model.maximumTests =max(sorted_ranked_marks[:,3])
    subject_ranking_model.save()
    ranking_key = str(my_student_id)+sub_acc.subject
    try:
        my_rank = np.where(sorted_ranked_marks[:,0] == my_student_id)[0]
        print('before my_rank {}'.format(my_rank))
        my_rank = my_rank[0]+1
        print('key {}, my rank {}'.format(ranking_key,my_rank))
    except:
        my_rank = int(99)
    try:
        client = boto3.resource(
        'dynamodb',
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = ACCESS_SECRET_KEY,
        region_name = 'ap-south-1'
        )
        table = client.Table('subjectranking1')
        res = table.update_item(
            Key = { 
                    'student_id':ranking_key
                },  
        UpdateExpression = "SET  dateTaken = list_append(dateTaken,:da),ranking =list_append(ranking,:ra)",
        ExpressionAttributeValues={
                    ':ra': [int(my_rank)],
                    ':da': [str(timezone.now())]
                },  
        ReturnValues="UPDATED_NEW"

        )
        print('db updated')
    except Exception as e:
        print('amazon db error {}'.format(str(e)))
        table.put_item(
        Item={
        'student_id': ranking_key,
        'ranking': [int(my_rank)],
        'dateTaken':[str(timezone.now())],
        'subject':subject

            }
        )
        print('db created')

@shared_task
def saveChapterWiseAccuracyRanking(subject,chapter_code,chapter_name,student_id):
    chapter_code = float(chapter_code)
    try:
        subject_ranking = ChapterRank.objects.get(subject =
                                                  subject,chapterCode =
                                                  chapter_code)
        subject_ranking.delete()
        
    except Exception as e:
        pass

    chapter_ranking_model = ChapterRank()
    subject_accuracy_list = []
    total_attempted_list = []
    number_test_list = []
    student_id_list = []
    all_accuracy = ChapterAccuracyStudent.objects.filter(subject
                                                        =
                                                         subject,chapterCode=chapter_code)

    for sub_acc in all_accuracy:
        accuracy = sub_acc.accuracy
        question_attempted = sub_acc.totalAttempted
        number_tests = sub_acc.testNumbers
        stud = sub_acc.student
        subject_accuracy_list.append(accuracy)
        total_attempted_list.append(question_attempted)
        number_test_list.append(number_tests)
        student_id_list.append(stud.id)
    subject_ranking =\
    list(zip(student_id_list,subject_accuracy_list,total_attempted_list,number_test_list))
    sorted_ranked_marks = sorted(subject_ranking, key=lambda x:\
                                 x[1],reverse=True)
    sorted_ranked_marks = np.array(sorted_ranked_marks)
    chapter_ranking_model.subject = subject
    chapter_ranking_model.chapterCode = chapter_code
    chapter_ranking_model.chapterName = chapter_name
    chapter_ranking_model.sortedAccuracies = list(sorted_ranked_marks[:,1])
    chapter_ranking_model.students = list(sorted_ranked_marks[:,0])
    chapter_ranking_model.minimumTests = min(sorted_ranked_marks[:,3])
    chapter_ranking_model.maximumTests =max(sorted_ranked_marks[:,3])
    chapter_ranking_model.save()
    ranking_key = str(student_id)+subject+chapter_name
    try:
        my_rank = np.where(sorted_ranked_marks[:,0] == student_id)[0]
        print('before my_rank {}'.format(my_rank))
        my_rank = my_rank[0]+1
        print('key {}, my rank {}'.format(ranking_key,my_rank))
    except:
        my_rank = int(0)
    try:
        client = boto3.resource(
        'dynamodb',
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = ACCESS_SECRET_KEY,
        region_name = 'ap-south-1'
        )
        table = client.Table('chapterRanking')
        res = table.update_item(
            Key = { 
                    'student_id':ranking_key
                },  
        UpdateExpression = "SET  dateTaken = list_append(dateTaken,:da),ranking =list_append(ranking,:ra)",
        ExpressionAttributeValues={
                    ':ra': [int(my_rank)],
                    ':da': [str(timezone.now())]
                },  
        ReturnValues="UPDATED_NEW"

        )
        print('db updated')
    except Exception as e:
        print('amazon db error {}'.format(str(e)))
        table.put_item(
        Item={
        'student_id': ranking_key,
        'ranking': [int(my_rank)],
        'dateTaken':[str(timezone.now())],
        'subject':subject,
        'chapter':chapter_name,
        'chapterCode':str(chapter_code)

            }
        )
        print('db created chapter')






@shared_task
def helperChapterAccuracy(user_id,test_id,subject,chapter_code,chapter_name):
    chapter_code = str(chapter_code)
    user = User.objects.get(id = user_id)
    me = Studs(user)
    student_id = me.profile.id
    test = SSCKlassTest.objects.get(id = test_id)
    marks = SSCOnlineMarks.objects.get(student = me.profile,test = test)
    rightAnswers = marks.rightAnswers
    wrongAnswers = marks.wrongAnswers
    numberAttempted = len(rightAnswers) + len(wrongAnswers)
    if numberAttempted == 0:
        return
    try:
        accuracyCache = ChapterAccuracyStudent.objects.get(student =
                                                             me.profile,subject
                                                            =
                                                           subject,chapterCode=chapter_code)
        pastNumberRightAnswers = accuracyCache.rightAnswers
        pastNumberTotalAttempted = accuracyCache.totalAttempted
        numberOfTests = accuracyCache.testNumbers
        numberOfTests = numberOfTests + 1
        countRightAnswers = 0
        countChapterAttempted = 0
        for ra in rightAnswers:
            question = SSCquestions.objects.get(choices__id = ra)
            if question.section_category == subject and question.topic_category == chapter_code:
                countRightAnswers += 1
                countChapterAttempted += 1

        for wa in wrongAnswers:
            question = SSCquestions.objects.get(choices__id = wa)
            if question.section_category == subject and question.topic_category == chapter_code:
                countChapterAttempted += 1
        if countChapterAttempted == 0:
            accuracyCache.save()
            return
        totalRightAnswers = pastNumberRightAnswers + countRightAnswers
        totalNumberAttempted = pastNumberTotalAttempted + countChapterAttempted
        newAccuracy = (totalRightAnswers / totalNumberAttempted) * 100

        accuracyCache.accuracy = newAccuracy
        accuracyCache.rightAnswers = totalRightAnswers
        accuracyCache.totalAttempted = totalNumberAttempted
        accuracyCache.testNumbers = numberOfTests
        accuracyCache.save()
        saveChapterWiseAccuracyRanking(subject,chapter_code,chapter_name,student_id)



    except Exception as e:
        accuracyCache = ChapterAccuracyStudent()
        countRightAnswers = 0
        countChapterAttempted = 0
        for ra in rightAnswers:
            question = SSCquestions.objects.get(choices__id = ra)
            if question.section_category == subject and\
            question.topic_category == chapter_code:
                countRightAnswers += 1
                countChapterAttempted += 1

        for wa in wrongAnswers:
            question = SSCquestions.objects.get(choices__id = wa)
            if question.section_category == subject and\
               question.topic_category == chapter_code:
                countChapterAttempted += 1


        if countChapterAttempted == 0:
            return
       
        accuracy = (countRightAnswers / countChapterAttempted) * 100 
 
        accuracyCache.student = me.profile
        accuracyCache.subject = subject
        accuracyCache.rightAnswers = countRightAnswers
        accuracyCache.totalAttempted = countChapterAttempted
        accuracyCache.testNumbers = int(1)
        accuracyCache.accuracy = accuracy
        accuracyCache.chapterCode = chapter_code
        accuracyCache.chapterName = chapter_name
        accuracyCache.save()
        saveChapterWiseAccuracyRanking(subject,chapter_code,chapter_name,student_id)

 
@shared_task
def saveChapterWiseAccuracyCache(user_id,test_id,subject):
    subject_chapters = SubjectChapters.objects.filter(subject = subject)
    for sub_chap in subject_chapters:
        chapter_name = sub_chap.name
        chapter_code = sub_chap.code
        helperChapterAccuracy(user_id,test_id,subject,chapter_code,chapter_name)


@shared_task
def send_otp(num,otp):
    message = """Welcome to BodhiAI, you OTP is {}""".format(otp)
   
        #send_url =\
        #"""http://sms.trickylab.com/http-api.php?username={}&password={}
        #&senderid={}&route=1&number={}&message={}""".format('bodhiai','123456','Bodhii',num,message)

    send_url =\
    'http://sms.trickylab.com/http-api.php?username=bodhiai&password=123456&senderid=Bodhii&route=1&number='+num+'&message='+message+''
    r = requests.get(send_url)




