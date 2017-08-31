from django.shortcuts import render
from django.core.urlresolvers import reverse
from .models import Questions,Choices,KlassTest
from basicinformation.models import *
from basicinformation.marksprediction import *
import datetime
import os.path
from django.utils import timezone
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User,Group
import re
import pickle
import urllib.request
from more_itertools import unique_everseen
from random import randint
# Create your views here.

def create_test(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name= 'Teachers').exists():
            me = Teach(user)
            quest_file_name = 'question_paper'+str(user.teacher)+'.pkl'
            if me.institution == 'School':
                questions = Questions.objects.all()
            elif me.institution == 'SSC':
                questions = SSCquestions.objects.all()
            school = me.my_school()
            all_klasses = me.my_classes_names()
            try:
                if 'klass_test' in request.GET:
                    try:
                        if os.path.exists(quest_file_name):
                            os.remove(quest_file_name)
                    except:
                        pass

                    ttt = request.GET['klass_test']
                    klasses = klass.objects.filter(name=ttt)
                    klass_level = 'aa'
                    
                    for kass in klasses:
                        if me.institution == 'School':
                            klass_level = kass.level
                        elif me.institution == 'SSC':
                            klass_level = 'SSC'
                    if me.institution == "School":
                        quest = Questions.objects.filter(level = klass_level,school
                                                     =school)
                    elif me.institution == "SSC":
                        quest = SSCquestions.objects.filter(school= school)

                    if me.institution == "School":
                        if quest:
                            unique_chapters = []
                            for i in quest:
                                unique_chapters.append(i.chapCategory)
                                #for j in i.chapCategory:
                                #    unique_chapters.append(j)
                            unique_chapters = list(unique_everseen(unique_chapters))
                            test_type = 'School'
                            return render(request, 'questions/klass_available.html',
                                      {'fin':
                                       unique_chapters,'which_klass':ttt,'test_type':test_type})
                        else:
                            test_type = 'School'
                            noTest = 'Not Questions for this class'
                            context = {'noTest':noTest,'test_type':test_type}
                            return render(request,'questions/klass_available.html',context)
                    elif me.institution == "SSC":
                        if quest:
                            unique_chapters = []
                            for i in quest:
                                unique_chapters.append(i.section_category)
                            unique_chapters = list(unique_everseen(unique_chapters))
                            test_type = 'SSC'
                            print(unique_chapters)
                            return render(request, 'questions/klass_available.html',
                                      {'fin':
                                       unique_chapters,'which_klass':ttt,'test_type':test_type})
                        else:
                            noTest = 'Not Questions for this class'
                            context = {'noTest':noTest}
                            return
                        render(request,'questions/klass_available.html',context)
                if 'category_test' in request.GET:
                    category_klass = request.GET['category_test']
                    split_category = category_klass.split(',')[0]
                    split_klass = category_klass.split(',')[1]
                    if me.institution == 'School':
                        pass
                    elif me.institution == 'SSC':
                        quest = SSCquestions.objects.filter(section_category =
                                                            split_category,school
                                                            =school)
                        all_categories = []
                        for i in quest:
                            all_categories.append(i.topic_category)
                        all_categories = list(unique_everseen(all_categories))
                        all_categories.sort()
                        all_categories = \
                        me.change_topicNumbersNames(all_categories,split_category)
                        context = \
                        {'categories':all_categories,'which_klass':split_klass}
                        return \
                    render(request,'questions/klass_categories.html',context)
                    

                if 'chapter_test' in request.GET:
                    quest_file_name = 'question_paper'+str(user.teacher)+'.pkl'
                    which_chap = request.GET['chapter_test']
                    splitChap = which_chap.split(",",1)[0]
                    splitClass = which_chap.split(",",1)[1]
                    klasses = klass.objects.filter(name=splitClass)
                    klass_level = 'aa'
                    for kass in klasses:
                        if me.institution == 'School':
                            klass_level = kass.level
                        elif me.institution == 'SSC':
                            klass_level = 'SSC'
                    
                    if os.path.exists(quest_file_name):
                        with open(quest_file_name,'rb') as fi:
                            questions_list = pickle.load(fi)
                        idlist = []
                        for qq in questions_list:
                            idlist.append(qq.id)

                        if me.institution == "School":
                            klass_question = Questions.objects.filter(level =
                                                          klass_level,chapCategory=splitChap,school=school)
                        elif me.institution == "SSC":
                            klass_question = \
                            SSCquestions.objects.filter(topic_category = splitChap,school =
                                                        school)
                        context = \
                        {'que':klass_question,'idlist':idlist,'which_class':splitClass }
                        return render(request,'questions/klass_questions.html',context)
                    else:
                        if me.institution == 'School':
                            klass_question = Questions.objects.filter(level =
                                                          klass_level,chapCategory=splitChap,school=school)
                        elif me.institution == 'SSC':
                            klass_question =\
                            SSCquestions.objects.filter(topic_category =
                                                        splitChap,school =
                                                        school)
                        context = \
                        {'que':klass_question,'which_class':splitClass }
                        return render(request,'questions/klass_questions.html',context)


            except Exception as e:
                print(str(e))

            context = {'questions':questions,'klasses':all_klasses}
            return render(request,'questions/createTest.html',context)
        else:
            raise Http404("You don't have necessary permissions.")
