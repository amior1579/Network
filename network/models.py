from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime 
from .models import *


class User(AbstractUser):
    pass

# class Followers(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
#     follower = models.ManyToManyField(User,blank=True,default=None, related_name='follower')
#     following = models.ManyToManyField(User,blank=True,default=None, related_name='following')

#     def __str__(self):
#         return f'{self.user}.{self.follower},{self.following}'

class Followers(models.Model):
    user = models.CharField(max_length=1000, null=True)
    follower = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.follower},  followed {self.user}'

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
            "post_title": self.post_title,
            "description": self.post_description,
            "post_date": self.post_date
        }

