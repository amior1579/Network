from ast import Not
from distutils.errors import LinkError
from genericpath import exists
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
    user = request.user
    all_post = Posts.objects.all().order_by('-id').exclude(post_uesr = user)
    paginator = Paginator(all_post,10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # post_likes_list = []
    # for i in posts:
    #     post_likes = i.post_likes
    #     post_likes_list.append(post_likes) 
    # print(post_likes_list)

    # if user in post_likes_list is not None:
    #     button_like = 'Unlike'
    # else:
    #     button_like = 'Like'
        # print(button_like)

    return render(request, "network/all_posts.html",{
        'posts':posts,
        # 'button':button_like,
    })


def my_account(request,user):
    all_post = Posts.objects.filter(post_uesr = request.user).order_by('-id')
    userr = User.objects.get(username = user)
    follower_len = Followers.objects.filter(followed_users = userr).count()
    following_len = Followers.objects.filter(follower = userr).count()
    return render(request, 'network/my_account.html',{
        'posts': all_post,
        'follower_len': follower_len,
        'following_len': following_len,
    })

def profile(request,user):
    follower = request.user
    user = User.objects.get(username = user)
    all_post_user = Posts.objects.filter(post_uesr = user).order_by('-id')
    followed_users_len = Followers.objects.filter(followed_users = user).count()
    following_len = Followers.objects.filter(follower = user).count()
    followed_users = Followers.objects.filter(followed_users = user)
    followed_users_list = []
    for i in followed_users:
        for_followed_users = i.follower
        followed_users_list.append(for_followed_users.username)

    # print(followed_users_list)
    if follower.username in followed_users_list is not None:
        button_and_value = 'Unfollow'
    else:
        button_and_value = 'Follow'

    return render(request, 'network/profile.html',{
        'posts': all_post_user,
        'user':user,
        'follower':follower,
        'follower_len':followed_users_len,
        'following_len':following_len,
        'button_and_value':button_and_value,
    })

def follower(request):
    if request.method == 'POST':
        value = request.POST['value']
        followed_users = request.POST['user']
        follower = request.user
        followed_users_username = User.objects.get(username = followed_users)
        
        if value == 'Follow':
            followers = Followers.objects.create(follower=follower, followed_users=followed_users_username)
            followers.save()
            print(followers)
        elif value == 'Unfollow':
            unfollow = Followers.objects.get(follower=follower, followed_users=followed_users_username)
            unfollow.delete()
        return redirect('profile', user=followed_users)


def following_posts(request):
    followed_users_list = []
    posts_list = []
    username1 = User.objects.get(username = request.user)
    followers = Followers.objects.filter(follower=username1)
    for i in followers:
        followed_users_list.append(i.followed_users)

    for x in followed_users_list:
        username2 = User.objects.get(username = x)
        all_post = Posts.objects.filter(post_uesr = username2).order_by('-id')

        for y in all_post:
            posts_list.append(y)

    # print(posts_list)
    paginator = Paginator(posts_list,10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'network/following_posts.html',{
        'posts':posts,
    })


def add_post(request):
    user = request.user
    title = request.POST['title']
    description = request.POST['description']
    post = Posts(post_title=title, post_description=description, post_uesr=request.user)
    post.save()
    return redirect('my_account', user=user)






def update_post(request,id):
    pass

@login_required
def posts(request):
    # post = Posts.objects.filter(post_uesr = request.user)
    post = Posts.objects.all().order_by('-id')
 
    return JsonResponse([posts.serialize() for posts in post], safe=False)


@csrf_exempt
@login_required
def posts_id(request, id):

    try:
        posts = Posts.objects.get(post_uesr=request.user, id=id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(posts.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        posts.post_description = data["description"]
        posts.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)

@login_required
@csrf_exempt
def like(request):
    user = request.user
    like = Likes.objects.all()

    if request.method == "GET":
        return JsonResponse([likes.serialize() for likes in like], safe=False)

    elif request.method == "PUT":
        data = json.loads(request.body)
        id = data["post"]
        postss = Posts.objects.get(id = id)
        list_user = postss.post_likes
        
        if(user in list_user.all() is not None):
            list_user.remove(user) 
            print('remove')
            # button = 'Like'

        else:
            list_user.add(user) 
            print('add')
        # postss.save()
        print(list_user.all())
        return HttpResponse(status=204)

    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)


@login_required
@csrf_exempt
def like_post(request):
    # like = Likes.objects.get(id = id)
    like = Likes.objects.all()
    posts = Posts.objects.get(id=id)




    # if request.method == "GET":
    #     return JsonResponse(like.serialize())

    # elif request.method == "PUT":
    #     data = json.loads(request.body)
    #     like.post_description = data["description"]
    #     like.save()
    #     return HttpResponse(status=204)

    # else:
    #     return JsonResponse({"error": "GET or PUT request required."}, status=400)







    # if request.method == "GET":
    #     return JsonResponse(like.serialize())

    # if( user in post.post_likes).exist():
    #     post.post_likes.remove(user)
    # else:
    #     post.post_likes.add(user)

    # return redirect('all_posts')

# @api_view(['GET'])
# def posts(request):
#     post = Posts.objects.filter(post_uesr = request.user)
#     serializer = PostsSerializer(post, many=True)
#     return Response(serializer.data)
    

# @csrf_exempt
# @api_view(['GET', 'PUT'])
# def posts_id(request,id):
#     try:
#         post = Posts.objects.get(id = id, post_uesr = request.user)
#     except Posts.DoesNotExist:
#         return Response({"error": "post not found."}, status=404)

#     if request.method == "GET":
#         serializer = PostsSerializer(post)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = PostsSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return HttpResponse(status=204)
#         return JsonResponse({"error": "GET or PUT request required."}, status=400)
#     else:
#         return JsonResponse({""}, status=204)
#         # return JsonResponse([posts.serialize() for posts in post], safe=False)


# @api_view(['GET'])
# def api(request):
#     api_urls ={
#         'List':'/task-list/',
#         'Detail View':'/task-detail/<str:pk>/',
#         'Create':'/task-create/',
#         'Update':'/task-update/<str:pk>/',
#         'Delete':'/task-delete/<str:pk>/',
        
#     }
#     return Response(api_urls)


