from rest_framework import generics
from django.contrib.auth.models import Group
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
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, logout as django_logout



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
               my_group = Group.objects.get(name='Students')
               my_group.user_set.add(user)

            
               teacher = Teacher.objects.get(school=school)
               if institute == 'YSM' or institute == 'BodhiAI':
                   add_subjects('SSC',stud,teacher)
               elif 'jen' in institute.lower():
                   add_subjects('Loco',stud,teacher)
               confirmation = StudentConfirmation()
               confirmation.student = user
               confirmation.school = school
               confirmation.name = stud.name
               confirmation.teacher = teacher
               confirmation.batch = batch
               confirmation.save()
               addOldTests.delay(stud.id,teacher.id,batch.id)
                

               token = Token.objects.create(user=user)
               json = serializer.data
               json['token'] =\
               {'token':token.key,'class':stud.klass.name,'school':stud.school.name}
               return Response(json,status = status.HTTP_201_CREATED)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class TeacherStudentConfirmationDisplayAPIView(APIView):

    def get(self,request,format=None):
        me = Teach(self.request.user)
        confirmations = StudentConfirmation.objects.filter(teacher =
                                                           me.profile,confirm=None)
        if len(confirmations) == 0:
            context = {'response':'No new students waiting for Batch allocation.'}
            return Response(context)
        else:
            serializer = StudentConfirmationSerializer(confirmations,many=True)

            batches = me.my_classes_objects()
            batch_serializer =BatchSerializer(batches,many=True)

            context =\
            {'confirmations':serializer.data,'batches':batch_serializer.data}
            return Response(context)


class TeacherStudentConfirmedAPIView(APIView):
    def post(self,request,*args,**kwargs):
        batch_id = request.POST['batch_id']
        confirmation_id = request.POST['confirmation_id']
        batch = klass.objects.get(id = batch_id)
        me = Teach(self.request.user)
        confirmation = StudentConfirmation.objects.get(id = confirmation_id)
        school = confirmation.school
        student_user = confirmation.student
        student = Student.objects.get(studentuser = student_user)
        subs = Subject.objects.filter(student = student)
        for i in subs:
            i.delete()
        if batch.name == 'LocoPilot':
            subGenInte = Subject(name="General-Intelligence",student=student,teacher=me.profile)
            subGenInte.save()
            subMaths = Subject(name="Quantitative-Analysis",student=student,teacher=me.profile)
            subEnglish = Subject(name="English",student=student,teacher=me.profile)
            subGenKnow = Subject(name="General-Knowledge",student=student,teacher=me.profile)
            subGenSci = Subject(name="General-Science",student=student,teacher=me.profile)
            subLocoPilot_Fitter =\
            Subject(name="FitterLocoPilot",student=student,teacher=me.profile)
            subLocoPilot_Fitter.save()
            subLocoPilot_diesel =\
            Subject(name="LocoPilot_Diesel",student=student,teacher=me.profile)
            subLocoPilot_diesel.save()



            subMaths.save()
            subEnglish.save()
            subGenSci.save()
            subGenKnow.save()

            subLocoPilot = Subject(name="ElectricalLocoPilot",student=student,teacher=me.profile)
            subLocoPilot.save()

        elif batch.name == 'SSC':
            subGenInte = Subject(name="General-Intelligence",student=student,teacher=me.profile)
            subGenInte.save()
            subMaths = Subject(name="Quantitative-Analysis",student=student,teacher=me.profile)
            subEnglish = Subject(name="English",student=student,teacher=me.profile)
            subGenKnow = Subject(name="General-Knowledge",student=student,teacher=me.profile)
            subGenSci = Subject(name="General-Science",student=student,teacher=me.profile)
            subMaths.save()
            subGenSci.save()
            subEnglish.save()
            subGenKnow.save()
            subLocoPilot =\
            Subject(name="ElectricalLocoPilot",student=student,teacher=me.profile)
            subLocoPilot.save()
            subLocoPilot_Fitter =\
            Subject(name="FitterLocoPilot",student=student,teacher=me.profile)
            subLocoPilot_Fitter.save()
            subLocoPilot_diesel =\
            Subject(name="LocoPilot_Diesel",student=student,teacher=me.profile)
            subLocoPilot_diesel.save()





        elif batch.name == 'RailwayGroupD':
            subGenInte = Subject(name="General-Intelligence",student=student,teacher=me.profile)
            subGenInte.save()
            subMaths = Subject(name="Quantitative-Analysis",student=student,teacher=me.profile)
            subGenKnow = Subject(name="General-Knowledge",student=student,teacher=me.profile)
            subGenSci = Subject(name="General-Science",student=student,teacher=me.profile)
            subMaths.save()
            subGenSci.save()
            subLocoPilot =\
            Subject(name="ElectricalLocoPilot",student=student,teacher=me.profile)
            subLocoPilot.save()
            subLocoPilot_Fitter =\
            Subject(name="FitterLocoPilot",student=student,teacher=me.profile)
            subLocoPilot_Fitter.save()
            subLocoPilot_diesel =\
            Subject(name="LocoPilot_Diesel",student=student,teacher=me.profile)
            subLocoPilot_diesel.save()




            subGenKnow.save()
        confirmation.confirm = True
        confirmation.batch = batch
        confirmation.save()
        addOldTests.delay(student.id,me.profile.id,batch.id)
        context = {'success': '{} Successfully added to  {} batch.'.format(student.name,batch.name)}
        return Response(context)


class CustomLoginAPIView(APIView):
    def post(self,request):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data["user"]
        django_login(request,user)
        token, created = Token.objects.get_or_create(user=user)
        groups = user.groups.all()
        deleteBadTests.delay()
        token_context  = \
        {'key':token.key,'user_type':groups[0].name,'name':user.first_name}
        return Response(token_context,status = 200)

class CustomLogoutAPIView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        django_logout(request)
        return Response(status=204)


def add_subjects(course,stud,teacher):
    if course == 'SSC':
        subGenInte = Subject(name="General-Intelligence",student=student,teacher=me.profile)
        subGenInte.save()
        subMaths = Subject(name="Quantitative-Analysis",student=student,teacher=me.profile)
        subEnglish = Subject(name="English",student=student,teacher=me.profile)
        subGenKnow = Subject(name="General-Knowledge",student=student,teacher=me.profile)
        subGenSci = Subject(name="General-Science",student=student,teacher=me.profile)
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

