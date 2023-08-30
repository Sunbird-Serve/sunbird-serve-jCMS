from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    id = models.AutoField(primary_key=True)
    board_name = models.CharField(max_length=255)

    def __str__(self):
        return self.board_name



class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)

    def __str__(self):
        return self.subject_name


class Language(models.Model):
    name = models.CharField(max_length=255, null=False)
    code = models.CharField(max_length=255, null=False)
    status = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True, null=False)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, default=None)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, default=None)
    grade = models.CharField(max_length=30,null=True, blank=False,db_index=True)
    type = models.CharField(max_length=30,null=True, blank=True,db_index=True)
    description = models.TextField(max_length=2048, null=True, blank=True)
    picture = models.FileField(upload_to='static/uploads/images', null=True, blank=True)
    status = models.CharField(max_length=50,choices=(('active', 'Active'), ('inactive', 'Inactive')),default="active")
    language = models.ForeignKey(Language, null=True, blank=True)
    availabilityType = models.CharField(max_length=50, choices=(('1', 'Web1.0 Only'), ('2', 'Mobile App only'),('3', 'All Platforms')), default="3")
    #age_group = models.CharField(max_length=30,null=True, blank=True)

    @property
    def topics():
        return Topics.objects.all()

    def get_topics(self):
        topics = self.topic_set.all()
        return ',<br/>'.join([unicode(t) for t in topics])

    get_topics.short_description = 'Topics'
    get_topics.allow_tags = True

    def __unicode__(self):
        return "%s-%s-%s" % (self.board, self.subject, self.grade)

class CourseProvider(models.Model):
    name = models.CharField(max_length=1024, null=True, blank=True)
    type = models.CharField(max_length=256,choices=(('State', 'State'),
            ('centralboard','centralboard'), ('stateboard','stateboard'),
            ('evidyaloka','evidyaloka'), ('Other', 'Other')), default="State")
    code = models.CharField(max_length=1024, null=True, blank=True)
    language_code = models.CharField(max_length=1024, null=True, blank=True)
    status = models.BooleanField(default=True)

    created_by = models.ForeignKey(User, null=True, related_name='course_providers_created_by', blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='course_providers_updated_by', blank=True)
    created_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.name


class CourseAttribute(models.Model):
    key = models.CharField(max_length=256, null=False, blank=False)
    value = models.CharField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, null=True, related_name="course_attributes_created_by", blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name="course_attributes_updated_by", blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    course = models.ForeignKey(Course, related_name="ca_course_id", null=True)
    class Meta:
        verbose_name = ('Coure Attribute')

    def __unicode__(self):
        return self.key


class Topic(models.Model):
    # board = models.ForeignKey(Board,db_index=True)
    course = models.ForeignKey(Course,db_index=True)
    title = models.CharField(max_length=400)
    #chapter = models.CharField(max_length=50)
    url = models.CharField(max_length=1024, null=True, blank=True)
    num_sessions = models.IntegerField(default=1)
    status = models.CharField(max_length=256,choices=(('Not Started', 'Not Started'),
            ('In Progress', 'In Progress'), ('Partially Complete', 'Partially Complete'),
            ('Complete','Complete'), ('Inactive', 'Inactive')), default="Not Started")
    priority = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title

class Attribute(models.Model):
    types = models.CharField(max_length=256,choices=(('TextBook', 'TextBook'), ('Lesson Plan', 'Lesson Plan'),
            ('Transliteration','Transliteration'),('Videos','Videos'), ('Pictures', 'Pictures'), 
            ('Activities', 'Activities'),('Worksheets','Worksheets'),('Assessments','Assessments'),
            ('PowerPoint','PowerPoint')))

    def __unicode__(self):
        return self.types


class TopicDetails(models.Model):
    topic = models.ForeignKey(Topic,db_index=True)
    attribute = models.ForeignKey(Attribute,db_index=True)
    url = models.CharField(max_length=1024, null=True, blank=True)
    types = models.CharField(max_length=1024, null=True, blank=True)
    status = models.CharField(max_length=256,choices=(('Not Started', 'Not Started'), ('Assigned', 'Assigned'),
            ('In Progress','In Progress'),('Draft','Draft'), ('In Review', 'In Review'), 
            ('Published', 'Published'), ('Inactive', 'Inactive')), default="Not Started")
    author = models.ForeignKey(User, null=True, related_name="topic_details_author", blank=True)
    last_updated_date = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name="topic_details_updated_by", blank=True)
    drafturl = models.CharField(max_length=2560, null=True, blank=True)


class SubTopics(models.Model):
    name = models.CharField(max_length=400,null=True, blank=True)
    topic = models.ForeignKey(Topic,null=True,related_name='topic')
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50,default="Not Started")
    type = models.CharField(max_length=50, choices=(('1', 'Subchapter'), ('2', 'quiz')),default=1)
    author_id = models.ForeignKey(User, null=True, related_name="subtopics_author_id", blank=True)
    created_by = models.ForeignKey(User, null=True, related_name="subtopics_created_by", blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name="subtopics_updated_by", blank=True)
    reviewer = models.ForeignKey(User, null=True, related_name="subtopics_reviewer_id", blank=True)
    def __unicode__(self):
        return self.name


