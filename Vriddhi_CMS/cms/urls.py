from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('cms.views',
    url(r'^$', 'user_login', name='login'),
    url(r'^register/$', 'register', name='register'),
    url(r'^home/$', 'home', name='home'),
    url(r'^get_courses/$', 'get_courses', name='get_courses'),
    url(r'^get_topics/$', 'get_topics', name='get_topics'),
    url(r'^home/view_course/$', 'view_course', name='view_course'),
)

(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve',
               {'document_root': settings.ADMIN_MEDIA_PREFIX})

(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
       'document_root': settings.STATIC_ROOT})
