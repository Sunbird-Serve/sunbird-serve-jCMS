from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import json
import traceback
import requests
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.db.models import Q, F
from django.core.urlresolvers import reverse
from cms.models import *
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from datetime import timedelta
from django.shortcuts import render as render_response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
import random
import string
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder 
from datetime import datetime
from django.contrib.auth import logout as auth_logout

# User register
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'register.html')

# User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home/view_course')
    
    return render(request, 'login.html')


# Get all courses
def get_courses(request):
    board_id = request.GET.get("board_id")
    courses = Course.objects.filter(board_id=board_id, status='active' )
    course_data = [{"id": course.id, "name": course.subject.subject_name, "board": course.board.board_name, "grade": course.grade} for course in courses]
    response_data = json.dumps(course_data)
    return HttpResponse(response_data, content_type="application/json")

# Get all topics
def get_topics(request):
    course_id = request.GET.get("course_id")
    topics = Topic.objects.filter(course_id=course_id).exclude(status='Inactive')
    topic_data = [{"id": topic.id, "name": topic.title} for topic in topics]
    response_data = json.dumps(topic_data)
    return HttpResponse(response_data, content_type="application/json")

# Get all topics
def get_subTopics(request):
    topic_id = request.GET.get("topic_id")
    subTopics = SubTopics.objects.filter(topic_id=topic_id).exclude(status='Inactive')
    subTopic_data = [{"id": subTopic.id, "name": subTopic.name} for subTopic in subTopics]
    response_data = json.dumps(subTopic_data)
    return HttpResponse(response_data, content_type="application/json")



    if search_input:
        # Filter courses based on both subject name and grade
        filtered_courses = Course.objects.filter(
            Q(grade__icontains=search_input) | Q(subject__subject_name__icontains=search_input) | Q(board__board_name__icontains=search_input)
        )
    course_data = [{"id": course.id, "subject": course.subject.subject_name, "board": course.board.board_name, "grade": course.grade} for course in filtered_courses]
    response_data = json.dumps(course_data)
    return HttpResponse(response_data, content_type="application/json")



# View all course data
@login_required
def view_course(request):
    selected_board = request.GET.get('boardId')
    selected_subjectId = request.GET.get('subjectId')
    search_input = request.GET.get('searchInput')

    get_all_board = Board.objects.all()
    get_all_subject = Subject.objects.all()
    # Number of items per page
    items_per_page = 12

    set_filters = Q(status='active')

    if selected_board:
        if selected_board == 'all':
            set_filters &= Q(status='active')
        else:
            set_filters &= Q(board_id=selected_board)

    if selected_subjectId:
        if selected_subjectId == 'all':
            set_filters &= Q(status='active')
        else:
            set_filters &= Q(subject_id=selected_subjectId)

    if search_input:
        # Filter courses based on both subject name and grade
        set_filters = (
            Q(grade__icontains=search_input) | Q(subject__subject_name__icontains=search_input) | Q(board__board_name__icontains=search_input)
        )
    queryset = Course.objects.filter(set_filters)

    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')

    if page_number:
        page_number = int(page_number)  
    else:
        page_number = 1  # Default to first page
    
    courses = paginator.page(page_number)

    return render(request, 'course_view.html', {
        'get_all_board': get_all_board,
        'get_all_subject': get_all_subject,
        'courses': courses,
        'selected_board': selected_board,  # Pass selected_board to the template
        'selected_subjectId': selected_subjectId,  # Pass selected_subjectId to the template
        'search_input':search_input,
    })

# Get content data
def view_content(request):
    course_id = request.GET.get('courseID')
    target_url = '/home/content_detail/?courseID={}'.format(course_id)
    return HttpResponseRedirect(target_url)

# View content details
def content_detail_view(request):
    course_id = request.GET.get('courseID')
    courseData = Course.objects.get(id=course_id)
    boardName = Board.objects.get(id=courseData.board_id)
    subjectName = Subject.objects.get(id=courseData.subject_id)

    topics = Topic.objects.filter(course_id=course_id).exclude(status='Inactive')

    firstTopic = Topic.objects.filter(course_id=course_id).exclude(status='Inactive')[:1]

    if firstTopic:
        topic_data = [{"id": topic.id, "name": topic.title} for topic in topics]
        response_data = json.dumps(topic_data)
        try:
            topic_id = firstTopic[0].id

            subtopics = SubTopics.objects.filter(topic_id=topic_id).exclude(status='Inactive')

            subtopic_data = [{
                'topic_id': subtopic.topic.id,
                'topic_names': subtopic.topic.title, 
                'subtopic_ids': subtopic.id,
                'subtopic_names': subtopic.name,
                'subtopic_statuses': subtopic.status
            } for subtopic in subtopics]

            subtopic_all_data = json.dumps(subtopic_data)
            

            # Create a dictionary with all the data you want to send to the template
            context_data = {
                'topic_data_json': response_data,
                'subtopic_all_data':subtopic_all_data,
                'board_name': boardName,
                'subject_name': subjectName,
                'grade': courseData.grade
            }
            return render(request, 'content_view.html', context_data)

        except SubTopics.DoesNotExist:
            return render(request, 'content_view.html', {
                'topic_data_json': response_data,
                'board_name': boardName,
                'subject_name': subjectName,
                'grade': courseData.grade,
            })
    else:
        return render(request, 'error.html', {
            'message': 'The requested Topic does not exist.'
        })