def add_questions(request):
    user = request.user
    me = Teach(user)
    quest_file_name = 'question_paper'+str(user.teacher)+'.pkl'
    if 'question_id' in request.GET:
        if os.path.exists(quest_file_name):
            with open(quest_file_name,'rb') as lql:
                questions_list = pickle.load(lql)
        else:
            questions_list = []
        question_id = request.GET['question_id']
        which_klass = question_id.split(',')[1]
        question_id = question_id.split(',')[0]
        if me.institution == 'School':
            questions_list.append(Questions.objects.get(id=question_id))
        elif me.institution == 'SSC':
            questions_list.append(SSCquestions.objects.get(id=question_id))
        questions_list = list(unique_everseen(questions_list))
        with open(quest_file_name,'wb') as ql:
            pickle.dump(questions_list,ql)
        total_marks = []
        for l in questions_list:
            total_marks.append(l.max_marks)
        total = 0
        for k in total_marks:
            total = total + k
        num_questions = len(total_marks)
        context = \
                {'questions':questions_list,'total_marks':total,'num_questions':num_questions,'which_klass':which_klass }
        return render(request,'questions/addedQuestions.html',context)
    if 'remove_id' in request.GET:
        if os.path.exists(quest_file_name):
            with open(quest_file_name,'rb') as rid:
                questions_list = pickle.load(rid)
        else:
            questions_list = []
        questions = []
        rem_id = request.GET['remove_id']
        which_klass = rem_id.split(',')[1]
        rem_id  = rem_id.split(',')[0]
        if rem_id == None:
            return HttpResponse('No questions in question paper')
        for tbr in questions_list:
            if not int(tbr.id) == int(rem_id):
                questions.append(tbr)
        total_marks = []
        questions_list = questions
        with open(quest_file_name,'wb') as ql:
            pickle.dump(questions_list,ql)
        for j in questions_list:
            total_marks.append(j.max_marks)
        total = 0
        for k in total_marks:
            total = total + k
        num_questions = len(total_marks)
        context = \
        {'questions':questions,'total_marks':total,'num_questions':num_questions
         }
        return render(request,'questions/addedQuestions.html',context)
    if request.POST:
        with open(quest_file_name,'rb') as ql:
            questions_list= pickle.load(ql)
        if len(questions_list)!=0:
            me = Teach(request.user)
            which_klass = request.POST['which_klass']
            klass = me.my_classes_objects(which_klass)
            tot = 0 
            for i in questions_list:
                tot = tot + i.max_marks
            if user.teacher.school.category == 'School':
                newClassTest = KlassTest()
                teacher_type = 'School'
            elif user.teacher.school.category == 'SSC':
                newClassTest = SSCKlassTest()
                teacher_type = 'SSC'
            newClassTest.max_marks = tot
            newClassTest.published = timezone.now()
            newClassTest.name = str(request.user.teacher) + str(timezone.now())
            newClassTest.klas = klass
            newClassTest.creator = request.user
            newClassTest.save()
            for zz in questions_list:
                zz.ktest.add(newClassTest)
            context = {'test':newClassTest,'teacher_type':teacher_type}
            return render(request,'questions/publish_test.html',context)


