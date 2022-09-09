from ast import Not
from distutils.errors import LinkError
from tkinter import NO
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import JsonResponse
import json
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *


from .models import *


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def all_posts(request):
    all_post = Posts.objects.all().exclude(post_uesr = request.user).order_by('-id')
    paginator = Paginator(all_post,10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, "network/all_posts.html",{
        'posts':posts
    })


def my_account(request,user):
    all_post = Posts.objects.filter(post_uesr = request.user)
    follower_len = Followers.objects.filter(user = user).count()
    following_len = Followers.objects.filter(follower = user).count()
    return render(request, 'network/my_account.html',{
        'posts': all_post,
        'follower_len': follower_len,
        'following_len': following_len,
    })

def profile(request,user):
    follower = request.user
    user = User.objects.get(username = user)
    all_post_user = Posts.objects.filter(post_uesr = user) 
    follower_len = Followers.objects.filter(user = user).count()
    following_len = Followers.objects.filter(follower = user).count()
    user_follower = Followers.objects.filter(user = user)
    user_follower_lists = []
    for i in user_follower:
        user_follower = i.follower
        user_follower_lists.append(user_follower)

    print(user_follower_lists)
    if follower.username in user_follower_lists is not None:
        button_and_value = 'Unfollow'
    else:
        button_and_value = 'Follow'

    return render(request, 'network/profile.html',{
        'posts': all_post_user,
        'user':user,
        'follower':follower,
        'follower_len':follower_len,
        'following_len':following_len,
        'button_and_value':button_and_value,
    })

def follower(request):
    if request.method == 'POST':
        value = request.POST['value']
        user = request.POST['user']
        follower = request.POST['follower']
        if value == 'Follow':
            followers = Followers.objects.create(follower=follower, user=user)
            followers.save()
        elif value == 'Unfollow':
            unfollow = Followers.objects.get(follower=follower, user=user)
            unfollow.delete()
        return redirect('profile', user=user)


def following_posts(request):
    user = request.user
    userr = User.objects.get(username = request.user)
    # followers = Followers.objects.filter(follower=userr)
    # print(followers)
    # all_post = Posts.objects.filter(post_uesr = followers)
    # paginator = Paginator(all_post,10)
    # page = request.GET.get('page')
    # posts = paginator.get_page(page)
    return render(request, 'network/following_posts.html',{
        # 'posts':posts,
    })

def add_post(request):
    title = request.POST['title']
    description = request.POST['description']
    post = Posts(post_title=title, post_description=description, post_uesr=request.user)
    post.save()
    return HttpResponseRedirect(reverse('all_posts'))
    # return JsonResponse({"message": "send post."}, status=201)


def update_post(request,id):
    pass

@login_required
def posts(request):
    post = Posts.objects.filter(post_uesr = request.user)
    return JsonResponse([posts.serialize() for posts in post], safe=False)


@api_view(['GET'])
def posts(request):
    post = Posts.objects.filter(post_uesr = request.user)
    serializer = PostsSerializer(post, many=True)
    return Response(serializer.data)
    

@csrf_exempt
@api_view(['GET', 'PUT'])
def posts_id(request,id):
    try:
        post = Posts.objects.get(id = id)
    except Posts.DoesNotExist:
        return Response({"error": "post not found."}, status=404)

    if request.method == "GET":
        serializer = PostsSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostsSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return JsonResponse({"error": "GET or PUT request required."}, status=400)
    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)
        # return JsonResponse([posts.serialize() for posts in post], safe=False)


@api_view(['GET'])
def api(request):
    api_urls ={
        'List':'/task-list/',
        'Detail View':'/task-detail/<str:pk>/',
        'Create':'/task-create/',
        'Update':'/task-update/<str:pk>/',
        'Delete':'/task-delete/<str:pk>/',
        
    }
    return Response(api_urls)


