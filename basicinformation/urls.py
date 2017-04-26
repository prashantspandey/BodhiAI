from django.conf.urls import url
from basicinformation import views

app_name = 'basic'

urlpatterns = [
    url(r'^$', views.home, name='home'),

]
