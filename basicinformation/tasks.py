from celery import shared_task
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
                                               user,klas=kl,sub=subject,mode='BodhiOnline')
    if len(online_tests) == 0 and subject == 'Defence-MultipleSubjects':
        online_tests = SSCKlassTest.objects.filter(creator = user,sub =
                                                   subject)
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
                pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/question_data/siel/'+sh,error_bad_lines=False )

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
            try:
                direction = df['Direction']
                print(direction)
            except:
                direction = None
            optA = df['optA']
            optB = df['optB']
            optC = df['optC']
            optD = df['optD']
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
            print('%s correct answers' %len(right_answer))
            print('%s number of categories' %len(quest_category))
            #print('%s languages ' %len(lang))
        
            for ind in range(len(optA)):
                if str(optD[ind]).lower() == 'noopt' and direction[ind]:
                    write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],None,None,None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'3',direction[ind])
                elif direction[ind]:
                    write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],optD[ind],None,None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'4',direction[ind])
                else:
                    write_questions(school,quest_text[ind],optA[ind],optB[ind],optC[ind],optD[ind],None,None,right_answer[ind],quest_category[ind],None,sectionType,lang,used_for,source,'4')


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
        new_questions.language = lang

        new_questions.usedFor = used_for

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





        #if question != None:
        #    new_questions.text = str(question)
        if direction and question is None:
            print('%s direction' %direction)
            new_questions.text = str(direction)
        elif question != None and direction:
            new_questions.text = str(direction) +'\n'+str(question)

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





