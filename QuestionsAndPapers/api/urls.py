from django.conf.urls import url
from QuestionsAndPapers.api import views

urlpatterns = [
    url(r'paper_details/$',views.StudentPaperDetailsAPIView.as_view(),name='PaperDetails'),
    url(r'paper_details_android/$',views.StudentPaperDetailsAndroidAPIView.as_view(),name='PaperDetailsAndroid'),
    url(r'all_topics_paper/$',views.StudentShowAllTopicsOfTest.as_view(),name='AllTopics'),
]
