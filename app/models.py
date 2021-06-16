from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class User(AbstractUser):
    img = models.ImageField(blank=True, null=True)
    

class Topic(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    body = RichTextUploadingField(blank=False, null=False)
    #body = models.TextField(max_length=10000, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.author.username + " : " + self.title

class Answer(models.Model):
    answer = RichTextUploadingField(blank=False, null=False)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE, related_name="topic")
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responder')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.topic.title + " : " + self.answer


class Profile(models.Model):
   
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name= 'userprofile')
    
    username =models.CharField(max_length=255, null=False, blank=False)
    email= models.EmailField(max_length=255, blank=False, null=False)

    name = models.CharField(max_length=255, null=True, blank=True)
    surname= models.CharField(max_length=255, blank=True, null=True)
    
    city= models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True,null=True)
    
    description = models.TextField(max_length=10000, blank=True, null=True)
    
    image= models.ImageField(null=True, blank=True,)
    

    timestamp= models.DateTimeField(auto_now_add=True)

    def profile_serialize(self):
        return {
            'id':self.pk,
            'user':self.user,
            'name':self.name,
            'surname':self.surname,
            'city':self.city,
            'country':self.country,
            'username':self.username,
            'description':self.description,
            'image':self.image,
            'email':self.email,
            'date':self.timestamp
        }
    def __str__(self):
        return self.username