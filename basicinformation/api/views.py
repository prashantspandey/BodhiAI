from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from basicinformation.models import *
from django.http import Http404, HttpResponse
from .serializers import *
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import *
from basicinformation.models import *
from basicinformation.marksprediction import *
import json
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)



class StudentListAPIView(generics.ListAPIView):

    def get_queryset(self):
        return Student.objects.all()

class StudentDetailAPIView(APIView):

    def get(self,request,format=None):
        user = self.request.user
        username = user.username
        email = user.email
        first_name = user.first_name
        me = Studs(user)
        school_name = me.profile.school.name
        subjects = me.my_subjects_names()

        my_details =\
        {'username':username,'email':email,'firstName':first_name,'school':school_name,'subjects':subjects}
        return Response(my_details)


        

# Return all the information about tests that a student has to take to be
# displayed on the home screen

class FrontPageTestAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        tests = me.toTake_Tests(20)
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

class PreviousSubjectPerformance(APIView):
    serializers = SSCOnlineMarksModelSerializer
    def get(self,request,format=None):
        me = Studs(self.request.user)
        all_subjects = me.my_subjects_names()
        test_info = me.test_marks_api(all_subjects)
        #online_marks = SSCOnlineMarks.objects.filter(student = me.profile)
        print(test_info)
        return Response(test_info)

class UplodatQuestionsAPI(APIView):
    def post(self,request,*args,**kwargs):
        name = request.POST['name']
        studs = Student.objects.all()
        num_studs = len(studs)
        text = 'Success! Hello %s, there are %s students at BodhiAI'\
        %(name,num_studs)
        return Response(text)
