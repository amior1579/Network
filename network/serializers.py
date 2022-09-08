from attr import fields
from rest_framework import serializers
from .models import *

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'