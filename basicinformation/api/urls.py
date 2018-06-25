from django.conf.urls import url
from basicinformation.api import views

urlpatterns = [
    url(r'^$',views.StudentListAPIView.as_view(),name='studentList'),
    url(r'student_info/$',views.StudentDetailAPIView.as_view(),name='studentInfo'),
    url(r'last_test_performance_teacher/$',views.LastClassTestPerformanceTeacherAPI.as_view(),name='last_performance_teacher'),
    url(r'teacher_weak_areas_brief/$',views.TeacherWeakAreasBrief.as_view(),name='teacher_weak_areas_brief'),
    url(r'teacher_tests_overview/$',views.TeacherTestsOverview.as_view(),name='teacher_tests_overview'),
    url(r'student_previous_performance/$',views.StudentPreviousPerformanceBriefAPIView.as_view(),name='StudentPreviousPerformance'),
    url(r'student_previous_performance_android/$',views.StudentPreviousPerformanceBriefAndroidAPIView.as_view(),name='StudentPreviousPerformanceAndroid'),
    url(r'student_proficiency/$',views.StudentTopicWiseProficiency.as_view(),name='StudentProficiency'),
    url(r'student_timing_topicwise/$',views.StudentAverageTimeTopicAPIView.as_view(),name='StudentTimingTopicWise'),
    url(r'student_previous_performance_detailed/$',views.StudentTakenTestsDetailsAPIView.as_view(),name='StudentPreviousPerformanceDetailed'),


]