#Get sub-Topic details
def getSubtopic(request):
    topicId = request.GET.get('topicId')
    
    # Fetch SubTopics based on the given topicId
    subtopics = SubTopics.objects.filter(topic_id=topicId).exclude(status='Inactive')
    
    subTopicData = []
    
    # Iterate through each subtopic
    for subtopic in subtopics:
        subtopic_data = {
            "id": subtopic.id,
            "name": subtopic.name,
            "status": subtopic.status,
            "topic_name": subtopic.topic.title,
            "content_details": []
        }
        
        # Fetch ContentDetail entries related to the current subtopic
        content_details = ContentDetail.objects.filter(subtopic_id=subtopic.id).exclude(status='Inactive')
        
        # Iterate through each content detail related to the current subtopic
        for content_detail in content_details:
            content_detail_data = {
                # "name": content_detail.name,
                "url": content_detail.url,
                "status": content_detail.status
            }
            subtopic_data["content_details"].append(content_detail_data)
        
        subTopicData.append(subtopic_data)
    
    response_data = json.dumps(subTopicData)
    return HttpResponse(response_data, content_type="application/json")

  
class SubTopicDetailsView(View):
    ''''GET: rtc player'''
    # def getChildRecord(self,contentId):
    #     try:
    #         url = "https://api.dev.diksha.gov.in/api/content/v1/read/"+contentId
    #         authDict = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBOGt5dGptMDdXN2tJOGxNY0c3Unljc3I2b1Q2NWhoViJ9.OMhRtUiochad7pMiozTVY9lOUC9kG3Us7NnA-lezVoc"}

    #         url = str(url)
    #         response = requests.get(url,headers=authDict)
    #         respDict = response.json()
    #         responseCode = respDict.get("responseCode")
    #         contentList = []

    #         if responseCode == "OK":
    #             result = respDict.get("result")
    #             contentObj = result.get("content")
    #             if contentObj:
    #                 name = contentObj.get("name")
    #                 mimeType = contentObj.get("mimeType")
    #                 artifactUrl = contentObj.get("artifactUrl")
    #                 if (mimeType == "video/mp4" or mimeType == "application/pdf") and artifactUrl:
    #                     mimtype = "worksheet"
    #                     if mimeType == "video/mp4":
    #                         mimtype = "video"

    #                     ctObj = {
    #                         "id":contentId,
    #                         "name":name,
    #                         "url":artifactUrl,
    #                         "mimeType":mimtype

    #                     }
    #                     contentList.append(ctObj)


    #         #print("contentList",contentList)
    #         return contentList
    #     except Exception as e:
    #         print("getChildRecord ",e)
    #         traceback.print_exc()
    #         return None

    # def getChildNodeDetails(self,leafNodes):
    #     try:
    #         childList = []
    #         for contentId in leafNodes:
    #             #print("contentId",contentId)
    #             newList = self.getChildRecord(contentId)
    #             if newList and len(newList) > 0:
    #                 childList.extend(newList)
    #         #print("childList",childList)
    #         return childList
    #     except Exception as e:
    #         print("getChildNodeDetails ",e)
    #         traceback.print_exc()
    #         return None

    # def getChildRecord(self, contentId):
    #     try:
    #         url = "https://api.dev.diksha.gov.in/api/content/v1/read/" + contentId
    #         authDict = {
    #             "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBOGt5dGptMDdXN2tJOGxNY0c3Unljc3I2b1Q2NWhoViJ9.OMhRtUiochad7pMiozTVY9lOUC9kG3Us7NnA-lezVoc"}

    #         url = str(url)
    #         response = requests.get(url, headers=authDict)
    #         respDict = response.json()
    #         responseCode = respDict.get("responseCode")
    #         contentList = []

    #         if responseCode == "OK":
    #             result = respDict.get("result")
    #             contentObj = result.get("content")
    #             if contentObj:
    #                 name = contentObj.get("name")
    #                 mimeType = contentObj.get("mimeType")
    #                 artifactUrl = contentObj.get("artifactUrl")
    #                 if (mimeType == "video/mp4" or mimeType == "application/pdf") and artifactUrl:
    #                     mimtype = "worksheet"
    #                     if mimeType == "video/mp4":
    #                         mimtype = "video"

    #                     ctObj = {
    #                         "id": contentId,
    #                         "name": name,
    #                         "url": artifactUrl,
    #                         "mimeType": mimtype

    #                     }
    #                     contentList.append(ctObj)
    #         return contentList
    #     except Exception as e:
    #         traceback.print_exc()
    #         return None

    # def getChildNodeDetails(self, leafNodes):
    #     try:
    #         childList = []
    #         for contentId in leafNodes:
    #             newList = self.getChildRecord(contentId)
    #             if newList and len(newList) > 0:
    #                 childList.extend(newList)
    #         return childList
    #     except Exception as e:
    #         traceback.print_exc()
    #         return None

    # def getContentFromThirdParty(self):
    #     try:
    #         url = "https://api.dev.diksha.gov.in/api/content/v1/search"
    #         payloadData = {
    #             "request": {

    #                 "filters": {
    #                     "primaryCategory": [
    #                         "Digital Textbook"
    #                     ],
    #                     "se_boards": [
    #                         "CBSE"
    #                     ],
    #                     "se_mediums": [
    #                         "English"
    #                     ],
    #                     "se_gradeLevels": [
    #                         "Class 7"
    #                     ]
    #                 },
    #                 "limit": 1000,
    #                 "fields": [
    #                     "string",
    #                     "name",
    #                     "contentType",
    #                     "leafNodes"

    #                 ]
    #             }
    #         }


    #         authDict = {
    #             "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBOGt5dGptMDdXN2tJOGxNY0c3Unljc3I2b1Q2NWhoViJ9.OMhRtUiochad7pMiozTVY9lOUC9kG3Us7NnA-lezVoc"}
    #         response = requests.post(url, json=payloadData, headers=authDict)
    #         print(response)
    #         respDict = response.json()
    #         responseCode = respDict.get("responseCode")
    #         contentList = []
    #         videoList = []
    #         if responseCode == "OK":
    #             result = respDict.get("result")
    #             contentObjs = result.get("content")
    #             for each in contentObjs:
    #                 eachId = each.get("identifier")
    #                 contentType = each.get("contentType")


    #                 leafNodes = each.get("leafNodes")
    #                 if leafNodes and len(leafNodes) > 0:
    #                     pass
    #                 tlist = self.getChildNodeDetails(leafNodes)
    #                 if tlist and len(tlist) > 0:
    #                     for newObj in tlist:
    #                         cType = newObj.get("mimeType")
    #                         eachDict = {
    #                             "id": 3788,
    #                             "did": newObj.get("id"),
    #                             "title": newObj.get("name"),
    #                             "contentType": newObj.get("mimeType"),
    #                             "url": newObj.get("url"),
    #                             "author": "Diksha",
    #                             "duration": 960,
    #                             "isPrimary": True,
    #                             "contentHost": "s3",
    #                             "description": ''

    #                         }
    #                         if cType != "video":
    #                             contentList.append(eachDict)
    #                         else:
    #                             videoList.append(eachDict)



    #                 else:
    #                     eachDict = {
    #                         "id": 3788,
    #                         "did": eachId,
    #                         "title": each.get("name"),
    #                         "contentType": contentType,
    #                         "objectType": each.get("objectType"),
    #                         "url": "https://dev.diksha.gov.in/play/collection/" + eachId + "?contentType=" + contentType
    #                     }

    #                     contentList.append(eachDict)


    #             return (contentList, videoList)
    #         else:
    #             return ([], [])


    #     except Exception as e:
    #         traceback.print_exc()
    #         return (None, None)



    # Get video content
    def get(self, request,  *args, **kwargs):
        try:

            subtopicId = self.request.GET.get('subtopic_id', None)
            topicId = self.request.GET.get('topic_id', None)

            topicObj = Topic.objects.get(id=topicId)

            try:
                subtopicObj = SubTopics.objects.get(id=subtopicId)
                topicObj = subtopicObj.topic
            except:
                return HttpResponseNotFound("SubTopics Not found")

            contentRecords = ContentDetail.objects.filter(status="approved", subtopic=subtopicObj).exclude(status='Inactive').select_related(
                'workstream_type', 'content_type', 'url_host').order_by('priority')


            contentDetailData = {
                'subtopic_id': subtopicId,
                'subtopic_name': subtopicObj.name,
                'subject': topicObj.course.subject.subject_name,
                'grade': topicObj.course.grade,
                'board': topicObj.course.board.board_name,
                'courseId':topicObj.course_id,
                'topicId':topicId
            }
            for i in range(len(contentRecords)):
                contentRec = contentRecords[i]
                workStreamType = contentRec.workstream_type
                contentTypeRec = contentRec.content_type
                contentHostRec = contentRec.url_host

                if not contentTypeRec or not contentHostRec or not workStreamType: continue
                # logService.logInfo("workStreamType code", workStreamType.code)
                dataRecArr = contentDetailData.get(workStreamType.code)
                if dataRecArr is None:
                    dataRecArr = []
                    contentDetailData[workStreamType.code] = dataRecArr

                contentDict = {"id": contentRec.id,
                               "title": contentRec.name,
                               "description": contentRec.description,
                               "author": "eVidyaloka",
                               "duration": contentRec.duration,
                               "url": contentRec.url,
                               "isPrimary": contentRec.is_primary,
                               "contentType": contentTypeRec.code,
                               "contentHost": contentHostRec.code
                               }
                dataRecArr.append(contentDict)

            context = contentDetailData


            # videoList= []
            # videoList.append(contentRec.url)
            # cList = len(videoList)
            # print(video_list_length)

            # cList, videoList = self.getContentFromThirdParty()

            # if cList and len(cList) > 0:
            #     context['tpContentList'] = cList
            #     context['showTpContent'] = 1
            # else:
            #     context['showTpContent'] = 0

            # if videoList and len(videoList) > 0:
            #     evdList = context['video']
            #     if evdList and len(evdList) > 0:
            #         evdList.extend(videoList)

            # response_data = json.dumps(context)
            # print((response_data))
            # return render(self.request, 'flm_content_details.html', {'contentDetails': response_data})

            return render_response(self.request, 'flm_content_details.html', context)
        except  Exception  as e:
            return HttpResponseNotFound("Page not found " + e.message)


    # View Video and Worksheet Rating page 
    def post(self, request,  *args, **kwargs):
        requestParams = json.loads(self.request.body)
        try:
            today = datetime.datetime.now()
            min_dt = datetime.datetime.combine(today, today.time().min)
            max_dt = datetime.datetime.combine(today, today.time().max)
            existing_rating = Flm_Content_Rating.objects.filter(reviewer=self.request.user, subtopic_id=int(requestParams['subtopicId']), updated_on__range=(min_dt, max_dt))
            if len(existing_rating) >0:
                rate = existing_rating[0]
                rate.videoRating=float(requestParams['videoRating'])
                rate.worksheetRating=float(requestParams['worksheetRating'])
                rate.comment=str(requestParams['comment'])
                rate.save()
            else:
                rate = Flm_Content_Rating.objects.create(reviewer=self.request.user, subtopic_id=int(requestParams['subtopicId']), videoRating=float(requestParams['videoRating']), worksheetRating=float(requestParams['worksheetRating']), comment=str(requestParams['comment']))
            return genUtility.getSuccessApiResponse(request, {'message': 'Rating saved successfully', 'id':rate.id})
        except Exception as e:
            traceback.print_exc()
            return genUtility.getStandardErrorResponse(request, 'kInvalidRequest')

