from django.conf.urls import url
from basicinformation.api import views

urlpatterns = [
        
    url(r'^$',views.StudentListAPIView.as_view(),name='studentList'),
    url(r'tests/$',views.FrontPageTestAPIView.as_view(),name='testList'),
    url(r'student_info/$',views.StudentDetailAPIView.as_view(),name='studentInfo'),
    url(r'brief_previous_performance/$',views.PreviousSubjectPerformance.as_view(),name='studnetPreviousPerformance'),
    url(r'upload_question/(?P<name>[\w\-]+)/$',views.UplodatQuestionsAPI.as_view(),name='uploadQuestion'),

    
]
