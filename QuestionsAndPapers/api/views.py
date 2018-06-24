from rest_framework import generics
from celery.result import AsyncResult
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from basicinformation.models import *
from django.http import Http404, HttpResponse
from .serializers import *
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import *
import json
from more_itertools import unique_everseen
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)
from basicinformation.tasks import *


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
        totalTime = test.totalTime
        maxMarks = test.max_marks
        published = test.published
        details ={'id':test_id,'topics':topics,'subject':subject,'time':totalTime,'maxMarks':maxMarks,'publised':published}
        return Response(details)



