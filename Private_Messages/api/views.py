from rest_framework import generics
from .serializers import *
from celery.result import AsyncResult
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from Private_Messages.models import *
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)

class TeacherLatestInbox(generics.ListAPIView):
    serializer_class = PrivateMessageModalSerializer
    def get_queryset(self):
        return PrivateMessage.objects.filter(receiver =
                                             self.request.user)[:5]


