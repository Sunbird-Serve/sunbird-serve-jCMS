from django.contrib import admin
from cms.models import *
from django import forms
import random
import string
from django.http import HttpResponse
import hashlib
from django.conf import settings

class BoardAdmin(admin.ModelAdmin):
    list_filter = ('id', 'board')
    list_display = ['id', 'board']
    ordering = ['id']
    
class SubjectAdmin(admin.ModelAdmin):
    list_filter = ('id', 'subject_name')
    list_display = ['id', 'subject_name']
    ordering = ['id']

class AttributeAdmin(admin.ModelAdmin):
    list_display = ['types']
    ordering = ['id']
    
class CourseAdmin(admin.ModelAdmin):
    list_filter = ('subject', 'board_name', 'grade','type', 'language')
    list_display = ['id', 'board_name', 'subject', 'grade', 'type','description','picture','get_topics', 'language']
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
# class BoardAdminForm(forms.ModelForm):
#     board = forms.ModelChoiceField(queryset=Board.objects.all(), empty_label="Select Board")
#     class Meta:
#         model = Topic
#         fields = '__all__'

# class CombinedForm(forms.ModelForm):
#     board = forms.ModelChoiceField(queryset=Board.objects.all(), empty_label="Select Board", label="Board")
#     course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label=None, label="Course")
    
#     class Meta:
#         model = SubTopics
#         fields = '__all__'


class TopicAdmin(admin.ModelAdmin):
    # form = BoardAdminForm #Add dynamic field
    list_filter = ('course_id',)
    list_display = ['title', 'course_id', 'url','status','priority']
    ordering = ['priority']
    # Arrange field in DjangoAdmin
    fields = [ 'course_id', 'title', 'url', 'num_sessions', 'status', 'priority']

    class Media:
        js = ('cms/js/dynamic_course_dropdown.js',)

class TopicDetailsAdmin(admin.ModelAdmin):
    list_display = ['topic','attribute','url','drafturl','types','status','author','last_updated_date','updated_by']
    ordering = ['id']

class SubTopicsAdmin(admin.ModelAdmin):
    # form = CombinedForm
    list_display = ['id','name', 'topic', 'created_date', 'updated_date','author_id','created_by','updated_by','status']
    fields = [
        'board', 'course', 'topic', 'name', 'created_date', 'updated_date', 'author_id', 'created_by', 'updated_by', 'status'
    ]
    class Media:
        js = ('cms/js/dynamic_course_dropdown.js',)
        
class ContentDetailAdmin(admin.ModelAdmin):
    search_fields = ["topic__title","subtopic__name","name","url"]
    list_display = ["topic",'subtopic','url','name','description','status',"workstream_type",'url_host',"content_type","author","priority","version","duration","is_primary","created_by","created_on","updated_by","updated_on"]
    class Media:
        js = ('cms/js/dynamic_course_dropdown.js',)

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



class CmsAPIKeyForm(forms.ModelForm):
    userName = forms.ModelChoiceField(
        # queryset=User.objects.filter(is_staff=True), 
        queryset=User.objects.all(), 
        empty_label="Select User"
    )
    class Meta:
        model = APIKey
        fields = ['userName'] 

    def save(self, commit=True, *args, **kwargs):
        instance = super(CmsAPIKeyForm, self).save(commit=False, *args, **kwargs)
        instance.user = self.cleaned_data['userName']
        instance.user_id = instance.user.id
        user_id = instance.user_id

        random_component = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
        secret_key = settings.SECRET_KEY
        key_to_hash = '{}{}{}'.format(user_id, random_component, secret_key).encode('utf-8')
        api_key_value = hashlib.sha256(key_to_hash).hexdigest()


        # APIKey.objects.create(user=request.user, key=api_key_value)
        # return HttpResponse(f'API Key: {api_key_value}')

        # characters = string.ascii_letters + string.digits
        # api_key = ''.join(random.choice(characters) for _ in range(40))
        instance.key = api_key_value

        if commit:
            instance.save()
        return instance

class APIKeyAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at","key"]
    form = CmsAPIKeyForm
        
# admin.site.register(Board, BoardAdmin)
# admin.site.register(Subject, SubjectAdmin)
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
admin.site.register(APIKey, APIKeyAdmin)
