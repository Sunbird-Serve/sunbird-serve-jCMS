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
# from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta
from django.shortcuts import render as render_response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def get_courses(request):
    board_id = request.GET.get("board_id")
    courses = Course.objects.filter(board_id=board_id)
    course_data = [{"id": course.id, "name": course.subject.subject_name, "board": course.board.board_name, "grade": course.grade} for course in courses]
    response_data = json.dumps(course_data)
    return HttpResponse(response_data, content_type="application/json")

def get_topics(request):
    course_id = request.GET.get("course_id")
    topics = Topic.objects.filter(course_id=course_id)
    topic_data = [{"id": topic.id, "name": topic.title} for topic in topics]
    response_data = json.dumps(topic_data)
    return HttpResponse(response_data, content_type="application/json")

def view_course(request):
    get_all_board = Board.objects.all()
    get_course_details = Course.objects.all()
    return render(request, 'course_view.html',{'get_all_board':get_all_board,'get_course_details': get_course_details})








def view_course(request):
    get_all_board = Board.objects.all()
    get_course_details = Course.objects.all()

    # Number of items per page
    items_per_page = 10  # You can adjust this according to your preference

    paginator = Paginator(get_course_details, items_per_page)
    page = request.GET.get('page')

    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        courses = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        courses = paginator.page(paginator.num_pages)

    return render(request, 'course_view.html', {
        'get_all_board': get_all_board,
        'courses': courses,
    })


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




def view_content(request):
    course_id = request.GET.get('courseID')
    target_url = '/home/content_detail/?courseID={}'.format(course_id)
    return HttpResponseRedirect(target_url)


def content_detail_view(request):
    course_id = request.GET.get('courseID')
    topics = Topic.objects.filter(course_id=course_id)
    topic_data = [{"id": topic.id, "name": topic.title} for topic in topics]
    response_data = json.dumps(topic_data)
    return render(request, 'content_view.html', {'topic_data_json': response_data})

# def getSubtopic(request):
#     topicId = request.GET.get('topicId')
#     subTopic = SubTopics.objects.filter(topic_id = topicId)
#     subTopicName = [{"id":subtopic.id, "name":subtopic.name, "content":subtopic.ContentDetail.url, "status":subtopic.ContentDetail.staus }for subtopic in subTopic]
#     response_data = json.dumps(subTopicName)
#     return HttpResponse(response_data, content_type="application/json")

