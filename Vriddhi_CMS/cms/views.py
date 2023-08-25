from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import json
from django.http import HttpResponse
from cms.models import Course
from cms.models import Topic

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
    get_course_details = Course.objects.all()
    return render(request, 'course_view.html',{'get_course_details': get_course_details})
