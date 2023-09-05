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
    courses = Course.objects.filter(board_id=board_id)
    course_data = [{"id": course.id, "name": course.subject.subject_name, "board": course.board.board_name, "grade": course.grade} for course in courses]
    response_data = json.dumps(course_data)
    return HttpResponse(response_data, content_type="application/json")

# Get all topics
def get_topics(request):
    course_id = request.GET.get("course_id")
    topics = Topic.objects.filter(course_id=course_id)
    topic_data = [{"id": topic.id, "name": topic.title} for topic in topics]
    response_data = json.dumps(topic_data)
    return HttpResponse(response_data, content_type="application/json")

# View all course data
def view_course(request):
    get_all_board = Board.objects.all()
    get_all_subject = Subject.objects.all()
    # Number of items per page
    items_per_page = 12 

    queryset = Course.objects.all()
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
    })


# Board wise data retrive 
def get_filtered_courses(request):
    selected_board = request.GET.get('boardId')
    if selected_board == 'all':
        courses = Course.objects.all()
        course_data = [{"id": course.id, "subject": course.subject.subject_name, "board": course.board.board_name, "grade": course.grade} for course in courses]
    else:
        courses = Course.objects.filter(board_id=selected_board)
        course_data = [{"id": course.id, "subject": course.subject.subject_name, "board": course.board.board_name, "grade": course.grade} for course in courses]
    response_data = json.dumps(course_data)
    return HttpResponse(response_data, content_type="application/json")


# Subject wise data retrive 
def get_filtered_subject(request): 
    selected_subject = request.GET.get('subjectId')
    if selected_subject == 'all':
        courses = Course.objects.all()
        course_data = [{"id": course.id, "subject": course.subject.subject_name, "board": course.board.board_name, "grade": course.grade} for course in courses]
    else:
        courses = Course.objects.filter(subject_id=selected_subject)
        course_data = [{"id": course.id, "subject": course.subject.subject_name, "board": course.board.board_name, "grade": course.grade} for course in courses]
    response_data = json.dumps(course_data)
    return HttpResponse(response_data, content_type="application/json")


# Search any course
def search_courses(request):
    search_input = request.GET.get('searchInput')

    # Initialize an empty list to store the filtered courses
    filtered_courses = []

    if search_input:
        # Filter courses based on both subject name and grade
        filtered_courses = Course.objects.filter(
            Q(grade__icontains=search_input) | Q(subject__subject_name__icontains=search_input) | Q(board__board_name__icontains=search_input)
        )
    print(filtered_courses)
    course_data = [{"id": course.id, "subject": course.subject.subject_name, "board": course.board.board_name, "grade": course.grade} for course in filtered_courses]
    response_data = json.dumps(course_data)
    return HttpResponse(response_data, content_type="application/json")

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

    topics = Topic.objects.filter(course_id=course_id)

    firstTopic = Topic.objects.filter(course_id=course_id)[:1]

    if firstTopic:
        topic_data = [{"id": topic.id, "name": topic.title} for topic in topics]
        response_data = json.dumps(topic_data)
        try:
            topic_id = firstTopic[0].id

            subtopics = SubTopics.objects.filter(topic_id=topic_id, status='Not Started')
            
            topic_names = []
            subtopic_ids = []
            subtopic_names = []
            subtopic_statuses = []

            # Iterate over the queryset or handle the objects as needed
            for subtopic in subtopics:
                topic_names.append(subtopic.topic.title)
                subtopic_ids.append(subtopic.id)
                subtopic_names.append(subtopic.name)
                subtopic_statuses.append(subtopic.status)

            # Create a dictionary with all the data you want to send to the template
            context_data = {
                'topic_data_json': response_data,
                'board_name': boardName,
                'subject_name': subjectName,
                'grade': courseData.grade,
                'topic_names': topic_names,  # Include the lists in the context data
                'subtopic_ids': subtopic_ids,
                'subtopic_names': subtopic_names,
                'subtopic_statuses': subtopic_statuses,
            }
            return render(request, 'content_view.html', context_data)
            # return render(request, 'content_view.html', {
            #     'topic_data_json': response_data,
            #     'board_name': boardName,
            #     'subject_name': subjectName,
            #     'grade': courseData.grade,
            #     "topic_id":subtopic.topic_id,
            #     "topic_name":subtopic.topic.title,
            #     "subtopic_id": subtopic.id,
            #     "subtopic_name": subtopic.name,
            #     "subtopic_status": subtopic.status
            # })

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
        content_details = ContentDetail.objects.filter(subtopic_id=subtopic.id)
        
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

            contentRecords = ContentDetail.objects.filter(status="approved", subtopic=subtopicObj).select_related(
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

        contentreating = FLMContentRating( subtopic_id=subtopicId, videoRating=videoRating, worksheetRating=worksheetRating, comment=comment, status='active', reviewer_id='0')
        contentreating.save()
        course_data={
            "status" : "success",
            "message": "Rating saved successfully",
        }
        response_data = json.dumps(course_data)
        return HttpResponse(response_data, content_type="application/json")

def delete_board_api(request):
# logout 
def logout_view(request):
    logout(request)
    return redirect('')  





