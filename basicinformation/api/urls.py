from django.conf.urls import url
from basicinformation.api import views
urlpatterns = [
    url(r'^$',views.StudentListAPIView.as_view(),name='studentList'),
    url(r'student_info/$',views.StudentDetailAPIView.as_view(),name='studentInfo'),
    url(r'last_test_performance_teacher/$',views.LastClassTestPerformanceTeacherAPI.as_view(),name='last_performance_teacher'),
    url(r'teacher_weak_areas_brief/$',views.TeacherWeakAreasBrief.as_view(),name='teacher_weak_areas_brief'),
    url(r'teacher_weak_areas_brief_android/$',views.TeacherWeakAreasBriefAndroid.as_view(),name='teacher_weak_areas_brief_Android'),
    url(r'teacher_tests_overview/$',views.TeacherTestsOverview.as_view(),name='teacher_tests_overview'),
    url(r'teacher_tests_overview_android/$',views.TeacherTestsOverviewAndroid.as_view(),name='teacher_tests_overview_Android'),
    url(r'teacher_hard_questions/$',views.TeachersHardQuestionsAPIView.as_view(),name='TeacherHardQuestions'),
    url(r'teacher_hard_questions_latest/$',views.TeachersHardQuestions3TestsAPIView.as_view(),name='TeacherHardQuestionsLatest'),
    url(r'teacher_subjectNames/$',views.TeacherSubjectsAPIView.as_view(),name='TeacherSubjects'),
    url(r'teacher_classNames/$',views.TeacherBatchesAPIView.as_view(),name='TeacherBatches'),
    url(r'teacher_generateRankTable/$',views.GenerateRankTableAPIView.as_view(),name='TeacherGenerateRankTable'),
    url(r'teacher_TestBasicDetails/$',views.TeacherTestBasicDetailsAPIView.as_view(),name='TeacherTestBasicDetails'),
    url(r'teacher_TestQuestionsDetails/$',views.TeacherTestQuestionsAPIView.as_view(),name='TeacherTestQuestionsDetails'),
    url(r'student_previous_performance/$',views.StudentPreviousPerformanceBriefAPIView.as_view(),name='StudentPreviousPerformance'),
    url(r'student_previous_performance_android/$',views.StudentPreviousPerformanceBriefAndroidAPIView.as_view(),name='StudentPreviousPerformanceAndroid'),
    url(r'student_proficiency/$',views.StudentTopicWiseProficiency.as_view(),name='StudentProficiency'),
    url(r'student_timing_topicwise/$',views.StudentAverageTimeTopicAPIView.as_view(),name='StudentTimingTopicWise'),
    url(r'student_previous_performance_detailed/$',views.StudentTakenTestsDetailsAPIView.as_view(),name='StudentPreviousPerformanceDetailed'),


]