def publish_test(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name= 'Teachers').exists():
            me = Teach(user)
            if 'publishTest' in request.POST:
                date = request.POST['dueDate']
                time = request.POST['timePicker']
                school = user.teacher.school
                if not date:
                    date = timezone.now()
                testid = request.POST['testid']
                if me.institution == 'School':
                    myTest = KlassTest.objects.get(id = testid)
                elif me.institution == 'SSC':
                    myTest = SSCKlassTest.objects.get(id = testid)
                kl = myTest.klas
                students = Student.objects.filter(klass = kl,school = school)
                for i in students:
                    myTest.testTakers.add(i)
                due_date = datetime.datetime.strptime(date, "%m/%d/%Y")
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
                    for sub in myTest.sscquestions_set.all():
                        subs.append(sub.section_category)
                    subs = list(unique_everseen(subs))
                    if len(subs)==1:
                        myTest.sub = subs[0]
                    else:
                        myTest.sub = 'SSCMultipleSections'
                    
                myTest.mode = 'BodhiOnline'
                myTest.save()
                return \
            render(request,'questions/teacher_successfully_published.html')
            if 'pdfTest' in request.POST:
                testid = request.POST['testid']
                if me.institution == 'School':
                    teacher_type = 'School'
                    myTest = KlassTest.objects.get(id = testid)
                    for sub in myTest.questions_set.all():
                        subject = sub.sub
                        break
                    myTest.sub = subject
                elif me.institution == 'SSC':
                    teacher_type = 'SSC'
                    myTest = SSCKlassTest.objects.get(id = testid)
                    subs = []
                    for sub in myTest.sscquestions_set.all():
                        subs.append(sub.section_category)
                    subs = list(unique_everseen(subs))
                    if len(subs)==1:
                        myTest.sub = subs[0]
                    else:
                        myTest.sub = 'SSCMultipleSections'

                myTest.mode = 'BodhiSchool'
                myTest.save()
                context = {'test':myTest,'teacher_type':teacher_type}
                pdf =\
                render_to_pdf('questions/teacher_school_createdTest.html',context)
                return HttpResponse(pdf,content_type= 'application/pdf')



def see_Test(request):
    user = request.user
    tests = KlassTest.objects.filter(creator = user)
    context = {'tests':tests}
    return render(request, 'questions/seeCreatedTest.html',context)

def student_my_tests(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name= 'Students').exists():
            me = Studs(user)
            subjects = me.subjects_OnlineTest()
            context = {'subjects':subjects}
            return render(request,'questions/student_my_tests.html',context)


def student_show_onlineTests(request):
    user = request.user
    me = Studs(user)
    if 'onlineTestSubject' in request.GET:
        my_sub = request.GET['onlineTestSubject']
        tests = me.OnlineTestsSubwise(my_sub)
        context = {'tests':tests}
        return render(request,'questions/student_onlinetests_subjectwise.html',context)
    if 'onlineTestid' in request.GET:
        testid = request.GET['onlineTestid']
        kk = SSCOnlineMarks.objects.all()
        old_test = me.is_onlineTestTaken(testid)
        if old_test:
            if me.institution == 'School':
                student_type = 'School'
            elif me.institution == 'SSC':
                student_type = 'SSC'
            context = {'marks':old_test,'student_type':student_type}
            return render(request,'questions/student_evaluated_test.html',context)
        else:
            if me.institution == 'School':
                test = KlassTest.objects.get(id = testid)
                context = {'test':test}
                return render(request,'questions/student_OnlineTest.html',context)

            elif me.institution == 'SSC':
                test = SSCKlassTest.objects.get(id = testid)
                quest = []
                for q in test.sscquestions_set.all():
                        quest.append(q.topic_category)
                lenquest = len(quest)
                nums = []
                for i in range(lenquest):
                    nums.append(i)
                context = {'questPosition':nums,'te_id':testid}
                return \
            render(request,'questions/student_individual_questionTest.html',context)

    if request.POST:
        all_answers = []
        right_answers = []
        right_answers2 = []
        wrong_answers = []
        wrong_answers2 = []
        skipped_answers = []
        skipped_answers2 = []
        num_of_quests = 0
        testid = request.POST['submitTest']
        if me.institution == 'School':
            test = KlassTest.objects.get(id= testid)
            for j in test.questions_set.all():
                num_of_quests += 1
        elif me.institution == 'SSC':
            test = SSCKlassTest.objects.get(id = testid)
            for j in test.sscquestions_set.all():
                num_of_quests += 1

        for i in range(num_of_quests+1):
            try:
                answerChoice = eval("'answerChoice'+str(i)")
                ans = request.POST[answerChoice]
                all_answers.append(int(ans))
            except:
                pass
        test_marks  = 0
        if me.institution == 'School':
            for qu in test.questions_set.all():
                for ch in qu.choices_set.all():
                    if not ch.id in all_answers:
                        skipped_answers.append(qu.id)
                    elif ch.id in all_answers and ch.predicament == "Correct":
                        right_answers.append(qu.id)
                        right_answers2.append(ch.id)
                        test_marks += int(qu.max_marks)
                    elif ch.id in all_answers and ch.predicament == "Wrong":
                        wrong_answers.append(qu.id)
                        wrong_answers2.append(ch.id)
            skipped_answers = list(unique_everseen(skipped_answers))
            for an in skipped_answers:
                if not an in right_answers and not an in wrong_answers:
                    skipped_answers2.append(an)
            my_marks = OnlineMarks()
            my_marks.test = test
            my_marks.student = request.user.student
            my_marks.rightAnswers = right_answers2
            my_marks.wrongAnswers = wrong_answers2
            my_marks.skippedAnswers = skipped_answers2
            my_marks.allAnswers = all_answers
            my_marks.marks = test_marks
            my_marks.testTaken = timezone.now()
            my_marks.save()
            context = {'marks':my_marks}
            return render(request,'questions/student_answered_paper.html',context)

        elif me.institution == 'SSC':
            for qu in test.sscquestions_set.all():
                for ch in qu.choices_set.all():
                    if not ch.id in all_answers:
                        skipped_answers.append(qu.id)
                    elif ch.id in all_answers and ch.predicament == "Correct":
                        right_answers.append(qu.id)
                        right_answers2.append(ch.id)
                        test_marks += int(qu.max_marks)
                    elif ch.id in all_answers and ch.predicament == "Wrong":
                        wrong_answers.append(qu.id)
                        wrong_answers2.append(ch.id)
                        test_marks -= int(qu.negative_marks)
            skipped_answers = list(unique_everseen(skipped_answers))
            for an in skipped_answers:
                if not an in right_answers and not an in wrong_answers:
                    skipped_answers2.append(an)
            my_marks = SSCOnlineMarks()
            my_marks.test = test
            my_marks.student = request.user.student
            my_marks.rightAnswers = right_answers2
            my_marks.wrongAnswers = wrong_answers2
            my_marks.skippedAnswers = skipped_answers2
            my_marks.allAnswers = all_answers
            my_marks.marks = test_marks
            my_marks.testTaken = timezone.now()
            my_marks.save()
            context = {'marks':my_marks}
            return render(request,'questions/student_answered_paper.html',context)

