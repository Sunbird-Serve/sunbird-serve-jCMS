from django.urls import path, re_path
from django.conf import settings
from .views import *
from django.views.static import serve as static_serve
urlpatterns = [
    path('', user_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', register, name='register'),
    path('register/admin/', adminRegister, name='adminRegister'),
    path('get_courses/', get_courses, name='get_courses'),
    re_path(r'^get_topics/?$', get_topics, name='get_topics'),
    re_path(r'^get_subTopics/?$', get_subTopics, name='get_subTopics'),
    re_path(r'^home/view_course/?$', view_course, name='view_course'),
    path('home/view_content/', view_content, name='view_content'),
    path('home/content_detail/', content_detail_view, name='content_detail'),
    re_path(r'^home/getSubtopic/?$', getSubtopic, name='getSubtopic'),
    re_path(r'^subtopic/content-details/?$', SubTopicDetailsView.as_view(), name="SubTopicDetailsView"),
    path('subtopic/content_rating/', content_rating, name='content_rating'),
    path('dashboard/', dashboard, name='dashboard'),
    re_path(r'^all_course/?$', all_course, name='all_course'),
    re_path(r'^all_topic/?$', all_topic, name='all_topic'),
    re_path(r'^all_subtopic/?$', all_subtopic, name='all_subtopic'),
    re_path(r'^all_content/?$', all_content, name='all_content'),
    path('file_upload/', file_upload, name='file_upload'),
    path('download_excel_template/', download_excel_template, name='download_excel_template'),
    path('deleteBulkData/', deleteBulkData, name='deleteBulkData'),
    path('exportToExcel/', exportToExcel, name='exportToExcel'),
    # Board API
    path('api/board/create', create_or_edit_board),
    path('api/board/update', create_or_edit_board),
    re_path(r'^api/board/list/?$', get_board),
    path('api/board/delete', delete_board, name='delete_board'),


    # Subject API
    path('api/subject/create', create_or_edit_subject),
    path('api/subject/update', create_or_edit_subject),
    re_path(r'^api/subject/list/?$', get_subject),
    path('api/subject/delete', delete_subject, name='delete_subject'),

    # Course API
     path('api/course/create', create_or_edit_course),
    path('api/course/update', create_or_edit_course),
    re_path(r'^api/course/list/?$', get_course),
    path('api/course/delete', delete_course, name='delete_course'),
    # Topic API
     path('api/topic/create', create_or_edit_topic),
    path('api/topic/update', create_or_edit_topic),
    re_path(r'^api/topic/list/?$', get_topic),
    path('api/topic/delete', delete_topic, name='delete_topic'),
    # Sub-Topic API
    path('api/subtopic/create', create_or_edit_subtopic),
    path('api/subtopic/update', create_or_edit_subtopic),
    re_path(r'^api/subtopic/list/?$', get_subtopic),
    path('api/subtopic/delete', delete_subTopic, name='delete_subTopic'),
    # Content API
    path('api/content/create', create_or_edit_content),
    path('api/content/update', create_or_edit_content),
    re_path(r'^api/content/list/?$', get_content),
    path('api/content/delete', delete_content, name='delete_content'),

    re_path(r'^static/admin/(?P<path>.*)$', static_serve, {'document_root': settings.ADMIN_MEDIA_PREFIX}),
    re_path(r'^static/(?P<path>.*)$', static_serve, {'document_root': settings.STATIC_ROOT}),
]

