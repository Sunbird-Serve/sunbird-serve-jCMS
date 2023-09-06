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



    # url(r'^home/topics/?$', TopicDetailsView.as_view(), name='topic_details_by_center'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^get_filtered_courses/$', get_filtered_courses, name='get_filtered_courses'),
    url(r'^get_filtered_subject/$', get_filtered_subject, name='get_filtered_subject'),
    url(r'^search_courses/$', search_courses, name='search_courses'),

    # Create Board Course Topic Sub-Topic through API
    url(r'^api/create_course/$', create_course),
    url(r'^api/create_board/$', create_board),
    url(r'^api/create_topic/$', create_topic),
    url(r'^api/create_subtopic/$', create_subtopic),

    # Create Board Course Topic Sub-Topic through API
    url(r'^api/get_course/$', get_course),
    url(r'^api/get_board/$', get_board),
    url(r'^api/get_topic/$', get_topic),
    url(r'^api/get_subtopic/$', get_subtopic),

    # Delete Board Course Topic Sub-Topic through API
    url(r'^api/delete_board/$', delete_board, name='delete_board'),
    url(r'^api/delete_course/$', delete_course, name='delete_course'),
    url(r'^api/delete_topic/$', delete_topic, name='delete_topic'),
    url(r'^api/delete_subTopic/$', delete_subTopic, name='delete_subTopic'),


    # url(r'^api/set_key/$', set_key),

]

(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve',
               {'document_root': settings.ADMIN_MEDIA_PREFIX})

(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
       'document_root': settings.STATIC_ROOT})
