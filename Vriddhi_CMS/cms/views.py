from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import json
from django.http import HttpResponse
from cms.models import *
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
# from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    get_all_topic = Topic.objects.all()
    get_all_subtopic = SubTopics.objects.all()
    # get_content = SubTopics.ContentDetail.objects.all()
    return render(request, 'content_view.html',{'get_all_topic':get_all_topic, 'get_all_subtopic': get_all_subtopic})




def logout_view(request):
    logout(request)
    return redirect('')  


# @login_required
# def protected_view(request):
#     return render(request, 'protected_template.html')