from rest_framework import generics
from .serializers import *
from celery.result import AsyncResult
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from basicinformation.api.serializers import *
from basicinformation.marksprediction import *
from Private_Messages.models import *
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)

class TeacherLatestInbox(generics.ListAPIView):
    serializer_class = PrivateMessageModalSerializer
    def get_queryset(self):
        return PrivateMessage.objects.filter(receiver =
                                             self.request.user)


class StudentSendMessage(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        school = me.get_school()
        teacher = Teacher.objects.filter(school = school)
        teacher_serializer = TeacherSerializer(teacher,many=True)
        return Response(teacher_serializer.data)

class StudentSendMessageFinal(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        teacher_id = request.POST['teacher_id']
        message = request.POST['message']
        teacher = Teacher.objects.get(id = teacher_id)
        send_message = PrivateMessage()
        send_message.sender = self.request.user
        send_message.receiver = teacher.teacheruser
        send_message.body = message
        send_message.save()
        context = {'teacher':teacher.name,'message':message}
        return Response(context)

class TeacherCreateAnnouncementAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        batches = me.my_classes_names_cache()
        context = {'batches':batches}
        return Response(context)


class TeacherCreateAnnouncemntFinalAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        batch_name = request.POST['batch_name']
        message = request.POST['message']
        school = me.my_school()
        batch = klass.objects.get(school=school,name=batch_name)
        students = Student.objects.filter(school=school,klass=batch)
        announcement = Announcement()
        announcement.announcer = me.profile
        announcement.text = message
        announcement.save()
        for stud in students:
            announcement.listener.add(stud)

        announcement.save()
        context = {'messsage':message, 'batch':batch.name}
        return Response(context)

class StudentShowAnnnouncementAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        my_announcement = Announcement.objects.filter(listener = me.profile)
        serializer = AnnouncementSerializer(my_announcement,many=True)
        return Response(serializer.data)