# Save content
def content_rating(request):
    if request.method == 'POST':
        topicId = request.POST.get('topicId')
        subtopicId = request.POST.get('subtopicId')
        videoRating = request.POST.get('videoRating')
        worksheetRating = request.POST.get('worksheetRating')
        comment = request.POST.get('comment')
        current_time = timezone.now()

        ratingExist = FLMContentRating.objects.filter(subtopic_id=subtopicId)
        # Get the row count
        row_count = ratingExist.count()

        if row_count == 0:
            # If no matching records found, create a new record
            content_rating = FLMContentRating(
                subtopic_id=subtopicId,
                videoRating=videoRating,
                worksheetRating=worksheetRating,
                comment=comment,
                status='active',
                reviewer_id='0',
                created_by_id = request.user.id,
                created_on = current_time
            )
            content_rating.save()
            course_data = {
                "status": "success",
                "message": "Rating saved successfully",
            }
        else:
            # If matching records found, update the first one (you might want to specify the update logic)

            existing_rating = ratingExist[0]
            existing_rating.videoRating = videoRating
            existing_rating.worksheetRating = worksheetRating
            existing_rating.comment = comment
            existing_rating.updated_by_id = request.user.id
            existing_rating.updated_on=current_time
            existing_rating.save()
            course_data = {
                "status": "success",
                "message": "Rating updated successfully",
            }

        # Return 'course_data' as needed for your application response
        response_data = json.dumps(course_data)
        return HttpResponse(response_data, content_type="application/json")




