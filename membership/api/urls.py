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
   url(r'google_login/$',
       views.GoogleCustomLoginAndroid.as_view(),name =
       'GoogleCustomLogin'),
# register student course
   url(r'register_student_course/$',
       views.B2CRegisterCourse.as_view(),name =
       'RegisterStudentCourse'),
# B2C Normal Registration
   url(r'b2c_student_registration/$',
       views.B2CNormalRegistration.as_view(),name =
       'B2CNormalRegistration'),
# Has subjects?
   url(r'check_subject/$',
       views.CheckSubjects.as_view(),name =
       'CheckForStudentSubjects'),





]
