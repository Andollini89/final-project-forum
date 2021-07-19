import json
import string
from django.conf import settings
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.utils import Error
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
import string
import json
import datetime
from.models import *
from .forms import *

# Create your views here.

def index(request):
    index = {
        'latest': Topic.objects.all().order_by('-timestamp')[:5],
        'latest_open': Topic.objects.filter(closed=True).order_by('-timestamp')[:5],
    }
    return render(request, "app/index.html",{
        "index" : index
    })

def closed_topics(request):
    try:
        topics = Topic.objects.filter(closed=True).order_by('-timestamp')
        paginator = Paginator(topics, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "app/topic_list.html", {
            'title': 'Closed Questions',
            'topics' : page_obj,
        })
    except:
        return render(request, "app/topic_list.html", {
            'title': 'Closed Topics',
            'message' : 'No topics to show!',
        })

def open_topics(request):
    try:
        topics = Topic.objects.filter(closed=False).order_by('-timestamp')
        paginator = Paginator(topics, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "app/topic_list.html", {
            'title': 'Open Questions',
            'topics' : page_obj,
        })
    except:
        return render(request, "app/topic_list.html", {
            'title': 'Open Topics',
            'message' : 'No topics to show!',
        })

def all_topics(request):
    try:
        topics = Topic.objects.all().order_by('-timestamp')
        paginator = Paginator(topics, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "app/topic_list.html", {
            'title': 'All Topics',
            'topics' : page_obj,
        })
    except:
        return render(request, "app/topic_list.html", {
            'title': 'All Topics',
            'message' : 'No topics to show!',
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
        answers = Answer.objects.filter(topic= topic).order_by('-timestamp','correct')
   
        
        return render(request, "app/topic.html",{
            "topic": topic,
            "answers":answers,
            "answerForm": AnswerForm(),
            'topicForm' :BodyForm(),
            
        })


# ------ LOGIN REQUIRED VIEWS------ #

@login_required(login_url='login')
def new_topic(request):
    """ This view function calls the url for make a new Topic"""

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

@login_required(login_url='login')
def user_profile_view(request, username):
    """ This function render the user profile and all the posts related """

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        return render(request, 'app/user_profile.html',{
            "profile" : profile,
            'topics':Topic.objects.filter(author= profile.user).order_by('-timestamp'),
            
            # brake profile!!!!
            'form': BodyForm()
        })
    except:
        message = [" OOPS!!! ", "The Profile you are looking for does not exist!!"]
        return render(request, 'app/oops.html', {
            'error_number': 404,
            'message':message,                
        })


@login_required(login_url='login')
def edit_profile(request, profile_id):
    """ This function act as:
        - 'Post' Method to save changes in the user profile
        - 'Get' Method to show the form page to modify user profile"""

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
def edit_topic(request, topic_id):
    """ This function is used to edit the topics from the autor via json
        - POST Method : save the changes to the specific topic,
        - PUT Method : change the status of the post from open to close,
        - DELETE Method : delete the Topic in question.
        if none of the above method is call return a invalid request rendering a error page"""
    
    if request.method == 'POST':
        topic = Topic.objects.get(pk=topic_id)
        form = BodyForm(request.POST, request.FILES, instance=topic)
        
        if form.is_valid():
            form.save()
    
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    elif request.method == 'PUT':
        
        try:
            data = json.loads(request.body)
            topic = Topic.objects.get(pk=data['id'])
            topic.closed = data['closed']
            topic.timestamp = datetime.datetime.now()
            topic.save()
            return JsonResponse({'message' : 'Topic closed'})
        except:
            return JsonResponse({'message': 'failed'})

    elif request.method == 'DELETE':
        
        try:
            data = json.loads(request.body)
            topic = Topic.objects.get(pk=data['id'])
            topic.delete()
            return JsonResponse({'message': 'topic deleted'})
        except:
            return JsonResponse({'message': 'failed'})
   
    else:
        
        message = ['OOOPS!!', 'It seems that you are tring something you are not autorized to']
        return render(request, 'app/oops.html',{
            'error_number': 403,
            'message' : message,
        })
@login_required(login_url='login')
def edit_answer(request, answer_id):
    
    if request.method == 'POST':
        answer = Answer.objects.get(pk=answer_id)
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        
        if form.is_valid():
            form.save()
    
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    elif request.method == 'PUT':
        
        try:
            data = json.loads(request.body)
            answer = Answer.objects.get(pk=data['id'])
            answer.correct = data['correct']
            answer.save()
            return JsonResponse({'message' : 'Answer correct', 'status': answer.correct})
        except:
            return JsonResponse({'message': 'failed'})
    
    elif request.method == 'DELETE':
       
        try:
            data = json.loads(request.body)
            answer = Answer.objects.get(pk=data['id'])
            answer.delete()
            return JsonResponse({'message': 'answer deleted'})
        except:
            return JsonResponse({'message': 'failed'})
    else:
        message = ['OOOPS!!', 'It seems that you are tring something you are not autorized to']
        return render(request, 'app/oops.html',{
            'error_number': 403,
            'message' : message,
        })
def add_votes(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        answer = Answer.objects.get(pk=data['id'])
        print(data['vote'])
        if data['vote'] == 1:
            try:
                vote = Votes.objects.get(user=request.user, answer=answer, vote_type='down')
                if vote:
                    vote.delete()
            except:
                pass
            response = answer.upvote(user=request.user)
            if response:
                return JsonResponse({'message': 'upvoted', 'updatevotes': answer.votes,})
            else:
                return JsonResponse({'message': 'vote failed','updatevotes': answer.votes,})
        elif data['vote'] == -1:
            try:
                vote = Votes.objects.get(user=request.user, answer=answer, vote_type='up')
                if vote:
                    vote.delete()
            except:
                pass
            response = answer.downvote(user=request.user,)
            if response:
                return JsonResponse({'message': 'downvoted', 'updatevotes': answer.votes,})
            else:
                return JsonResponse({'message': 'vote failed', 'updatevotes': answer.votes,})
        else:
             message = ['OOOPS!!', 'It seems that you are tring something you are not autorized to']
        return render(request, 'app/oops.html',{
            'error_number': 403,
            'message' : message,
        })

    
    
def search_view(request):
    """ This function serch through all the topic and answers for a match"""
    
    
    query = request.GET['query']
    
    if query == '':
        return HttpResponseRedirect(reverse('all_topics'))

    query_set = query.split()
    query_set[-1] = query_set[-1].translate(str.maketrans('', '', string.punctuation))
    print(query_set)
    results = []
    for q in query_set:
        try:
            topics = Topic.objects.filter(Q(title__icontains = q) | Q(body__icontains=q))
            if topics:
                for topic in topics:
                    results.append(topic)
        except: 
            continue
    
    if results: 
        print(results)   
        return render(request, 'app/search_view.html',{
        'results': set(results),
        })
    else:
        message= 'No results to show...'
        return render(request, 'app/search_view.html',{
            'message': message
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