@csrf_exempt
def create_or_edit_board(request):

        data = json.loads(request.body)
        name = data.get('board_name')
        board_id = data.get('id')

        if name:
            if board_id:
                if request.method == 'PUT':
                    try:
                        board = Board.objects.get(id=board_id)
                        board.board_name = name
                        board.save()
                        return HttpResponse(json.dumps({"message": 'Board Name updated successfully'}), status=200)
                    except Board.DoesNotExist:
                        return HttpResponse(json.dumps({'message': 'Board not found'}), status=404)
                else :
                    return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)
            else:
                if request.method == 'POST':
                    board = Board(board_name=name)
                    board.save()
                    return HttpResponse(json.dumps({"message": 'Board created successfully'}), status=200)
                else :
                    return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)
        else:
            return HttpResponse(json.dumps({'message': 'Board Name is required'}), status=400)




@csrf_exempt
def create_or_edit_subject(request):

        data = json.loads(request.body)
        name = data.get('subject_name')
        subject_id = data.get('id')

        if name:
            if subject_id:
                if request.method == 'PUT':
                    try:
                        subject = Subject.objects.get(id=subject_id)
                        subject.subject_name = name
                        subject.save()
                        return HttpResponse(json.dumps({"message": 'Subject Name updated successfully'}), status=200)
                    except Subject.DoesNotExist:
                        return HttpResponse(json.dumps({'message': 'Subject not found'}), status=404)
                else :
                    return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)
            else:
                if request.method == 'POST':
                    subject = Subject(subject_name=name)
                    subject.save()
                    return HttpResponse(json.dumps({"message": 'Subject created successfully'}), status=200)
                else :
                    return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)
        else:
            return HttpResponse(json.dumps({'message': 'Subject Name is required'}), status=400)


