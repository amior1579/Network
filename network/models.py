from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime 
from .models import *


class User(AbstractUser):
    pass

class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='follower')
    followed_users = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='followed_users')

    def __str__(self):
        return f'{self.follower},  followed {self.followed_users}'

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    post_uesr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='create_user')
    post_title = models.CharField(max_length=200)
    post_description = models.TextField()
    post_date = models.DateTimeField(default=datetime.now, blank=True)
    post_likes = models.ManyToManyField(User,blank=True,default=None, related_name='post_likes')
    like_count = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.id}.{self.post_title},{self.post_uesr}'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.post_title,
            "description": self.post_description,
            "date": self.post_date
        }

