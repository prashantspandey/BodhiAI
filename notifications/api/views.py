from rest_framework import generics
from .serializers import *
from celery.result import AsyncResult
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from basicinformation.marksprediction import *
from notifications.models import *
from rest_framework.response import Response
import requests


class OneToOneMessageAPIView(title,body,sender_token,receiver_token):
    payload = {
    "notification" : {
        "title" : str(title),
        "body" : str(body),
        "priority" : "high",
        'content_available':"true"
        },
    "to" : receiver_token,
}


    headers = {"Authorization":"key="+str(sender_token),
           "Content-Type":"application/json",
           }

    link = "https://fcm.googleapis.com/fcm/send"
    response = requests.post(link,data=json.dumps(payload),headers=headers)
    return response.status_code 


class CreateTestNotification(title,body,teacher_token,batch):
    payload = {
    "notification" : {
        "title" : str(title),
        "body" : str(body),
        "priority" : "high",
        'content_available':"true"
        },
    "to" : "/topics/test_"+str(batch),
}


    headers = {"Authorization":"key="+str(sender_token),
           "Content-Type":"application/json",
           }

    link = "https://fcm.googleapis.com/fcm/send"
    response = requests.post(link,data=json.dumps(payload),headers=headers)
    return response.status_code 


class AnnouncementNotification(title,body,teacher_token,batch):
    payload = {
    "notification" : {
        "title" : str(title),
        "body" : str(body),
        "priority" : "high",
        'content_available':"true"
        },
    "to" : "/topics/announcement_"+str(batch),
}


    headers = {"Authorization":"key="+str(sender_token),
           "Content-Type":"application/json",
           }

    link = "https://fcm.googleapis.com/fcm/send"
    response = requests.post(link,data=json.dumps(payload),headers=headers)
    return response.status_code 

class TimeTableNotification(title,body,teacher_token,batch):
    payload = {
    "notification" : {
        "title" : str(title),
        "body" : str(body),
        "priority" : "high",
        'content_available':"true"
        },
    "to" : "/topics/classes_"+str(batch),
}


    headers = {"Authorization":"key="+str(sender_token),
           "Content-Type":"application/json",
           }

    link = "https://fcm.googleapis.com/fcm/send"
    response = requests.post(link,data=json.dumps(payload),headers=headers)
    return response.status_code 