@csrf_exempt
def create_or_edit_course(request):

    data = json.loads(request.body)
    board_id= data.get('board_id')
    subject_id = data.get('subject_id')
    grade = data.get('grade')
    type = data.get('type')
    description = data.get('description')
    picture = data.get('picture')
    status = data.get('status')
    language_id = data.get('language_id')
    availabilityType = data.get('availabilityType')
    course_id = data.get('id')

    if board_id and subject_id and grade:
        if request.method == 'POST':
            course = Course(board_id=board_id,subject_id=subject_id,grade=grade,type=type,description=description,picture=picture,status=status,language_id=language_id,availabilityType=availabilityType)  
            course.save()
            return HttpResponse(json.dumps({"message": 'Course created successfully'}), status=404)
        else:
            return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)

    if course_id:
        if request.method == 'PUT':
            try:
                course = Course.objects.get(id=course_id)
                fields_to_update = {
                    'board_id': board_id,
                    'subject_id': subject_id,
                    'grade': grade,
                    'type': type,
                    'description': description,
                    'picture': picture,
                    'status': status,
                    'language_id': language_id,
                    'availabilityType': availabilityType,
                }

                # Update the fields with non-empty values
                for field_name, field_value in fields_to_update.items():
                    if field_value is not None:
                        setattr(course, field_name, field_value)

                course.save()

                return HttpResponse(json.dumps({"message": 'Course updated successfully'}), status=200)
            except Board.DoesNotExist:
                return HttpResponse(json.dumps({'message': 'Course not found'}), status=404)
        else:
            return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)

@csrf_exempt
def create_or_edit_topic(request):

    data = json.loads(request.body)
    course_id = data.get('course_id')
    title = data.get('title')
    url = data.get('url')
    num_sessions = data.get('num_sessions')
    status = data.get('status')
    priority = data.get('priority')
    topic_id = data.get('id')

    if course_id and title:
        if request.method == 'POST':
            topic = Topic(course_id=course_id,title=title,url=url,num_sessions=num_sessions,status=status,priority=priority ) 
            topic.save()
            response_data = {
                "message": 'Topic created successfully!',
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)

    if topic_id:
        if request.method == 'PUT':
            try:
                topic = Topic.objects.get(id=topic_id)
                fields_to_update = {
                    'course_id': course_id,
                    'title': title,
                    'url': url,
                    'num_sessions': num_sessions,
                    'status': status,
                    'priority': priority,
                }

                # Update the fields with non-empty values
                for field_name, field_value in fields_to_update.items():
                    if field_value is not None:
                        setattr(topic, field_name, field_value)

                topic.save()

                return HttpResponse(json.dumps({"message": 'Topic updated successfully'}), content_type='application/json')
            except Board.DoesNotExist:
                return HttpResponse(json.dumps({'message': 'Topic not found'}), status=404)
        else:
            return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405, content_type='application/json')

@csrf_exempt
def create_or_edit_subtopic(request):
    data = json.loads(request.body)
    name = data.get('name')
    topic_id = data.get('topic_id')
    status = data.get('status')
    type = data.get('type')
    author_id = data.get('author_id')
    created_by_id = data.get('created_by_id')
    updated_by_id = data.get('updated_by_id')
    subTopic_id = data.get('id')

    if name and topic_id :
        if request.method == 'POST':
            subtopic = SubTopics(name=name,topic_id=topic_id,status=status,type=type,author_id=author_id,created_by_id=created_by_id,updated_by_id=updated_by_id ) 
            subtopic.save()

            response_data = {
                "message": 'Sub-Topic created successfully',
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)
    if subTopic_id:
        if request.method == 'PUT':
            try:
                subtopic = SubTopics.objects.get(id=subTopic_id)
                fields_to_update = {
                    'name': name,
                    'topic_id': topic_id,
                    'status': status,
                    'type': type,
                    'status': status,
                    'author_id': author_id,
                    'created_by_id': created_by_id,
                    'updated_by_id': updated_by_id,
                    'subTopic_id': subTopic_id,
                }

                # Update the fields with non-empty values
                for field_name, field_value in fields_to_update.items():
                    if field_value is not None:
                        setattr(subtopic, field_name, field_value)

                subtopic.save()

                return HttpResponse(json.dumps({"message": 'Sub-Topic updated successfully'}), content_type='application/json')
            except Board.DoesNotExist:
                return HttpResponse(json.dumps({'message': 'Sub-Topic not found'}), status=404)
        else:
            return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)

@csrf_exempt
def create_or_edit_content(request):
    data = json.loads(request.body)
    name = data.get('name')
    topic_id = data.get('topic_id')
    subTopic_id = data.get('subTopic_id')
    description = data.get('description')
    url = data.get('url')
    url_host_id = data.get('url_host_id')
    content_type_id = data.get('content_type_id')
    workstream_type_id = data.get('workstream_type_id')
    author_id = data.get('author_id')
    status = data.get('status')
    version = data.get('version')
    duration = data.get('duration')
    is_primary = data.get('is_primary')
    created_by_id = data.get('created_by_id')
    created_on = data.get('created_on')
    updated_by_id = data.get('updated_by_id')
    updated_on = data.get('updated_on')
    contentDetails_id = data.get('id')


    if name and topic_id and subTopic_id:
        if request.method == 'POST':
            contentDetail = ContentDetail(name=name,topic_id=topic_id,subtopic_id=subTopic_id,description=description,url=url,url_host_id=url_host_id,content_type_id=content_type_id,workstream_type_id=workstream_type_id,author_id=author_id,status=status,version=version,duration=duration,is_primary=is_primary,created_by_id=created_by_id,created_on=created_on,updated_by_id=updated_by_id,updated_on=updated_on) 
            contentDetail.save()

            response_data = {
                "message": 'Content Detail added successfully',
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)
    if contentDetails_id:
        if request.method == 'PUT':
            try:
                contentDetail = ContentDetail.objects.get(id=contentDetails_id)
                fields_to_update = {
                    'name': name,
                    'topic_id': topic_id,
                    'subTopic_id': subTopic_id,
                    'description': description,
                    'url': url,
                    'url_host_id': url_host_id,
                    'content_type_id': content_type_id,
                    'workstream_type_id': workstream_type_id,
                    'author_id': author_id,
                    'status': status,
                    'version': version,
                    'duration': duration,
                    'is_primary': is_primary,
                    'created_by_id': created_by_id,
                    'created_on': created_on,
                    'updated_by_id': updated_by_id,
                    'updated_on': updated_on
                }

                # Update the fields with non-empty values
                for field_name, field_value in fields_to_update.items():
                    if field_value is not None:
                        setattr(contentDetail, field_name, field_value)

                contentDetail.save()

                return HttpResponse(json.dumps({"message": 'Content Detail updated successfully'}), content_type='application/json')
            except Board.DoesNotExist:
                return HttpResponse(json.dumps({'message': 'Content Detail not found'}), status=404)
        else:
            return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)