def getSubtopic(request):
    topicId = request.GET.get('topicId')
    
    # Fetch SubTopics based on the given topicId
    subtopics = SubTopics.objects.filter(topic_id=topicId)
    
    subTopicData = []
    
    # Iterate through each subtopic
    for subtopic in subtopics:
        subtopic_data = {
            "id": subtopic.id,
            "name": subtopic.name,
            "status": subtopic.status,
            "content_details": []  # Initialize an empty list to store content details
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
    def getChildRecord(self,contentId):
        try:
            url = "https://api.dev.diksha.gov.in/api/content/v1/read/"+contentId
            authDict = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBOGt5dGptMDdXN2tJOGxNY0c3Unljc3I2b1Q2NWhoViJ9.OMhRtUiochad7pMiozTVY9lOUC9kG3Us7NnA-lezVoc"}

            url = str(url)
            response = requests.get(url,headers=authDict)
            respDict = response.json()
            responseCode = respDict.get("responseCode")
            contentList = []

            if responseCode == "OK":
                result = respDict.get("result")
                contentObj = result.get("content")
                if contentObj:
                    name = contentObj.get("name")
                    mimeType = contentObj.get("mimeType")
                    artifactUrl = contentObj.get("artifactUrl")
                    if (mimeType == "video/mp4" or mimeType == "application/pdf") and artifactUrl:
                        mimtype = "worksheet"
                        if mimeType == "video/mp4":
                            mimtype = "video"

                        ctObj = {
                            "id":contentId,
                            "name":name,
                            "url":artifactUrl,
                            "mimeType":mimtype

                        }
                        contentList.append(ctObj)


            #print("contentList",contentList)
            return contentList
        except Exception as e:
            print("getChildRecord ",e)
            traceback.print_exc()
            return None

    def getChildNodeDetails(self,leafNodes):
        try:
            childList = []
            for contentId in leafNodes:
                #print("contentId",contentId)
                newList = self.getChildRecord(contentId)
                if newList and len(newList) > 0:
                    childList.extend(newList)
            #print("childList",childList)
            return childList
        except Exception as e:
            print("getChildNodeDetails ",e)
            traceback.print_exc()
            return None

    def getChildRecord(self, contentId):
        try:
            url = "https://api.dev.diksha.gov.in/api/content/v1/read/" + contentId
            authDict = {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBOGt5dGptMDdXN2tJOGxNY0c3Unljc3I2b1Q2NWhoViJ9.OMhRtUiochad7pMiozTVY9lOUC9kG3Us7NnA-lezVoc"}

            url = str(url)
            response = requests.get(url, headers=authDict)
            respDict = response.json()
            responseCode = respDict.get("responseCode")
            contentList = []

            if responseCode == "OK":
                result = respDict.get("result")
                contentObj = result.get("content")
                if contentObj:
                    name = contentObj.get("name")
                    mimeType = contentObj.get("mimeType")
                    artifactUrl = contentObj.get("artifactUrl")
                    if (mimeType == "video/mp4" or mimeType == "application/pdf") and artifactUrl:
                        mimtype = "worksheet"
                        if mimeType == "video/mp4":
                            mimtype = "video"

                        ctObj = {
                            "id": contentId,
                            "name": name,
                            "url": artifactUrl,
                            "mimeType": mimtype

                        }
                        contentList.append(ctObj)
            return contentList
        except Exception as e:
            traceback.print_exc()
            return None

    def getChildNodeDetails(self, leafNodes):
        try:
            childList = []
            for contentId in leafNodes:
                newList = self.getChildRecord(contentId)
                if newList and len(newList) > 0:
                    childList.extend(newList)
            return childList
        except Exception as e:
            traceback.print_exc()
            return None

    def getContentFromThirdParty(self):
        try:
            url = "https://api.dev.diksha.gov.in/api/content/v1/search"
            payloadData = {
                "request": {

                    "filters": {
                        "primaryCategory": [
                            "Digital Textbook"
                        ],
                        "se_boards": [
                            "CBSE"
                        ],
                        "se_mediums": [
                            "English"
                        ],
                        "se_gradeLevels": [
                            "Class 7"
                        ]
                    },
                    "limit": 1000,
                    "fields": [
                        "string",
                        "name",
                        "contentType",
                        "leafNodes"

                    ]
                }
            }


            authDict = {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBOGt5dGptMDdXN2tJOGxNY0c3Unljc3I2b1Q2NWhoViJ9.OMhRtUiochad7pMiozTVY9lOUC9kG3Us7NnA-lezVoc"}
            response = requests.post(url, json=payloadData, headers=authDict)
            print(response)
            respDict = response.json()
            responseCode = respDict.get("responseCode")
            contentList = []
            videoList = []
            if responseCode == "OK":
                result = respDict.get("result")
                contentObjs = result.get("content")
                for each in contentObjs:
                    eachId = each.get("identifier")
                    contentType = each.get("contentType")


                    leafNodes = each.get("leafNodes")
                    if leafNodes and len(leafNodes) > 0:
                        pass
                    tlist = self.getChildNodeDetails(leafNodes)
                    if tlist and len(tlist) > 0:
                        for newObj in tlist:
                            cType = newObj.get("mimeType")
                            eachDict = {
                                "id": 3788,
                                "did": newObj.get("id"),
                                "title": newObj.get("name"),
                                "contentType": newObj.get("mimeType"),
                                "url": newObj.get("url"),
                                "author": "Diksha",
                                "duration": 960,
                                "isPrimary": True,
                                "contentHost": "s3",
                                "description": ''

                            }
                            if cType != "video":
                                contentList.append(eachDict)
                            else:
                                videoList.append(eachDict)



                    else:
                        eachDict = {
                            "id": 3788,
                            "did": eachId,
                            "title": each.get("name"),
                            "contentType": contentType,
                            "objectType": each.get("objectType"),
                            "url": "https://dev.diksha.gov.in/play/collection/" + eachId + "?contentType=" + contentType
                        }

                        contentList.append(eachDict)


                return (contentList, videoList)
            else:
                return ([], [])


        except Exception as e:
            traceback.print_exc()
            return (None, None)



    @method_decorator(login_required)
    def get(self, request,  *args, **kwargs):
        try:

            subtopicId = self.request.GET.get('subtopic_id', None)
            topicId = self.request.GET.get('topic_id', None)

   
                # offeringObj = Offering.objects.get(id=offeringId)
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
            
            return render_response(self.request, 'flm_content_details.html', context)
        except  Exception  as e:
            return HttpResponseNotFound("Page not found " + e.message)

    @method_decorator(login_required)
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

def content_rating(request):
    # {topicId: "4", subtopicId: "1", videoRating: 3, worksheetRating: 4, comment: "ss"}
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


def logout_view(request):
    logout(request)
    return redirect('')  


# @login_required
# def protected_view(request):
#     return render(request, 'protected_template.html')