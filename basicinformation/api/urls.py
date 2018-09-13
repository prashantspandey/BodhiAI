from django.conf.urls import url
from basicinformation.api import views
urlpatterns = [
    url(r'^$',views.StudentListAPIView.as_view(),name='studentList'),
    url(r'user_type/$',views.TeacherorStudentAPIView.as_view(),name='UserType'),
    url(r'student_info/$',views.StudentDetailAPIView.as_view(),name='studentInfo'),
    url(r'last_test_performance_teacher/$',views.LastClassTestPerformanceTeacherAPI.as_view(),name='last_performance_teacher'),
    url(r'teacher_weak_areas_brief/$',views.TeacherWeakAreasBrief.as_view(),name='teacher_weak_areas_brief'),
    url(r'teacher_weak_areas_brief_android/$',views.TeacherWeakAreasBriefAndroid.as_view(),name='teacher_weak_areas_brief_Android'),
    url(r'teacher_weak_areas_detail/$',views.TeacherWeakAreasDetailAPIView.as_view(),name='TeacherWeakAreasDetailAPI'),
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
    url(r'student_proficiency_android/$',views.StudentTopicWiseProficiencyAndroid.as_view(),name='StudentProficiencyAndroid'),
    url(r'student_timing_topicwise/$',views.StudentAverageTimeTopicAPIView.as_view(),name='StudentTimingTopicWise'),
    url(r'student_timing_topicwise_android/$',views.StudentAverageTimeTopicAndroidAPIView.as_view(),name='StudentTimingTopicWiseAndroid'),
    url(r'student_previous_performance_detailed/$',views.StudentTakenTestsDetailsAPIView.as_view(),name='StudentPreviousPerformanceDetailed'),
# Time Table APIs
    url(r'teacher_time_table/$',views.TeacherTimeTableAPIView.as_view(),name='TeacherTimeTable'),
# teacher create Time Table
    url(r'teacher_create_TimeTable/$',views.TeacherCreateTimeTable.as_view(),name='TeacherCreateTimeTable'),
# teacher get batches for Time Table
    url(r'teacher_create_TimeTableBatches/$',views.TeacherTimeTableFirst.as_view(),name='TeacherTimeTableBatches'),
# Student Test Performance Detail
    url(r'student_individual_test_detail/$',views.StudentTestPerformanceDetailedAPIView.as_view(),name='StudentTestPastPerformanceDetail'),
# Custom Registration
    #url(r'custom_registration/$',views.CustomRegistrationAPIView.as_view(),name='CustomRegistration'),
# Student Test Rank
    url(r'student_test_rank/$',views.StudentFindMyRankAPIView.as_view(),name='StudentTestRank'),
# Teacher all Student List
    url(r'teacher_student_list/$',views.TeacherShowAllStudentsAPIView.as_view(),name='TeacherStudentList'),
# Student Show Profile
    url(r'student_profile/$',views.StudentShowDetialsAPIView.as_view(),name='StudentDetailsAPI'),
# Student Write Profile
    url(r'student_edit_profile/$',views.StudentFillDetailsAPIView.as_view(),name='StudentWriteDetails'),
# Student Detailed Average Timings
    url(r'student_averageTiming_detail/$',views.StudentAverageTimingDetailAPIView.as_view(),name='StudentAverageTimingDetailed'),
# Teacher Individual Analysis 
    url(r'teacher_analysis_showTests/$',views.TeacherAnalysisShowTestsAPIView.as_view(),name='TeacherAnalysisShowTests'),
# Teacher Individual Send Students 
    url(r'teacher_analysis_sendStudents/$',views.TeacherAnalysisIndividualSendStudentAPIView.as_view(),name='TeacherAnalysisIndividualSendStudent'),
# Teacher Individual Student Test Analysis 
    url(r'teacher_analysis_student_analysis/$',views.TeacherAnalysisIndividualStudentAPIView.as_view(),name='TeacherAnalysisIndividualStudentFinal'),


]
