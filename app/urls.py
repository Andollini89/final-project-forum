from os import name
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    
    # GET VIEWS
    
    path("", views.index, name="index"),
    path("closed-topics", views.closed_topics, name='closed_topics'),
    path("open-topics", views.open_topics, name='open_topics'),
    path("all-topics", views.all_topics, name='all_topics'),
    path('<str:username>-profile', views.user_profile_view, name='profile'),
    path("read_topic/topic/<int:topic_id>", views.topic_view, name='topic'),
    path("logout", views.logout_view, name="logout"),
    
    # GET AND POST VIEWS

    path("login", views.login_view, name="login"),
    path("register", views.register, name='register'),
    path("new-topic", views.new_topic, name='new_topic'),
    path("search-results", views.search_view, name= 'search'),
    
    # POST VIEWS

    path('edit/<str:profile_id>', views.edit_profile, name='edit_profile'),
    path('edittopic/<str:topic_id>', views.edit_topic, name= 'edit_topic'),
    path('editanswer/<str:answer_id>', views.edit_answer, name='edit_answer'),
    path('add-vote', views.add_votes, name='votes'),

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)