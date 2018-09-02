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
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User



class CustomRegistration(APIView):
   def post(self,request,*args,**kwargs):
       username = request.POST['username']
       password = request.POST['password']
       name = request.POST['name']
       institute = request.POST['institute']
       context =\
               {'username':username,'password':password,'first_name':name}
       serializer = CustomRegistrationSerializer(data = context)
       if serializer.is_valid():
           user = serializer.save()
           if user:
               school = School.objects.get(name=institute)
               batch = klass.objects.get(school=school,name='Outer')
               stud = Student(studentuser = user,klass = batch,school =school)
               stud.studentuser.first_name = name
               stud.name = name
               stud.save()

               teacher = Teacher.objects.get(school=school)
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
               subMaths.save()
               subEnglish.save()
               subGenSci.save()
               subGenKnow.save()


               token = Token.objects.create(user=user)
               json = serializer.data
               json['token'] =\
               {'token':token.key,'class':stud.klass.name,'school':stud.school.name}
               return Response(json,status = status.HTTP_201_CREATED)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
