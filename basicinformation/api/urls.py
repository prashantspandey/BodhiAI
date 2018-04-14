from django.conf.urls import url
from basicinformation.api import views

urlpatterns = [
        
    url(r'^$',views.StudentListAPIView.as_view(),name='studentList'),
    url(r'tests/$',views.FrontPageTestAPIView.as_view(),name='testList'),

    
]