def conduct_Test(request):
    user = request.user
    if user.is_authenticated:
        me = Studs(user)
        
        if 'onlineTestid' in request.GET:
            testid = request.GET['onlineTestid']
            TemporaryAnswerHolder.objects.filter(stud=user.student,test__id=testid).delete()
            taken = me.is_onlineTestTaken(testid)
            if taken:
                if me.institution == 'School':
                    student_type = 'School'
                elif me.institution == 'SSC':
                    student_type = 'SSC'
                total_time = taken.timeTaken
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
            
                context = \
                {'marks':taken,'student_type':student_type,'timetaken':tt}
                return render(request,'questions/student_evaluated_test.html',context)
            else:
                if me.institution == 'School':
                    test = KlassTest.objects.get(id=test_id)
                    quest = []
                    for q in test.questions_set.all():
                        quest.append(q)
                    num_questions = len(quest)
                    context ={'num_questions':num_questions,'testid':testid,'student_type':'School'}
                    return \
                render(request,'questions/student_startoftest.html',context)
                elif me.institution == 'SSC':
                    test = SSCKlassTest.objects.get(id=testid)
                    if test.totalTime:
                        timeTest = test.totalTime
                    else:
                        timeTest = 10000
                    mins = timeTest %60
                    hours = int(timeTest /60)
                    if hours ==1:
                        timer = '{} hour and {} minutes'.format(hours,mins)
                    elif hours == 0:
                        timer = '{} minutes'.format(mins)
                    else:
                        timer = '{} hours and {} minutes'.format(hours,mins)
                    if hours >4:
                        timer = 'Unlimited (no time boundation)'

                    quest = []
                    for q in test.sscquestions_set.all():
                        quest.append(q)
                    num_questions = len(quest)
                    context = \
                            {'num_questions':num_questions,'testid':testid,'student_type':'SSC','timer':timer}
                    return \
                render(request,'questions/student_startoftest.html',context)


        if 'takeTest' in request.POST:
            testid = request.POST['takeTest']
            quest = []
            if me.institution == 'School':
                test = KlassTest.objects.get(id = testid)
                for q in test.questions_set.all():
                    quest.append(q.topic_category)

            elif me.institution == 'SSC':
                test = SSCKlassTest.objects.get(id = testid)
                for q in test.sscquestions_set.all():
                    quest.append(q.topic_category)

            lenquest = len(quest)
            if test.totalTime:
                timeTest = test.totalTime
            else:
                timeTest = 1000
            nums = []
            for i in range(lenquest):
                nums.append(i)
            context =\
                    {'questPosition':nums,'te_id':testid,'how_many':lenquest,'testTime':timeTest}
            return \
            render(request,'questions/student_individual_questionTest.html',context)
        if 'IndividualTestQuestPos' in request.GET:
            # this method gets the value of button pressed and sends the
            # question that is in that place
            questPos = request.GET['IndividualTestQuestPos']
            pos = questPos.split(',')[0]
            testid = questPos.split(',')[1]
            test = SSCKlassTest.objects.get(id = testid)
            quest = []
            # gets the number of questions in the test
            for q in test.sscquestions_set.all():
                quest.append(q)
            tosend = quest[int(pos)]
            qu = str(tosend.id)
            how_many = len(quest)
            try:
            # if this question was already answered then send the selected
            # choice to template
                temp_marks = TemporaryAnswerHolder.objects.filter(stud =
                                                              user.student,test__id
                                                              =testid,quests=qu).order_by('time')
                Quests = []
                for i in temp_marks:
                    Quests.append(int(i.answers))
                answer_sel = Quests[-1]
                context = \
                {'question':tosend,'testid':testid,'sel':answer_sel}
            except Exception as e:
            # if question has not been answered then just send the question
                hom_many = len(quest)
                context = {'question':tosend,'testid':testid,'how_many':how_many}
            return \
        render(request,'questions/student_individual_questionTestquestion.html',context)
        if 'questionid'  in  request.POST:
            # gets the values of choice id and time taken to choose that value
            try:
                choice_id = request.POST['choiceid']
                questTime = request.POST['questTimer']
            except Exception as e:
            # runs when next button is pressed rather than selecting a
            # choice(skipped)
                choice_id = -1
            question_id = request.POST['questionid']
            test_id = request.POST['testid']
            if choice_id == -1:
                questTime = -1
            if me.institution == 'School':
                pass
            elif me.institution == 'SSC':
                test = SSCKlassTest.objects.get(id = test_id)
                questnum = []
            # get the number of questions in the test
                for q in test.sscquestions_set.all():
                    questnum.append(q)
                how_many = len(questnum)

                try:
                    temp_marks = TemporaryAnswerHolder.objects.filter(stud =
                                                                  user.student,test__id=test_id)
                   
                except:
                    pass
            # saves choice to temporary holder 
                test = SSCKlassTest.objects.get(id = test_id)
                my_marks = TemporaryAnswerHolder()
                my_marks.stud = user.student
                my_marks.test = test
                my_marks.quests= question_id
                my_marks.answers = choice_id
                my_marks.time = int(questTime)
                my_marks.save()
                all_quests = []
                for i in temp_marks:
                   all_quests.append(i.quests)
                return HttpResponse(how_many)
        if 'testSub' in request.POST:
            # get values of test id and total test time
            test_id = request.POST['testSub']
            time_taken = request.POST['timeTaken']
            if me.institution == 'School':
                student_type = 'School'
                test = KlassTest.objects.get(id = test_id)
                online_marks = OnlineMarks()
            elif me.institution == 'SSC':
                student_type = 'SSC'
                test = SSCKlassTest.objects.get(id = test_id)
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
                    TemporaryAnswerHolder.objects.filter(stud=user.student,test__id=test_id,quests
                                                         =
                                                         str(i)).order_by('time')
                    for j in temp_marks:
                        answers_ids.append(int(j.answers))
                        time_ids.append(j.time)
                   
                    
                    qad = {'answers':answers_ids,'time':time_ids}
                    quest_ans_dict[i] = qad
            
                    
                except:
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
                        if int(final_ans) == -1:
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
                        print(final_ans)
                        if int(final_ans) == -1:
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
            total_time = (test.totalTime * 60)- (int(time_taken))
            # save to SSCOnlinemarks
            online_marks.rightAnswers = final_correct
            online_marks.wrongAnswers = final_wrong
            online_marks.skippedAnswers = final_skipped2
            online_marks.allAnswers = all_answers
            online_marks.marks = test_marks
            online_marks.timeTaken = total_time
            online_marks.save()
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
                        if times >3:
                            online_marks_quests.time = -1
                online_marks_quests.save()
            # calculate time to send to template
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

            # delete the temporary holders
            TemporaryAnswerHolder.objects.filter(stud=user.student,test__id=test_id).delete()
            context = \
            {'student_type':student_type,'marks':online_marks,'timetaken':tt}
            url = \
                    reverse('QuestionsAndPapers:studentMyOnlineTests')
            return HttpResponseRedirect(url)
            #return render(request,'questions/student_finished_test.html',context)


           



