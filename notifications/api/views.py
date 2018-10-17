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


JEN_KEY = 'AIzaSyCnTXtRcZgSXhNSYA_wAWNIHrYBBru0Q-s'
BODHIAI_KEY = 'AIzaSyBPReyXJ8R4K18wdVw8ij7mjbdj3DNUUPI'
def  OneToOneMessageAPIView(title,body,school,receiver_token):
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
    print('{} response code message'.format(response.status_code))
    return response.status_code


def CreateTestNotification(title,body,school,batch):
    if 'JEN' in school:
        sender_token = JEN_KEY
    elif 'BodhiAI' in school:
        sender_token = BODHIAI_KEY

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
    print('{} payload {} headers'.format(payload,headers))
    response = requests.post(link,data=json.dumps(payload),headers=headers)
    print('{} response code create test'.format(response.status_code))
    return response.status_code


def AnnouncementNotification(title,body,school,batch):
    if 'JEN' in school:
        sender_token = JEN_KEY
    elif 'BodhiAI' in school:
        sender_token = BODHIAI_KEY
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
    print('{} response code announcement'.format(response.status_code))
    return response.status_code

def TimeTableNotification(title,body,school,batch):
    if 'JEN' in school:
        sender_token = JEN_KEY
    elif 'BodhiAI' in school:
        sender_token = BODHIAI_KEY

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
    print('{} response code time table'.format(response.status_code))
    return response.status_code


