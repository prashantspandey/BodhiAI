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
import requests

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
               print('{} institute'.format(institute))
               if 'jen' in institute.lower():
                   institute = 'JEN'
               if 'ysm' in institute.lower():
                   institute = 'YSM'
               if 'bodhiai' in institute.lower():
                   institute = "BodhiAI"
               school = School.objects.get(name=institute)
               print('{} school'.format(school.name))
               batch = klass.objects.get(school=school,name='Outer')
               stud = Student(studentuser = user,klass = batch,school =school)
               stud.studentuser.first_name = name
               stud.name = name
               stud.save()
               my_group = Group.objects.get(name='Students')
               my_group.user_set.add(user)

            
               teacher = Teacher.objects.get(school=school)
               if institute == 'YSM' or institute == 'BodhiAi':
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
               add_announcements_newStudent.delay(stud.id,batch.id)

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
        student.klass = batch
        student.save()
        subs = Subject.objects.filter(student = student)
        for i in subs:
            i.delete()
        custom_batches = CustomBatch.objects.filter(school = school)
        for cb in custom_batches:
            custom_bat = cb.klass
            if batch == custom_bat:
                subjects = cb.subjects
                for sub in subjects:
                    addSub = Subject(name =
                                     sub.strip(),student=student,teacher=me.profile)
                    addSub.save()
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
            subCivil =\
            Subject(name='Civil_Loco_Pilot_Tech',student=student,teacher=me.profile)


            subCivil.save() 
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
            subCivil =\
            Subject(name='Civil_Loco_Pilot_Tech',student=student,teacher=me.profile)
            subCivil.save()
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
            subCivil =\
            Subject(name='Civil_Loco_Pilot_Tech',student=student,teacher=me.profile)



            subCivil.save()
            subGenKnow.save()
        confirmation.confirm = True
        confirmation.batch = batch
        confirmation.save()
        addOldTests.delay(student.id,me.profile.id,batch.id)
        add_announcements_newStudent.delay(student.id,batch.id)
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
        try:
            student_details = StudentDetails.objects.get(student = user)
            student = Student.objects.get(studentuser = user)
            klass_name = student.klass.name

            token_context  = \
                {'key':token.key,'user_type':groups[0].name,'name':user.username,'photo':student_details.photo,'batch':klass_name}

        except:
            token_context  = \
                {'key':token.key,'user_type':groups[0].name,'name':user.username,'photo':None}

        return Response(token_context,status = 200)

class CustomLogoutAPIView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        django_logout(request)
        return Response(status=204)


def add_subjects(course,stud,teacher):
    if course == 'SSC':
        subGenInte =\
        Subject(name="General-Intelligence",student=stud,teacher=teacher)
        subGenInte.save()
        subMaths =\
        Subject(name="Quantitative-Analysis",student=stud,teacher=teacher)
        subEnglish = Subject(name="English",student=stud,teacher=teacher)
        subGenKnow =\
        Subject(name="General-Knowledge",student=stud,teacher=teacher)
        subGenSci = Subject(name="General-Science",student=stud,teacher=teacher)
        subCivil =\
        Subject(name='Civil_Loco_Pilot_Tech',student=stud,teacher=teacher)
        subMaths.save()
        subGenSci.save()
        subEnglish.save()
        subGenKnow.save()
        subCivil.save()
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
       subCivil =\
       Subject(name='Civil_Loco_Pilot_Tech',student=stud,teacher=teacher)



       subCivil.save()
       subMaths.save()
       subEnglish.save()
       subGenSci.save()
       subGenKnow.save()

class FireBaseToken(APIView):
    def post(self,request,*args,**kwargs):
        token = request.POST['token']
        user = self.request.user
        try:
            firebase_token = FirebaseToken.objects.get(user = user)
            firebase_token.token = token
            firebase_token.save()
        except Exception as e:
            print(str(e))
            firebase_token = FirebaseToken()
            firebase_token.user = user
            firebase_token.token = token
            firebase_token.save()
        context = {'token': 'token saved'}
        return Response(context)

class ResetPassword(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        username = data['username']
        phone = data['phone']
        password = data['password']
        try:
            user = User.objects.get(username=username)
            message = 'This is your new password '+str(password)
            send_url = 'http://sms.trickylab.com/http-api.php?username=bodhiai&password=123456&senderid=Bodhii&route=1&number='+phone+'&message='+message+''
            r = requests.get(send_url)
            print('status code {}'.format(r.status_code))
            print(r.text)
            user.set_password(str(password))
            user.save()
            return Response({'type':'success'})

        except:
            return Response({'type':'failed'})


class GoogleCustomLoginAndroid(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        user_id = data['user_id']
        email = data['email']
        display_name = data['display_name']
        photo = data['photo']
        try:
            user = User.objects.create_user(username=user_id, email=email,\
                                                password='newpassword')
            institute = "BodhiAI"
            school = School.objects.get(name=institute)
            print('{} school'.format(school.name))
            batch = klass.objects.get(school=school,name='Outer')
            stud = Student(studentuser = user,klass = batch,school =school)
            stud.studentuser.first_name = display_name
            stud.name = display_name
            stud.save()
            student_details = StudentDetails()
            student_details.student = user
            student_details.photo = photo
            student_details.email = email
            student_details.save()
            my_group = Group.objects.get(name='Students')
            my_group.user_set.add(user)


            teacher = Teacher.objects.get(school=school)
            if institute == 'YSM' or institute == 'BodhiAi':
               add_subjects('SSC',stud,teacher)
            confirmation = StudentConfirmation()
            confirmation.student = user
            confirmation.school = school
            confirmation.name = stud.name
            confirmation.teacher = teacher
            confirmation.batch = batch
            confirmation.save()
            addOldTests.delay(stud.id,teacher.id,batch.id)
            add_announcements_newStudent.delay(stud.id,batch.id)

            token = Token.objects.create(user=user)
            json = serializer.data
            json['token'] =\
                    {'token':token.key,'class':stud.klass.name,'school':stud.school.name,'photo':photo,'name':display_name}
            return Response(json,status = status.HTTP_201_CREATED)

            print('new user created')
        except Exception as e:
            print(str(e))
            user = User.objects.get(username=user_id)
            django_login(request,user)
            token, created = Token.objects.get_or_create(user=user)
            groups = user.groups.all()
            student = Student.objects.get(studentuser = user)
            klass_name = student.klass.name
            try:
                student_details = StudentDetails.objects.get(student = user)

                token_context  = \
                    {'key':token.key,'user_type':groups[0].name,'name':student.name,'photo':student_details.photo,'batch':klass_name}

            except:
                token_context  = \
                {'key':token.key,'user_type':groups[0].name,'name':student.name,'photo':None,'batch':klass_name}
            return Response(token_context,status = 200)