class ContentHostMaster(models.Model):
    name = models.CharField(max_length=256, null=True, blank=False)
    code = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, choices=(('active', 'Active'), ('inactive', 'Inactive')), default="active")
    created_by = models.ForeignKey(User, null=True, related_name='chm_created', blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='chm_updated', blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name = ('Content Host Master')

    def __unicode__(self):
        return self.name


class ContentTypeMaster(models.Model):
    name = models.CharField(max_length=256, null=True, blank=False)
    code = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, choices=(('active', 'Active'), ('inactive', 'Inactive')), default="active")
    created_by = models.ForeignKey(User, null=True, related_name='ctm_created', blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='ctm_updated', blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    format = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = ('Content Type Master')

    def __unicode__(self):
        return self.name


class WorkStreamType(models.Model):
    name = models.CharField(max_length=256, null=True, blank=False)
    code = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, choices=(('active', 'Active'), ('inactive', 'Inactive')), default="active")
    created_by = models.ForeignKey(User, null=True, related_name='wst_created', blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='wst_updated', blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name = ('Workstream Type')

    def __unicode__(self):
        return self.name


class ContentAuthor(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    user = models.ForeignKey(User, null=True, related_name="ca_author", blank=True)
    status = models.CharField(max_length=50, choices=(('active', 'Active'), ('inactive', 'Inactive')), default="active")
    created_by = models.ForeignKey(User, null=True, related_name='car_created', blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='car_updated', blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = ('Content Author')

    def __unicode__(self):
        return self.name


class ContentDetail(models.Model):
    topic = models.ForeignKey(Topic, null=True, related_name='cd_topic_id')
    subtopic = models.ForeignKey(SubTopics,null=True,related_name="cd_sub_topic_id")
    name = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=2048, null=True, blank=True)
    url_host = models.ForeignKey(ContentHostMaster, null=True, related_name="cd_host_master_id")
    content_type = models.ForeignKey(ContentTypeMaster,null=True,related_name="cd_content_type_id")
    workstream_type = models.ForeignKey(WorkStreamType, null=True, related_name="cd_workstream_type_id")
    author = models.ForeignKey(ContentAuthor, null=True, related_name="cd_content_author_id")
    status = models.CharField(max_length=50, choices=(('approved', 'Approved'),('unapproved', 'Unapproved'), ('inactive', 'Inactive')), default="unapproved")
    priority = models.IntegerField(default=1)
    version = models.IntegerField(default=1)
    duration = models.IntegerField(default=0)
    is_primary = models.BooleanField()
    created_by = models.ForeignKey(User, null=True, related_name='cd_created', blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='cd_updated', blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = ('Content Detail')

    def __unicode__(self):
        return self.name


class ContentMetaAttributeType(models.Model):
    name = models.CharField(max_length=256, null=True, blank=False)
    code = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, choices=(('active', 'Active'), ('inactive', 'Inactive')), default="active")
    workstream_type = models.ForeignKey(WorkStreamType,null=True,related_name="mat_workstream_type")
    created_by = models.ForeignKey(User, null=True, related_name='mat_created', blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='mat_updated', blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = ('Meta Attribute Type')

    def __unicode__(self):
        return self.name


class ContentMetaAttribute(models.Model):
    key = models.CharField(max_length=256, null=True, blank=False)
    value = models.CharField(max_length=500, null=True, blank=False)
    status = models.BooleanField(default=True)
    content_detail = models.ForeignKey(ContentDetail,null=True,related_name="cma_content_detail_d")
    meta_attribute_type = models.ForeignKey(ContentMetaAttributeType, null=True, related_name="cma_meta_attribute_id")
    created_by = models.ForeignKey(User, null=True, related_name='cma_created', blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='cma_updated', blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = ('Content Meta Attribute')

    def __unicode__(self):
        return self.key

class BaseModel(models.Model):
    # Define common fields and methods for your base model here
    # For example:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class FLTeacher_Content_View_Status(BaseModel):
    content_detail = models.ForeignKey(ContentDetail, null=True, blank=True, related_name='fsvs_content_id')
    status = models.CharField(max_length=50, choices=(('1', 'Viewed'), ('2', 'Pending'), ('3', 'Inprogress')),default="1")
    progress = models.IntegerField(default=0)
    number_of_times_viewed = models.IntegerField(default=1)
    user = models.ForeignKey(User, null=True, related_name='fsvs_auth_user', blank=True)
    topic = models.ForeignKey(Topic, null=True, blank=True, related_name="fsvs_topic")
    subtopic = models.ForeignKey(SubTopics, null=True, blank=True, related_name="fsvs_sub_topic")

