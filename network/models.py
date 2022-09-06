from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Posts(models.Model):
    post_uesr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='create_user')
    post_title = models.CharField(max_length=200)
    post_description = models.TextField()
    post_likes = models.IntegerField()
    post_date = models.DateField(primary_key=True)

    def __str__(self):
        return f'{self.post_uesr}'