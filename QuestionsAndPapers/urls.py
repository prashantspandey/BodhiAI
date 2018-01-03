from django.conf.urls import url
from QuestionsAndPapers import views

app_name = 'QuestionsAndPapers'

urlpatterns = [
    #url(r'^$', views.home, name='home'),
    url(r'^createTest/$',views.create_test,name= 'createTest'),
    url(r'^addQuestions/$',views.add_questions,name= 'addQuestions'),
    url(r'^seeTests/$',views.see_Test,name= 'seeTests'),
    url(r'^publishTest/$',views.publish_test,name= 'publishTest'),
    url(r'^students_homework_tests/$',views.student_my_tests,name=
        'studentMyOnlineTests'),
    url(r'^show_online_tests/$',views.student_show_onlineTests,name=
        'studentShowOnlineTest'),
    url(r'^conduct_Test/$',views.conduct_Test,name= 'conductTest'),
    url(r'^create_instant_test/$',views.create_oneclick_test,name='oneClickTest'),
    url(r'^create_pattern_test/$',views.create_pattern_test,name='patternTest'),
    url(r'^create_pattern_test2/$',views.pattern_test,name='patternTest2'),
    
    url(r'^one_click_test/$',views.oneclick_test,name='oneClickTest2'),
    url(r'^FinishedResult/(\d+)/$',views.show_finished_test,name='showFinishedTest'),
    url(r'^EvaluateTest/$',views.evaluate_test,name='EvaluateTest'),

    #url(r'^teacher/(?P<grade>\d+)/$', views.current_analysis,
        #name='current_analysis'),
    #url(r'teach/$',views.teacher_home_page, name= 'teacherHomePage'),
    #url(r'teacher/update/$',views.teacher_update_page,name='teacher_update_page'),

]