@csrf_exempt
def get_board(request):
    if request.method == 'GET':
        if request.body :
            data = json.loads(request.body)
            board_id = data.get('id')
            board_name = data.get('board_name')

            if board_id:
                boards = Board.objects.filter(id=board_id)
                
            if board_name:
                boards = Board.objects.filter(board_name=board_name)

        else :
            boards = Board.objects.values('id', 'board_name')

        board_data = list(boards.values('id', 'board_name'))

        response_data = {
            'board_details': board_data,
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)



@csrf_exempt
def get_subject(request):
    if request.method == 'GET':
        if request.body :
            data = json.loads(request.body)
            subject_id = data.get('id')
            subject_name = data.get('subject_name')

            if subject_id:
                subjects = Subject.objects.filter(id=subject_id)
                
            if subject_name:
                subjects = Subject.objects.filter(subject_name=subject_name)

        else :
            subjects = Subject.objects.values('id', 'subject_name')

        subject_data = list(subjects.values('id', 'subject_name'))

        response_data = {
            'subject_details': subject_data,
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)


@csrf_exempt
def get_course(request):
    if request.method == 'GET':
        if request.body :
            data = json.loads(request.body)
            filters = {}
            course_id = data.get('id')
            board_id = data.get('board_id')
            subject_id = data.get('subject_id')
            grade = data.get('grade')
            status = data.get('status')


            if course_id:
                filters['id'] = course_id

            if board_id:
                filters['board_id'] = board_id

            if subject_id:
                filters['subject_id'] = subject_id

            if grade:
                filters['grade'] = grade

            if status:
                filters['status'] = status

            course_list = Course.objects.filter(**filters) 

        else:
            course_list = Course.objects.all()

        course_data = list(course_list.values('id', 'board_id', 'subject_id', 'grade', 'type', 'description', 'picture', 'status', 'language_id', 'availabilityType'))

        response_data = {
            'course_details': course_data,
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)        


@csrf_exempt
def get_topic(request):
    if request.method == 'GET':
        if request.body :
            data = json.loads(request.body)
            filters = {}
            topic_id = data.get('id')
            course_id = data.get('course_id')
            title = data.get('title')
            status = data.get('status')

            if topic_id:
                filters['id'] = topic_id
            if course_id:
                filters['course_id'] = course_id
            if title:
                filters['title'] = title
            if status:
                filters['status'] = status

            topic_list = Topic.objects.filter(**filters)  

        else:
            topic_list = Topic.objects.all()

        topic_data = list(topic_list.values('id', 'course_id', 'title', 'url', 'num_sessions', 'status', 'priority'))

        response_data = {
            'topic_details': topic_data,
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)

@csrf_exempt
def get_subtopic(request):
    if request.method == 'GET':
        if request.body :
            data = json.loads(request.body)
            filters = {}
            subtopic_id = data.get('id')
            topic_id = data.get('topic_id')
            name = data.get('name')
            status = data.get('status')

            if subtopic_id:
                filters['id'] = subtopic_id
            if name:
                filters['name'] = name
            if topic_id:
                filters['topic_id'] = topic_id
            if status:
                filters['status'] = status

            contentDetails_list = ContentDetail.objects.filter(**filters)
        else:
            subTopic_list = SubTopics.objects.all()

        subtopic_data = json.dumps(list(contentDetails_list.values('id','name','topic_id','created_date','updated_date','status','type','author_id','created_by_id','updated_by_id','reviewer_id')), cls=DjangoJSONEncoder)
        
        response_data = {
            'topic_details': subtopic_data,
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)



