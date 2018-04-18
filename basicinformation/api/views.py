from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from basicinformation.models import *
from django.http import Http404, HttpResponse
from .serializers import *
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import SSCKlassTest
from basicinformation.marksprediction import *
import json
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)



class StudentListAPIView(generics.ListAPIView):
    serializer_class = StudentModelSerializer

    def get_queryset(self):
        return Student.objects.all()

# Return all the information about tests that a student has to take to be
# displayed on the home screen

class FrontPageTestAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        tests = me.toTake_Tests(6)
        all_tests = []
        for key,value in tests.items():
            topics = value['topics']
            subject = value['subject']
            test_id = key
            j_topics = json.dumps(topics)
            j_subject = json.dumps(subject)
            j_testid = json.dumps(test_id)
            j_creator = json.dumps(value['creator'])
            j_questions = json.dumps(value['num_questions'])
            psudo_test =\
            {'topics':j_topics,'subject':j_subject,'test_id':j_testid,'creator':j_creator,'num_questions':j_questions}
            all_tests.append(psudo_test)
        return Response(all_tests)
