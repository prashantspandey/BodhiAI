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
    url(r'teacher_one_click_create/$',views.TeacherOneClickCreateAPIView.as_view(),name='OneClickCreate'),
    # Normal create test apis
    url(r'teacher_create_test_batches/$',views.CreateTestBatchesAPIView.as_view(),name='CreateTestBatches'),
    url(r'teacher_create_test_subjects/$',views.CreateTestSubjectsAPIView.as_view(),name='CreateTestSubjects'),
    url(r'teacher_create_test_chapters/$',views.CreateTestChaptersAPIView.as_view(),name='CreateTestChapters'),
]
