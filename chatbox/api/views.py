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
import random
from basicinformation.nameconversions import *
from membership.api.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)
from basicinformation.tasks import *
import datetime
from decimal import Decimal



class ChatBoxAPIView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        page = data['page']
        language = data['language']
        if page == 'testResult':
            test_id = data['test_id']
            marks = SSCOnlineMarks.objects.get(test__id = test_id)


