from django.conf.urls import patterns
from django.conf.urls import url
from django.conf import settings
from .views import *

urlpatterns = [
    url(r'^$', user_login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^get_courses/$', get_courses, name='get_courses'),
    url(r'^get_topics/?$', get_topics, name='get_topics'),
    url(r'^home/view_course/?$', view_course, name='view_course'),
    # url(r'^home/view_content/?$', view_content, name='view_content'),
    url(r'^home/view_content/$', view_content, name='view_content'),
    url(r'^home/content_detail/$', content_detail_view, name='content_detail'),
    url(r'^home/getSubtopic/?$', getSubtopic, name='getSubtopic'),
    url(r'^subtopic/content-details/?$', SubTopicDetailsView.as_view(), name="SubTopicDetailsView"),
    url(r'^subtopic/content_rating/$', content_rating, name='content_rating'),


    url(r'^logout/$', logout_view, name='logout'),
    url(r'^get_filtered_courses/$', get_filtered_courses, name='get_filtered_courses'),
    url(r'^get_filtered_subject/$', get_filtered_subject, name='get_filtered_subject'),
    url(r'^search_courses/$', search_courses, name='search_courses'),
]

(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve',
               {'document_root': settings.ADMIN_MEDIA_PREFIX})

(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
       'document_root': settings.STATIC_ROOT})
