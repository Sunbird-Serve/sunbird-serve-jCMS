from django.conf.urls import patterns
from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$', user_login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^home/$', home, name='home'),
    url(r'^get_courses/$', get_courses, name='get_courses'),
    url(r'^get_topics/$', get_topics, name='get_topics'),
]

(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve',
               {'document_root': settings.ADMIN_MEDIA_PREFIX})

(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
       'document_root': settings.STATIC_ROOT})
