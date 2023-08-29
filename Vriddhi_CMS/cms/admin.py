from django.contrib import admin
from cms.models import *
from django import forms

class BoardAdmin(admin.ModelAdmin):
    list_filter = ('id', 'board_name')
    list_display = ['id', 'board_name']
    ordering = ['id']
    
class SubjectAdmin(admin.ModelAdmin):
    list_filter = ('id', 'subject_name')
    list_display = ['id', 'subject_name']
    ordering = ['id']

class AttributeAdmin(admin.ModelAdmin):
    list_display = ['types']
    ordering = ['id']
    
class CourseAdmin(admin.ModelAdmin):
    list_filter = ('subject', 'board', 'grade','type', 'language')
    list_display = ['id', 'board', 'subject', 'grade', 'type','description','picture','get_topics', 'language']
    ordering = ['id']


class CourseProviderAdmin(admin.ModelAdmin):
    search_fields = ["name","type","code"]
    list_display = ['id','name','type','code','status','language_code']

class CourseAttributeAdmin(admin.ModelAdmin):
    search_fields = ["course__subject","key","value"]
    list_display = ["course",'key','value','status',"created_by","created_on"]

class LanguageAdmin(admin.ModelAdmin):
    list_filter = ['name','code']
    list_display = ['name', 'code', 'status','created_on']
    ordering = ['id']

# Create dynamicfield for board
class BoardAdminForm(forms.ModelForm):
    board = forms.ModelChoiceField(queryset=Board.objects.all(), empty_label="Select Board")
    class Meta:
        model = Topic


class TopicAdmin(admin.ModelAdmin):
    form = BoardAdminForm #Add dynamic field
    list_filter = ('course',)
    list_display = ['title', 'course', 'url','status','priority']
    ordering = ['priority']
    # Arrange field in DjangoAdmin
    fields = ['board', 'course', 'title', 'url', 'num_sessions', 'status', 'priority']

    class Media:
        js = ('js/dynamic_course_dropdown.js',)

class TopicDetailsAdmin(admin.ModelAdmin):
    list_display = ['topic','attribute','url','drafturl','types','status','author','last_updated_date','updated_by']
    ordering = ['id']

class SubTopicsAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'topic', 'created_date', 'updated_date','author_id','created_by','updated_by','status']

        
class ContentDetailAdmin(admin.ModelAdmin):
    search_fields = ["topic__title","subtopic__name","name","url"]
    list_display = ["get_topicId","get_subtopicId","topic",'subtopic','url','name','description','status',"workstream_type",'url_host',"content_type","author","priority","version","duration","is_primary","created_by","created_on","updated_by","updated_on"]

    def get_topicId(self, obj):
        return obj.topic.id
    get_topicId.short_description = 'Topic Id'

    def get_subtopicId(self, obj):
        return obj.subtopic.id
    get_subtopicId.short_description = 'Subtopic Id'

class ContentHostMasterAdmin(admin.ModelAdmin):
    search_fields = ["name","code"]
    list_display = ["name",'code','status',"created_by","created_on"]

class ContentTypeMasterAdmin(admin.ModelAdmin):
    search_fields = ["name","code"]
    list_display = ["name",'code','status',"created_by","created_on"]

class WorkStreamTypeAdmin(admin.ModelAdmin):
    search_fields = ["name","code"]
    list_display = ["name",'code','status',"created_by","created_on"]

class ContentAuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name",'user','status',"created_by","created_on"]

class ContentMetaAttributeAdmin(admin.ModelAdmin):
    search_fields = ["content_detail__name", "key", "value"]
    list_display = ["content_detail","key", 'value', 'status', "meta_attribute_type","created_by", "created_on"]
class MetaAttributeTypeAdmin(admin.ModelAdmin):
    search_fields = ["name","code"]
    list_display = ["name",'code','status',"workstream_type","created_by","created_on"]
    
admin.site.register(Board, BoardAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseProvider, CourseProviderAdmin)
admin.site.register(CourseAttribute, CourseAttributeAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicDetails, TopicDetailsAdmin)
admin.site.register(SubTopics, SubTopicsAdmin)
admin.site.register(ContentDetail, ContentDetailAdmin)
admin.site.register(ContentHostMaster, ContentHostMasterAdmin)
admin.site.register(ContentTypeMaster, ContentTypeMasterAdmin)
admin.site.register(WorkStreamType, WorkStreamTypeAdmin)
admin.site.register(ContentAuthor, ContentAuthorAdmin)
admin.site.register(ContentMetaAttribute, ContentMetaAttributeAdmin)
admin.site.register(ContentMetaAttributeType, MetaAttributeTypeAdmin)