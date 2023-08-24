from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('cms.views',
    url(r'^$', 'user_login', name='login'),
    url(r'^register/$', 'register', name='register'),
    url(r'^home/$', 'home', name='home'),
)

(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve',
               {'document_root': settings.ADMIN_MEDIA_PREFIX})

(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
       'document_root': settings.STATIC_ROOT})
