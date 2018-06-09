from django.conf.urls import url
from Private_Messages.api import views

urlpatterns = [
        
    url(r'latestMessages/$',views.TeacherLatestInbox.as_view(),name='messageList'),

    
]
