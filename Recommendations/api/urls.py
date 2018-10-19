from django.conf.urls import url
from ..api import views

urlpatterns = [
    url(r'chapter_recommendations/$',views.StudentChapterYoutubeRecommendationsAPIView.as_view(),name='ChapterRecommendations'),
]
