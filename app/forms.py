from django import forms
from django.db.models import fields
from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _
from .models import *

class ProfileForm(ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user',)

class TopicForm( ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'body']
        labels = {
            "body": _("Write here:")
        }

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields =['answer']
        labels = {
            "answer": ""
        }
        
class BodyForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['body']
        labels = {
            'body': ''
        }
