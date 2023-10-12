from django.conf.urls import patterns
from django.conf.urls import url
from django.conf import settings
from .views import *

urlpatterns = [
    url(r'^$', user_login, name='login'),
    url(r'^logout/$', custom_logout, name='logout'),

    url(r'^register/$', register, name='register'),
    url(r'^get_courses/$', get_courses, name='get_courses'),
    url(r'^get_topics/?$', get_topics, name='get_topics'),
    url(r'^get_subTopics/?$', get_subTopics, name='get_subTopics'),
    url(r'^home/view_course/?$', view_course, name='view_course'),
    url(r'^home/view_content/$', view_content, name='view_content'),
    url(r'^home/content_detail/$', content_detail_view, name='content_detail'),
    url(r'^home/getSubtopic/?$', getSubtopic, name='getSubtopic'),
    url(r'^subtopic/content-details/?$', SubTopicDetailsView.as_view(), name="SubTopicDetailsView"),
    url(r'^subtopic/content_rating/$', content_rating, name='content_rating'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^all_course/?$', all_course, name='all_course'),
    url(r'^all_topic/?$', all_topic, name='all_topic'),
    url(r'^all_subtopic/?$', all_subtopic, name='all_subtopic'),
    url(r'^all_content/?$', all_content, name='all_content'),
    url(r'^file_upload/$', file_upload, name='file_upload'),
    url(r'^export/$', export_to_excel, name='export_to_excel'),
    url(r'^deleteBulkData/$', deleteBulkData, name='deleteBulkData'),
    url(r'^exportToExcel/$', exportToExcel, name='exportToExcel'),
    # Board API
    url(r'^api/board/create$', create_or_edit_board),
    url(r'^api/board/update$', create_or_edit_board),
    url(r'^api/board/list?$', get_board),
    url(r'^api/board/delete$', delete_board, name='delete_board'),

    # Subject API
    url(r'^api/subject/create$', create_or_edit_subject),
    url(r'^api/subject/update$', create_or_edit_subject),
    url(r'^api/subject/list?$', get_subject),
    url(r'^api/subject/delete$', delete_subject, name='delete_subject'),

    # Course API
    url(r'^api/course/create$', create_or_edit_course),
    url(r'^api/course/update$', create_or_edit_course),
    url(r'^api/course/list?$', get_course),
    url(r'^api/course/delete$', delete_course, name='delete_course'),

    # Topic API
    url(r'^api/topic/create$', create_or_edit_topic),
    url(r'^api/topic/update$', create_or_edit_topic),
    url(r'^api/topic/list?$', get_topic),
    url(r'^api/topic/delete$', delete_topic, name='delete_topic'),

    # Sub-Topic API
    url(r'^api/subtopic/create$', create_or_edit_subtopic),
    url(r'^api/subtopic/update$', create_or_edit_subtopic),
    url(r'^api/subtopic/list?$', get_subtopic),
    url(r'^api/subtopic/delete$', delete_subTopic, name='delete_subTopic'),

    # Content API
    url(r'^api/content/create$', create_or_edit_content),
    url(r'^api/content/update$', create_or_edit_content),
    url(r'^api/content/list?$', get_content),
    url(r'^api/content/delete$', delete_content, name='delete_content'),

]

(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve',
               {'document_root': settings.ADMIN_MEDIA_PREFIX})

(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
       'document_root': settings.STATIC_ROOT})
