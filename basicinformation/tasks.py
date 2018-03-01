from celery import shared_task
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .models import *
from QuestionsAndPapers.models import *
from django.utils import timezone
from more_itertools import unique_everseen
from django.http import Http404
from .marksprediction import *
from django.core import serializers


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


