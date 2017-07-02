from django.conf.urls import url
from QuestionsAndPapers import views

app_name = 'QuestionsAndPapers'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^createTest/$',views.create_test,name= 'createTest'),
    url(r'^addQuestions/$',views.add_questions,name= 'addQuestions'),
    url(r'^seeTests/$',views.see_Test,name= 'seeTests'),
    #url(r'^teacher/(?P<grade>\d+)/$', views.current_analysis,
        #name='current_analysis'),
    #url(r'teach/$',views.teacher_home_page, name= 'teacherHomePage'),
    #url(r'teacher/update/$',views.teacher_update_page,name='teacher_update_page'),

]
