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




class StudentListAPIView(generics.ListAPIView):
    serializer_class = StudentModelSerializer

    def get_queryset(self):
        return Student.objects.all()
