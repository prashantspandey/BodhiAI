from django.conf.urls import url
from leanring.api import views

urlpatterns = [
    url(r'learning_subjects/$',views.StudentListAPIView.as_view(),name='LearningSubjects'),
    url(r'learning_chapters/$',views.StudentGetChaptersAPIView.as_view(),name='GetChapters'),
]
