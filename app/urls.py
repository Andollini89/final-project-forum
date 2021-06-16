from os import name
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name='register'),
    path("new-topic", views.new_topic, name='new_topic'),
    path("read_topic/topic/<int:topic_id>", views.topic_view, name='topic'),
    path("search-results", views.search_view, name= 'search'),
    path('<str:username>-profile', views.user_profile_view, name='profile'),
    path('edit/<str:profile_id>', views.edit_profile, name='edit_profile'),
    
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)