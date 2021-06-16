import json
from django.conf import settings
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
import re
from.models import *
from .forms import *

# Create your views here.

def index(request):
    topic_form = TopicForm()
    topics = Topic.objects.all().order_by('-timestamp')
    for topic in topics:
        if len(topic.body) > 150:
            topic.body = f"{topic.body[:150]}..."
    return render(request, "app/index.html",{
        "topics" : topics, 
        "form": topic_form,
    })
@login_required(login_url='login')
def new_topic(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        form = TopicForm(request.POST)
        if form.is_valid:
            f = form.save(commit=False)
            f.author = user
            f.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "app/new_topic.html",{
            "form": TopicForm()
        })
def topic_view(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    
    if request.method == 'POST':
        answer = AnswerForm(request.POST)
        user = User.objects.get(username=request.user)
        if answer.is_valid:
            a = answer.save(commit=False)
            a.topic= topic
            print(a.topic.id)
            a.responder = user
            a.save()
            send_mail(
                subject= f"New answer from: {a.responder} to your {topic.title} Topic",
                message= a.answer,
                html_message= a.answer,
                from_email= settings.EMAIL_HOST_USER,
                recipient_list= [topic.author.email],
                fail_silently= False,
                
            )
        return  HttpResponseRedirect(reverse('topic', kwargs={'topic_id':a.topic.id}))
    else:
        answers = Answer.objects.filter(topic= topic).order_by('-timestamp')
   
        
        return render(request, "app/topic.html",{
            "topic": topic,
            "answers":answers,
            "answerForm": AnswerForm(),
            
        })

def edit_profile(request, profile_id):
    if request.method == 'POST':
        profile = Profile.objects.get(pk=profile_id)
        edit = ProfileForm(request.POST, request.FILES, instance=profile)
        user = User.objects.get(pk=profile.user.id)
        
        if edit.is_valid():
            edit.save()
            user.img = profile.image
            user.save()
        
        return HttpResponseRedirect(reverse('profile', kwargs={
            'username': profile.user.username
            }))
    else:
        profile = Profile.objects.get(pk=profile_id)
        form = ProfileForm(initial=profile.profile_serialize())

        return render(request, 'app/edit_profile.html',{
            'form': form,
        })

@login_required(login_url='login')
def user_profile_view(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        print(profile.user)
        return render(request, 'app/user_profile.html',{
            "profile" : profile,
            'topics':Topic.objects.filter(author= profile.user),
            
            # brake profile!!!!
            #'form': EditTopicForm()
        })
    except:
        message = [" OOPS!!! ", "The Profile you are looking for does not exist!!"]
        return render(request, 'app/oops.html', {
            'error_number': 404,
            'message':message,                
        })

def search_view(request):
    queryset = Topic.objects.all()
    query = request.GET['query']
    results = []
    for topic in queryset:
        if query in topic.title:
            results.append(topic)
        elif query in topic.body:
            results.append(topic)
        elif query in topic.author.username:
            results.append(topic)
    
    for topic in results:
        if len(topic.body) > 50:
            topic.body = f"{topic.body[:50]}..."
    
    return render(request, 'app/search_view.html',{
        "results": set(results)
    })


def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        user =authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            prev_url = str(request.META.get('HTTP_REFERER'))
            if prev_url.endswith('/login'):
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else: 
            return render(request, "app/login.html",{
            'message': "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match.",
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken.",
            })
        login(request, user)

        
        profile = Profile(user=user,username=user.username, email=user.email, )
        print(profile)
        profile.save()
        

        prev_url = str(request.META.get('HTTP_REFERER'))
        if prev_url.endswith('/register'):
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, "app/register.html")


def logout_view(request):
    logout(request)

    prev_url = str(request.META.get('HTTP_REFERER'))
    try:

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        return HttpResponseRedirect(reverse('index'))
