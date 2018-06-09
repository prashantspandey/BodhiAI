from django.conf.urls import url
from basicinformation.api import views

urlpatterns = [
        
    url(r'^$',views.StudentListAPIView.as_view(),name='studentList'),
    url(r'tests/$',views.FrontPageTestAPIView.as_view(),name='testList'),
    url(r'student_info/$',views.StudentDetailAPIView.as_view(),name='studentInfo'),
    url(r'brief_previous_performance/$',views.PreviousSubjectPerformance.as_view(),name='studnetPreviousPerformance'),
    url(r'upload_question/(?P<name>[\w\-]+)/$',views.UplodatQuestionsAPI.as_view(),name='uploadQuestion'),
    url(r'last_test_performance_teacher/$',views.LastClassTestPerformanceTeacherAPI.as_view(),name='last_performance_teacher'),
    url(r'teacher_weak_areas_brief/$',views.TeacherWeakAreasBrief.as_view(),name='teacher_weak_areas_brief'),
    url(r'teacher_tests_overview/$',views.TeacherTestsOverview.as_view(),name='teacher_tests_overview'),


    
]
