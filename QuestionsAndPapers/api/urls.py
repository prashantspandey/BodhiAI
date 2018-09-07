from django.conf.urls import url
from QuestionsAndPapers.api import views

urlpatterns = [
    url(r'paper_details/$',views.StudentPaperDetailsAPIView.as_view(),name='PaperDetails'),
    url(r'paper_details_android/$',views.StudentPaperDetailsAndroidAPIView.as_view(),name='PaperDetailsAndroid'),
    url(r'all_topics_paper/$',views.StudentShowAllTopicsOfTest.as_view(),name='AllTopics'),
    url(r'individual_test_details/$',views.IndividualTestDetailsAPIView.as_view(),name='IndividualTestDetails'),
    # test taking apis
    url(r'individual_test_first/$',views.ConductTestFirstAPIview.as_view(),name='ConductTestFirst'),
    # Once click test apis
    url(r'teacher_one_click_first/$',views.TeacherOneClickTestOneAPIView.as_view(),name='OneClickOne'),
    url(r'teacher_one_click_subject/$',views.TeacherOneClickTestSubjectsAPIView.as_view(),name='OneClickSubjects'),
    url(r'teacher_one_click_chapters/$',views.TeacherOneClickTestChaptersAPIView.as_view(),name='OneClickChapters'),
    url(r'teacher_one_click_confirm/$',views.TeacherOneClickConfirmAPIView.as_view(),name='OneClickConfirm'),
    url(r'teacher_one_click_final/$',views.TeacherOneClickFinalAPIView.as_view(),name='OneClickFinal'),
    # Normal create test apis
    url(r'teacher_create_test_batches/$',views.CreateTestBatchesAPIView.as_view(),name='CreateTestBatches'),
    url(r'teacher_create_test_subjects/$',views.CreateTestSubjectsAPIView.as_view(),name='CreateTestSubjects'),
    url(r'teacher_create_test_chapters/$',views.CreateTestChaptersAPIView.as_view(),name='CreateTestChapters'),
    url(r'teacher_create_test_questions/$',views.CreateTestQuestionsAPIView.as_view(),name='CreateTestQuestions'),
    url(r'teacher_create_test_final/$',views.CreateTestFinalAPIView.as_view(),name='CreateTestFinal'),
    url(r'teacher_create_test/$',views.CreateTestAPIView.as_view(),name='CreateTestAPI'),
    # Student profile apis
    url(r'student_subjects/$',views.StudentSubjectsAPIView.as_view(),name='StudentSubjects'),
    # Student Take test APIs
    url(r'take_test/$',views.StudentTakeTestAPIView.as_view(),name='StudentTakeTest'),
    # Student evaluate test APIs
    url(r'evaluate_test_android/$',views.StudentEvaluateTestAPIView.as_view(),name='StudentEvaluateTest'),


]