@csrf_exempt
def get_content(request):
    if request.method == 'GET':
        if request.body :
            data = json.loads(request.body)
            filters = {}
            
            contentDetails_id=data.get('id')
            name=data.get('name')
            topic_id=data.get('topic_id')
            subTopic_id=data.get('subtopic_id')
            status=data.get('status')

            if contentDetails_id:
                filters['id'] = contentDetails_id
            if name:
                filters['name'] = name
            if topic_id:
                filters['topic_id'] = topic_id
            if subTopic_id:
                filters['subtopic_id'] = subTopic_id
            if status:
                filters['status'] = status

            contentDetails_list = ContentDetail.objects.filter(**filters)
        else:
            contentDetails_list = ContentDetail.objects.all()

        content_details = json.dumps(list(contentDetails_list.values('id', 'topic_id', 'subtopic_id', 'name', 'description', 'url', 'url_host_id', 'content_type_id', 'workstream_type_id', 'author_id', 'status', 'priority', 'version', 'duration', 'is_primary', 'created_by_id', 'created_on', 'updated_by_id', 'updated_on')), cls=DjangoJSONEncoder)

        response_data = {
            'content_details': content_details,
        }
        return HttpResponse(content_details, content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405)


@csrf_exempt
def delete_board(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        board_id = data.get('id')

        if board_id:
            board = Board(id=board_id)
            board.delete()
            response_data = {
                "message": 'Board deleted successfully',
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            response_data = {'message': 'Board Id is required'}
            return HttpResponse(json.dumps(response_data), status=400, content_type='application/json')
    else:
        response_data = {'message': 'Invalid request method'}
        return HttpResponse(json.dumps(response_data), status=405, content_type='application/json')



@csrf_exempt
def delete_subject(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        subject_id = data.get('id')

        if subject_id:
            subject = Subject(id=subject_id)
            subject.delete()
            response_data = {
                "message": 'Subject deleted successfully',
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            response_data = {'message': 'Subject Id is required'}
            return HttpResponse(json.dumps(response_data), status=400, content_type='application/json')
    else:
        response_data = {'message': 'Invalid request method'}
        return HttpResponse(json.dumps(response_data), status=405, content_type='application/json')


@csrf_exempt
def delete_course(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        course_id = data.get('id')

        if course_id:
            course = Course(id=course_id)
            course.delete()
            response_data = {
                "message": 'Course deleted successfully',
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            response_data = {'message': 'Course Id is required'}
            return HttpResponse(json.dumps(response_data), status=400, content_type='application/json')
    else:
        response_data = {'message': 'Invalid request method'}
        return HttpResponse(json.dumps(response_data), status=405, content_type='application/json')



@csrf_exempt
def delete_topic(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        topic_id = data.get('id')

        if topic_id:
            topic = Topic(id=topic_id)
            topic.delete()
            response_data = {
                "message": 'Topic deleted successfully',
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            response_data = {'message': 'Topic Id is required'}
            return HttpResponse(json.dumps(response_data), status=400, content_type='application/json')
    else:
        response_data = {'message': 'Invalid request method'}
        return HttpResponse(json.dumps(response_data), status=405, content_type='application/json')


@csrf_exempt
def delete_subTopic(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        subTopic_id = data.get('id')

        if subTopic_id:
            subtopic = SubTopics(id=subTopic_id)
            subtopic.delete()
            response_data = {
                "message": 'Sub-Topic deleted successfully',
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            response_data = {'message': 'Sub-Topic Id is required'}
            return HttpResponse(json.dumps(response_data), status=400, content_type='application/json')
    else:
        response_data = {'message': 'Invalid request method'}
        return HttpResponse(json.dumps(response_data), status=405, content_type='application/json')


@csrf_exempt
def delete_content(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        contentDetails_id = data.get('id')

        if contentDetails_id:
            contentDetails = ContentDetail(id=contentDetails_id)
            contentDetails.delete()
            response_data = {
                "message": 'Content Details deleted successfully',
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            response_data = {'message': 'Content Details Id is required'}
            return HttpResponse(json.dumps(response_data), status=400, content_type='application/json')
    else:
        response_data = {'message': 'Invalid request method'}
        return HttpResponse(json.dumps(response_data), status=405, content_type='application/json')

def custom_logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

def dashboard(request):
    return render(request, 'dashboard.html')

def all_course(request):
    selected_board = request.GET.get('boardId')
    selected_subjectId = request.GET.get('subjectId')
    search_input = request.GET.get('searchInput')

    get_all_board = Board.objects.all()
    get_all_subject = Subject.objects.all()
    # Number of items per page
    items_per_page = 12

    set_filters = Q(status='active')

    if selected_board:
        if selected_board == 'all':
            set_filters &= Q(status='active')
        else:
            set_filters &= Q(board_id=selected_board)

    if selected_subjectId:
        if selected_subjectId == 'all':
            set_filters &= Q(status='active')
        else:
            set_filters &= Q(subject_id=selected_subjectId)

    if search_input:
        # Filter courses based on both subject name and grade
        set_filters = (
            Q(grade__icontains=search_input) | Q(subject__subject_name__icontains=search_input) | Q(board__board_name__icontains=search_input)
        )
    queryset = Course.objects.filter(set_filters)

    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')

    if page_number:
        page_number = int(page_number)  
    else:
        page_number = 1  # Default to first page
    
    courses = paginator.page(page_number)

    return render(request, 'course_view_admin.html', {
        'get_all_board': get_all_board,
        'get_all_subject': get_all_subject,
        'courses': courses,
        'selected_board': selected_board,  # Pass selected_board to the template
        'selected_subjectId': selected_subjectId,  # Pass selected_subjectId to the template
        'search_input':search_input,
    })

def all_topic(request):
    selected_board = request.GET.get('boardId')
    selected_subjectId = request.GET.get('subjectId')
    selected_topicId = request.GET.get('topicId')
    search_input = request.GET.get('searchInput')

    get_all_board = Board.objects.all()
    get_all_subject = Subject.objects.all()
    get_all_topic = Topic.objects.all()
    # Number of items per page
    items_per_page = 12

    queryset = Topic.objects.all()

    if selected_board:
        queryset = queryset.filter(Q(course__board_id=selected_board))

    if selected_subjectId:
        queryset = queryset.filter(Q(course__subject_id=selected_subjectId))

    if selected_topicId:
        queryset = queryset.filter(Q(id=selected_topicId))

    if search_input:
        # Filter courses based on both subject name and grade
        queryset = queryset.filter(
            Q(course__grade__icontains=search_input) | Q(course__subject__subject_name__icontains=search_input) | Q(course__board__board_name__icontains=search_input) | Q (title__icontains=search_input)
        )

    # Exclude courses with a status of 'Inactive' from the final queryset
    queryset = queryset.exclude(status='Inactive')
        

    paginator = Paginator(queryset, items_per_page)

    page_number = request.GET.get('page')
   

    if page_number:
        page_number = int(page_number)  
    else:
        page_number = 1  # Default to first page
    print(page_number)
    topics = paginator.page(page_number)

    return render(request, 'topic_view_admin.html', {
        'get_all_board': get_all_board,
        'get_all_subject': get_all_subject,
        'topics': topics,
        'selected_board': selected_board,  
        'selected_subjectId': selected_subjectId,  
        'search_input':search_input,
        'get_all_topic':get_all_topic,
    })

def all_subtopic(request):
    selected_board = request.GET.get('boardId')
    selected_subjectId = request.GET.get('subjectId')
    selected_topicId = request.GET.get('topicId')
    search_input = request.GET.get('searchInput')

    get_all_board = Board.objects.all()
    get_all_subject = Subject.objects.all()
    get_all_topic = Topic.objects.all()
    # Number of items per page
    items_per_page = 12

    queryset = SubTopics.objects.all()

    if selected_board:
        queryset = queryset.filter(Q(topic__course__board_id=selected_board))

    if selected_subjectId:
        queryset = queryset.filter(Q(topic__course__subject_id=selected_subjectId))

    if selected_topicId:
        queryset = queryset.filter(Q(topic_id=selected_topicId))

    if search_input:
        # Filter courses based on both subject name and grade
        queryset = queryset.filter(
            Q(topic__course__grade__icontains=search_input) | Q(topic__course__subject__subject_name__icontains=search_input) | Q(topic__course__board__board_name__icontains=search_input) | Q (name__icontains=search_input)
        )

    # Exclude courses with a status of 'Inactive' from the final queryset
    queryset = queryset.exclude(status='Inactive')
        

    paginator = Paginator(queryset, items_per_page)

    page_number = request.GET.get('page')
   

    if page_number:
        page_number = int(page_number)  
    else:
        page_number = 1  # Default to first page
    print(page_number)
    subtopics = paginator.page(page_number)

    return render(request, 'subtopic_view_admin.html', {
        'get_all_board': get_all_board,
        'get_all_subject': get_all_subject,
        'subtopics': subtopics,
        'selected_board': selected_board,  
        'selected_subjectId': selected_subjectId,  
        'search_input':search_input,
        'get_all_topic':get_all_topic,
    })


def all_content(request):
    selected_board = request.GET.get('boardId')
    selected_subjectId = request.GET.get('subjectId')
    selected_topicId = request.GET.get('topicId')
    search_input = request.GET.get('searchInput')

    get_all_board = Board.objects.all()
    get_all_subject = Subject.objects.all()
    get_all_topic = Topic.objects.all()
    # Number of items per page
    items_per_page = 12

    queryset = ContentDetail.objects.all()

    if selected_board:
        queryset = queryset.filter(Q(topic__course__board_id=selected_board))

    if selected_subjectId:
        queryset = queryset.filter(Q(topic__course__subject_id=selected_subjectId))

    if selected_topicId:
        queryset = queryset.filter(Q(topic_id=selected_topicId))

    if search_input:
        # Filter courses based on both subject name and grade
        queryset = queryset.filter(
            Q(topic__title__icontains=search_input) | Q(topic__course__subject__subject_name__icontains=search_input) | Q(topic__course__board__board_name__icontains=search_input) | Q (name__icontains=search_input) | Q(subtopic__name__icontains=search_input)
        )

    # Exclude courses with a status of 'Inactive' from the final queryset
    queryset = queryset.exclude(status='Inactive')
        

    paginator = Paginator(queryset, items_per_page)

    page_number = request.GET.get('page')
   

    if page_number:
        page_number = int(page_number)  
    else:
        page_number = 1  # Default to first page
    print(page_number)
    contentDetails = paginator.page(page_number)

    return render(request, 'content_view_admin.html', {
        'get_all_board': get_all_board,
        'get_all_subject': get_all_subject,
        'contentDetails': contentDetails,
        'selected_board': selected_board,  
        'selected_subjectId': selected_subjectId,  
        'search_input':search_input,
        'get_all_topic':get_all_topic,
    })






