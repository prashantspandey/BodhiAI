from rest_framework import generics
from celery.result import AsyncResult
from rest_framework.decorators import api_view 
from rest_framework.views import APIView
from basicinformation.models import *
from django.http import Http404, HttpResponse 
from .serializers import *
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import *
from basicinformation.tasks import *
import json
from more_itertools import unique_everseen
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)
from basicinformation.tasks import *
from django.utils import timezone
from django.utils.timezone import localdate
import numpy as np
# ALL STUDENT APIs

#---------------------------------------------------------------------------------------

# returns information about test papers yet to be taken by the student 
# only returns 3 topics in a test 
class StudentPaperDetailsAPIView(APIView):

    def get(self,request,format=None):
        user = self.request.user
        me = Studs(user)
        my_tests = SSCOnlineMarks.objects.filter(student = me.profile)
        taken_ids = []
        for test in my_tests:
            taken_ids.append(test.test.id)
        new_tests = SSCKlassTest.objects.filter(testTakers = me.profile)
        tests = []
        test_details = {}
        for te in new_tests:
            if te.id not in taken_ids:
                tests.append(te.id)
                topics,num_questions = self.find_topics(te)
                test_details[te.id] =\
                        {'topics':topics[:2],'num_questions':num_questions,'subject':te.sub,'published':te.published,'creator':te.creator.teacher.name}

        return Response(test_details)

    def find_topics(self,test):
        topics = []
        tp_num = []
        for quest in test.sscquestions_set.all():
            tp_number = quest.topic_category
            tp_name = changeIndividualNames(tp_number,quest.section_category)
            topics.append(tp_name)
        topics = list(unique_everseen(topics))
        num_questions = len(test.sscquestions_set.all())
        return topics,num_questions


#---------------------------------------------------------------------------------------
class StudentPaperDetailsAndroidAPIView(APIView):

    def get(self,request,format=None):
        user = self.request.user
        me = Studs(user)
        my_tests = SSCOnlineMarks.objects.filter(student = me.profile)
        taken_ids = []
        for test in my_tests:
            taken_ids.append(test.test.id)
        new_tests = SSCKlassTest.objects.filter(testTakers = me.profile)
        tests = []
        test_details = {}
        details = []
        for te in new_tests:
            if te.id not in taken_ids:
                tests.append(te.id)
                topics,num_questions = self.find_topics(te)
                test_details =\
                        {'id':te.id,'topics':topics[:2],'num_questions':num_questions,'subject':te.sub,'published':te.published,'creator':te.creator.teacher.name}
                details.append(test_details)

        return Response(details)

    def find_topics(self,test):
        topics = []
        tp_num = []
        for quest in test.sscquestions_set.all():
            tp_number = quest.topic_category
            tp_name = changeIndividualNames(tp_number,quest.section_category)
            topics.append(tp_name)
        topics = list(unique_everseen(topics))
        num_questions = len(test.sscquestions_set.all())
        return topics,num_questions

#---------------------------------------------------------------------------------------

# When student clicks on show more topics then this api returns all the topcis
# of a particular test
class StudentShowAllTopicsOfTest(APIView):

    def post(self,request,*args,**kwargs):
        te_id = request.POST['test_id']
        test = SSCKlassTest.objects.get(id = te_id)
        topics = []
        for quest in test.sscquestions_set.all():
            number = quest.topic_category
            name = changeIndividualNames(number,quest.section_category)
            topics.append(name)
        topics = list(unique_everseen(topics))
        return Response(topics)



#---------------------------------------------------------------------------------------

# Get all the details of a test (post: test_id)

class  IndividualTestDetailsAPIView(APIView):

    def post(self,request,*args,**kwargs):
        test_id = request.POST['testid']
        test = SSCKlassTest.objects.get(id= test_id)
        topics = []
        for quest in test.sscquestions_set.all():
            number = quest.topic_category
            name = changeIndividualNames(number,quest.section_category)
            topics.append(name)
        topics = list(unique_everseen(topics))
        subject = test.sub
        num_questions = len(test.sscquestions_set.all())
        totalTime = test.totalTime
        maxMarks = test.max_marks
        published = test.published
        details ={'id':test_id,'topics':topics,'numQuestions':num_questions,'subject':subject,'time':totalTime,'maxMarks':maxMarks,'publised':published}
        return Response(details)


#-------------------------------------------------------------------------------------
# All test taking APIs

#When Start test button is clicked ('TakeTest') post request

