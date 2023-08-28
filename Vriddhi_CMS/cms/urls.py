from django.conf.urls import patterns
from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$', user_login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^home/$', home, name='home'),
]


