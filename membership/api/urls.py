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
   url(r'custom_login/$',
       views.CustomLoginAPIView.as_view(),name =
       'CustomLogin'),
   url(r'custom_logout/$',
       views.CustomLogoutAPIView.as_view(),name =
       'CustomLogout'),
   url(r'firebase_token/$',
       views.FireBaseToken.as_view(),name =
       'FireBaseToken'),
   url(r'reset_password/$',
       views.ResetPassword.as_view(),name =
       'ResetPassword'),




]
