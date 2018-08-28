from celery import shared_task
from rest_framework.response import Response
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .models import *
from QuestionsAndPapers.models import *
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
            print('cant fetch test error to evaluate')
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
                        print(str(e))
               
                
                qad = {'answers':answers_ids,'time':time_ids}
                quest_ans_dict[i] = qad
        
                
            except Exception as e:
                print(str(e))
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
        print('%s time taken, %s type' %(time_taken,type(time_taken)))
        try:
            time_taken = float(time_taken)
        except Exception as e:
            time_taken = float(100)
            print(str(e))

        try:
            total_time = (test.totalTime * 60)- time_taken
        except Exception as e:
            print(str(e))
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
            print('error at line 1263')
            print(str(e))
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
                print(str(e))
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
            print(str(e))

        # delete the temporary holders
        try:
            TemporaryAnswerHolder.objects.filter(stud=user.student,test__id=int(test_id)).delete()
        except Exception as e:
            print(str(e))
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
                print(str(e))
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
                pd.read_csv('/app/question_data/siel/'+sh,error_bad_lines=False )
            else:
                df=\
                pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/question_data/swami_reasoning/'+sh,error_bad_lines=False )

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
                print(optE)
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
                pd.read_csv('/app/question_data/jen_content/fitter/'+sh,error_bad_lines=False )
            else:
                df=\
                pd.read_csv('/home/prashant/Desktop/programming/projects/bodhiai/bodhiai/question_data/jen_content/fitter/'+sh,error_bad_lines=False )

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
                direction = df['Direction']
            except:
                direction = len(optD) * ['None']
            used_for = len(optD)*['LOCOPILOT_ELECTRICAL']
            lang = df['lang']
            source = len(used_for)*['JEN']
            if onlyImage:
                images = df['QuestionLink']
            else:
                quest_text = df['Question']
            sectionType = len(lang)*['locopilot_fitter']
            #direction = df['Direction']

            if explanation_quest:
                exp = df['Explanation']
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
            print('%s correct answers' %len(right_answer))
            print('%s number of categories' %len(quest_category))
            #print('%s languages ' %len(lang))
            print('%s sources' %len(source))
            print('%s sheet ' %sh)
        
            for ind in range(len(optA)):
                if onlyImage:
                    write_questions(school,None,optA[ind],optB[ind],optC[ind],optD[ind],None,images[ind],right_answer[ind],quest_category[ind],None,sectionType[ind],str(lang[ind]),used_for[ind],source[ind],fouroptions='4',direction
                                    = direction[ind] )
                else:
                    write_questions(school,quest_text,optA[ind],optB[ind],optC[ind],optD[ind],None,None,right_answer[ind],quest_category[ind],None,sectionType[ind],lang[ind],used_for[ind],source[ind],direction[ind],fouroptions='3')








@shared_task
def\
write_questions(school,question,optA,optB,optC,optD,optE,image,correctOpt,questCategory,exp,sectionType,lang,used_for,source,fouroptions,direction=False,replace=False):
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
@shared_task
def allquestions_institute(subject,institute):
    sch = School.objects.get(name=institute)
    questions =\
    SSCquestions.objects.filter(section_category=subject,source='SSCMaths')
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
        sub.name = 'FitterLocoPilot'
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
        print(saved_areas.date)
        print(latest_test.test.published)
        if latest_test.test.published <= saved_areas.date:
            print('yes dates are same')
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
            print('no dates are not same')
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
        print('above exception happened')
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
                                                   user).order_by('published')
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


#_--------------------------------------------------------------------------------------------
#@shared_task
#def student_topic_test(user_id):
#    user = User.objects.get(id = user_id)
#    me = Studs(user)
#    subjects = me.my_subjects_names()
#    for sub in subjects:

@shared_task
def deleteBadTests():
    quest_bad = SSCKlassTest.objects.all()
    for quest in quest_bad:
        if quest.sub == "":
            quest.delete()
@shared_task
def add_questions(institute,section):
    if institute == 'JEN':
        questions = SSCquestions.objects.filter(school__name =
                                                'SIEL',section_category
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
def create_test_api(user_id,quest_list,date,time):
    user = User.objects.get(id = user_id)
    me = Teach(user)
    date = datetime.strptime(date,"%d,%m,%Y")
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
    test.name = str(me.profile)+ str(timezone.now(0))
    test.creator = user
    test.save()
    for qu in quest_list:
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
    test_details.test = myTest
    test_details.num_questions = len(all_questions)
    test_details.questions = all_questions
    test_details.save()

    if len(subs)==1:
        test.sub = subs[0]
        kl = myTest.klas
        students = Student.objects.filter(klass = kl,school =
                                          me.profile.school)
        for i in students:
            subjs = Subject.objects.filter(teacher =
                                          me.profile,student=i,name
                                          = myTest.sub)
            if subjs:
                studs = Student.objects.get(subject = subjs)
                test.testTakers.add(studs)
                test.save()

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
                        test.testTakers.add(studs)
                        test.save()
                    except:
                        pass
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
            test.sub = 'SSCMultipleSections'
    
    test.mode = 'BodhiOnline'
    test.save()






