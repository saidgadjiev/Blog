from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField(default=0)
    avatar_url = models.ImageField(upload_to='users')

class Question(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=60)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    tags = TagField()

class Answer(models.Model):
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_right = models.BooleanField(default=False) 
