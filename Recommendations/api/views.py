from django.utils import timezone
from rest_framework import generics
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
from basicinformation.tasks import *
from Recommendations.api.serializers import *
from Recommendations.models import *
import datetime
from apiclient.discovery import build 
from apiclient.errors import HttpError 
from oauth2client.tools import argparser 
import pandas as pd 
import pprint 
#import matplotlib.pyplot as pd 



DEVELOPER_KEY = "AIzaSyDOW6Nt-1jpzxcEbypSpJ-ObCsZHjYBjPA" 


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"



def\
youtube_search(q,max_results=5,order='relevance',token=None,location=None,location_radius=None):
    print('got here')
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=
                    DEVELOPER_KEY)
    search_response = youtube.search().list(
        q = q,
        type = "video",
        pageToken = token,
        order = order,
        part = "id,snippet",
        maxResults = max_results,
        location = location,
        locationRadius = location_radius).execute()

    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    favoriteCount = []
    category = []
    tags = []
    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title.append(search_result['snippet']['title'])

            videoId.append(search_result['id']['videoId'])

            response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()

            channelId.append(response['items'][0]['snippet']['channelId'])
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
            categoryId.append(response['items'][0]['snippet']['categoryId'])
            favoriteCount.append(response['items'][0]['statistics']['favoriteCount'])
            viewCount.append(response['items'][0]['statistics']['viewCount'])
            likeCount.append(response['items'][0]['statistics']['likeCount'])
            dislikeCount.append(response['items'][0]['statistics']['dislikeCount'])

        if 'commentCount' in response['items'][0]['statistics'].keys():
            commentCount.append(response['items'][0]['statistics']['commentCount'])

        else:
            commentCount.append([])

        if 'tags' in response['items'][0]['snippet'].keys():
            tags.append(response['items'][0]['snippet']['tags'])
        else:
            tags.append([])

    youtube_dict = {'tags':tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'likeCount':likeCount,'dislikeCount':dislikeCount,'commentCount':commentCount,'favoriteCount':favoriteCount}

    return youtube_dict




