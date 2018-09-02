from django.conf.urls import url
from membership.api import views


urlpatterns = [

   url(r'custom_registration/$', views.CustomRegistration.as_view(),name =
       'CustomRegistration')
]
