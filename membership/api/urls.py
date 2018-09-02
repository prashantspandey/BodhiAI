from django.conf.urls import url
from membership.api import views


urlpatterns = [

   url(r'custom_registration/$', views.CustomRegistration.as_view(),name =
       'CustomRegistration'),
   url(r'teacher_confirmation_detail/$',
       views.TeacherStudentConfirmationDisplayAPIView.as_view(),name =
       'TeacherConfirmationDetail'),
   url(r'teacher_confirmation_final/$',
       views.TeacherStudentConfirmedAPIView.as_view(),name =
       'TeacherConfirmationDone'),

]
