from django.conf.urls import url
from learning.api import views

urlpatterns = [
    url(r'learning_subjects/$',views.StudentSubjectsAPIView.as_view(),name='LearningSubjects'),
    url(r'learning_chapters/$',views.StudentGetChaptersAPIView.as_view(),name='GetChapters'),
]
