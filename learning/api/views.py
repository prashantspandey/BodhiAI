from rest_framework import generics
from django.utils import timezone
from celery.result import AsyncResult 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from basicinformation.models import *
from django.http import Http404, HttpResponse
from .serializers import *
from QuestionsAndPapers.api.views import *
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import *
from basicinformation.models import * 
from basicinformation.marksprediction import * 
from membership.api.views import add_subjects
import json
from basicinformation.nameconversions import *
from membership.api.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)
from basicinformation.tasks import *
import datetime
from .serializers import *

class StudentSubjectsAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = me.my_subjects_names()
        context = {'subjects':subjects}
        return Response(context)


class StudentGetChaptersAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        subject = request.POST['subject']
        chapters = SubjectChapters.objects.filter(subject = subject)
        chapter_serializer = SubjectChapterSerializer(chapters,many=True)
        return Response(chapter_serializer.data)