class ConductTestFirstAPIview(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        testid = request.POST['takeTest']
        testid = int(testid)
        already_taken =\
        SSCOnlineMarks.objects.filter(student=me.profile,test__id =
                                      testid)

        quest = []
        test = SSCKlassTest.objects.get(id = testid)
        try:
            test_detail = TestDetails.objects.get(test = test)
            lenquest = test_detail.num_questions
        except:
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
        current_test = StudentCurrentTest()
        current_test.student = me.profile
        current_test.test = SSCKlassTest.objects.get(id=testid)
        current_test.save()
        context =\
                {'questPosition':nums,'te_id':testid,'how_many':lenquest,'testTime':timeTest}
        return Response(context)


class TeacherOneClickTestOneAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        testholder = TemporaryOneClickTestHolder.objects.filter(teacher= me.profile)
        if testholder:
            testholder.delete()
        my_batches = me.my_classes_names_cache()
        context = {'myBatches':my_batches}
        return Response(context)


class TeacherOneClickTestSubjectsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        clickBatch = request.POST['oneclickbatches']
        print('%s click batch' %clickBatch)
        me = Teach(self.request.user)
        testholder = TemporaryOneClickTestHolder.objects.filter(teacher= me.profile)
        if testholder:
            testholder.delete()
        my_subs = me.my_subjects_names()
        context = {'subjects': my_subs,'oneClickBatch':clickBatch}
        return Response(context)
 
class TeacherOneClickTestChaptersAPIView(APIView):
    def post(self,request,*args,**kwargs):
        subandbatch = request.POST['questionsubjects']
        me = Teach(self.request.user)
        sub = subandbatch.split(',')[0]
        batch = subandbatch.split(',')[1]
        school = me.my_school()
        all_topics = []
        sub_topics = SSCquestions.objects.filter(section_category =
                                                 sub,school = school)
        for i in sub_topics:
            all_topics.append(i.topic_category)
        all_topics = list(unique_everseen(all_topics))
        topics = me.change_topicNumbersNames(all_topics,sub)
        topics = np.array(topics)
        context = {'chapters':topics,'subject':sub,'oneclickbatch':batch}
        return Response(context)

class TeacherOneClickConfirmAPIView(APIView):
    def post(self,request,*args,**kwargs):
        user = request.user
        me = Teach(user)
        topicnumber = request.POST['chapters'];
        subject = request.POST['subject']
        batch = request.POST['batch']
        print(topicnumber)
        tps = topicnumber.split(',')
        inner = []
        outer = []
        tot = 0
        for n,a in enumerate(tps):
            a = a.replace('[','')
            a = a.replace(']','')
            inner.append(val)
            if (n+1)%2 == 0:
                outer.append(list(inner))
                inner = []


        topics_total = np.array(outer)
        print(topic_total)
        final_num = []
        final_name = []
        # creation of one click paper
        
        # class object to find out how many times has the teacher used a
        # question for that certain class
        test_quest = []  # the question containing list

        for cat,num in final_topic:
            questions = SSCquestions.objects.filter(topic_category =
                                                    cat,section_category =
                                                    subject,school=me.my_school())
            cat_quest = []
            used_quests = [] # used question containing list
            for count,quest in enumerate(questions):
                # get the number of times used object associated with the
                # question

                t_used=\
                TimesUsed.objects.filter(teacher=me.profile,quest=quest,batch=kl)

                #if quest has not been used in the batch before then add that
                #question

                if len(t_used) == 0 and count < num:
                    cat_quest.append(quest)
                # otherwise add used questions to the used_quest list
                if len(t_used) != 0:
                    used_quests.append(quest)
            # check if there are not enough new(unused) questions 
            if len(cat_quest) < num:
                try:
                    # if yes then add already used questions to list until
                    # list is equal to number of required questions
                    for count,q in enumerate(used_quests):
                        if count < len(cat_quest):
                            cat_quest.append(q)
                except Exception as e:
                    print(str(e))
            # finally add all questions to final questions list
            test_quest.extend(cat_quest)
        # setting up the test
        serializer = SSCQuestionSerializer(test_quest,many=True)
        return Response(serializer.data)
   
# For all normal create test apis

class CreateTestBatchesAPIView(APIView):
    def get(self,request,format=None):
        user = self.request.user
        me = Teach(user)
        all_klasses = me.my_classes_names_cache()
        my_batches = {'myBatches':all_klasses}
        return Response(my_batches)

class CreateTestSubjectsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        user = self.request.user
        me = Teach(user)
        ttt = request.POST['batch']
        quest = SSCquestions.objects.filter(school=
                                            me.profile.school)
        if len(quest)!=0:
            unique_chapters = me.my_subjects_names()
            test_type = 'SSC'
            context = {'subjects':
                       unique_chapters,'klass':ttt}
            return Response(context)
        else:
            noTest = 'Not Questions for this class'
            context = {'noTest':noTest}
            return Response(context)


class CreateTestChaptersAPIView(APIView):
    def post(self,request,*args,**kwargs):
        category_klass = request.POST['getChapters']
        user = self.request.user
        me = Teach(user)

        split_category = category_klass.split(',')[0]
        split_klass = category_klass.split(',')[1]
        quest = SSCquestions.objects.filter(section_category =
                                            split_category,school
                                            =me.profile.school)
        all_categories = []
        for i in quest:
            all_categories.append(i.topic_category)
        all_categories = list(unique_everseen(all_categories))
        all_categories = \
        me.change_topicNumbersNames(all_categories,split_category)
        all_categories.sort()
        context = \
                {'chapters':all_categories,'klass':split_klass,'subject':split_category}
        return Response(context)

class CreateTestQuestionsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        which_chap = request.POST['chapter_test']
        questions_list = []
        splitChap = which_chap.split(",")[0]
        splitClass = which_chap.split(",")[1]
        splitSection = which_chap.split(",")[2]
        qu = \
    SSCquestions.objects.filter(topic_category=splitChap,school=me.profile.school,section_category=splitSection)
        serializer = SSCQuestionSerializer(qu,many=True)
        return Response(serializer.data)


class CreateTestFinalAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        quest_list  = request.POST['questions_list']
        all_questions = []
        total_marks = 0

        if ',' in quest_list:
            quest_list = quest_list.split(',')
            for qu in quest_list:
                print('this is qu {}'.format(qu))
                questions = SSCquestions.objects.get(id = int(qu))
                total_marks = total_marks + questions.max_marks
                all_questions.append(questions)

        else:
                questions = SSCquestions.objects.get(id = int(quest_list))
                total_marks = total_marks + questions.max_marks
                all_questions.append(questions)

        
        serializer = SSCQuestionSerializer(all_questions,many=True)
        context =\
        {'totalMarks':total_marks,'questions':serializer.data,'number_questions':len(all_questions)}
        return Response(context)

class CreateTestAPIView(APIView):
    def post(self,request,*args,**kwargs):
        quest_list = request.POST['quest_list']
        date = request.POST['date']
        time = request.POST['time']
        klass = request.POST['batch']
        create_test_api.delay(self.request.user.id,quest_list,date,time,klass)
        context = {'success':'Successfully created'}
        return Response(context)
        


class StudentSubjectsAPIView(APIView):
    def get(self,request):
        me = Studs(self.request.user)
        return response(me.my_subjects_names)


class StudentTakeTestAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        test_id = request.POST['test_id']
        test = SSCKlassTest.objects.get(id = test_id)
        #questions = test.sscquestions_set.all()
        serializer = TestSerializer(test)
        return Response(serializer.data)

class StudentEvaluateTestAPIView(APIView):
    def post(self,request,*args,**kwargs):
        test_id = request.POST['test_id']
        answers = request.POST['answers']
        total_time = request.POST['total_time']
        answers = answers.split(',')
        inner = []
        outer = []
        tot = 0
        for n,a in enumerate(answers):
            a = a.replace('[','')
            a = a.replace(']','')
            val = int(a)
            inner.append(val)
            if (n+1)%3 == 0:
                outer.append(list(inner))
                inner = []




        outer = np.array(outer)
        me = Studs(self.request.user)
        test = SSCKlassTest.objects.get(id = test_id)
        online_marks = SSCOnlineMarks()
        online_marks.test = test
        online_marks.testTaken = localdate()
        online_marks.student = me.profile
        total_marks = 0
        right_answers = []
        wrong_answers = []
        skipped_answers = []
        all_answers = []
        details = []
        for qid,chid,time in outer:
            question = SSCquestions.objects.get(id = qid)
            all_answers.append(chid)
            if chid == -1:
                skipped_answers.append(qid)
            for ch in question.choices_set.all():
                if chid == ch.id:
                    pred = ch.predicament
                    if pred =='Correct':
                        total_marks += question.max_marks
                        right_answers.append(chid)
                    if pred == 'Wrong':
                        total_marks -= question.negative_marks
                        wrong_answers.append(chid)
            answered_detail = eval('"detail",chid')
            answered_detail = SSCansweredQuestion()
            answered_detail.quest = question
            answered_detail.time = time
            details.append(answered_detail)
        all_answers = list(unique_everseen(all_answers))
        online_marks.allAnswers = all_answers
        online_marks.marks = total_marks
        online_marks.test = test
        online_marks.rightAnswers = right_answers
        online_marks.wrongAnswers = wrong_answers
        online_marks.skippedAnswers = skipped_answers
        online_marks.timeTaken = total_time
        online_marks.save()
        for i in details:
            i.onlineMarks = online_marks
            i.save()

        serializer = SSCOnlineMarksSerializer(online_marks)
        context = {'marks':serializer.data}
        print(context)
        return Response(context)

