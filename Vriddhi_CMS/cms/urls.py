from django.conf.urls import patterns
from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$', user_login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^home/$', home, name='home'),
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
    url(r'^search_courses/$', search_courses, name='search_courses'),
    # url(r'^get_filtered_subtopic/$', get_filtered_subtopic, name='get_filtered_subtopic'),
    
]


